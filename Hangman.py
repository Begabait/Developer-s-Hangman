import pygame
import random
import string

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

images = []
for i in range(7):
    images.append(pygame.image.load('hangman{}.png'.format(i)))

letters = []
for letter in string.ascii_uppercase:
    letters.append([letter, 100 + 50 * (string.ascii_uppercase.index(letter) % 13),
                    370 + (string.ascii_uppercase.index(letter) // 13) * 60, True])
words = ['DEVELOPER', 'PYTHON', 'PYGAME', 'WINDOW', 'TEXT EDITOR']
WORD = random.choice(words)
WORD_TO_DISPLAY = ''
passed = []
FPS = 60
clock = pygame.time.Clock()
run = True
status = 0

RADIUS = 20
GAP = 10

word_font = pygame.font.SysFont('comicsans', 45)
letter_font = pygame.font.SysFont('comicsans', 30)
title_font = pygame.font.SysFont('comicsans', 70)


def draw(window):
    window.fill(WHITE)
    window.blit(images[status], (130, 60))
    txt = word_font.render(WORD_TO_DISPLAY, True, BLACK)
    win.blit(txt, ((WIDTH - (209 + txt.get_width())) / 2 + 220, 160))

    for char in letters:
        if char[3]:
            pygame.draw.circle(window, BLACK, (100 + 50 * (string.ascii_uppercase.index(char[0]) % 13), 370 + (string.ascii_uppercase.index(char[0]) // 13) * 60), RADIUS, 4)
            txt = letter_font.render(char[0], True, BLACK)
            window.blit(txt, ((100 + 50 * (string.ascii_uppercase.index(char[0]) % 13)) - txt.get_width() / 2, 370 + (string.ascii_uppercase.index(char[0]) // 13) * 60  - txt.get_height() / 2))

    pygame.display.update()


def display_message(message):
    draw(win)
    pygame.time.delay(1000)
    win.fill(WHITE)
    txt = title_font.render(message, True, BLACK)
    win.blit(txt, ((WIDTH - txt.get_width()) / 2, (HEIGHT - txt.get_height()) / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global FPS, clock, run, status, WORD_TO_DISPLAY, letter, event, end
    while run:
        clock.tick(FPS)

        WORD_TO_DISPLAY = ''
        for letter in WORD:
            if letter in passed:
                WORD_TO_DISPLAY += letter + ' '
            elif letter == ' ':
                WORD_TO_DISPLAY += ' '
            else:
                WORD_TO_DISPLAY += '_ '


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for letter in letters:
                    dis = ((pos[0] - letter[1]) ** 2 + (pos[1] - letter[2]) ** 2) ** 0.5
                    if dis < RADIUS and letter[3]:
                        if letter[0] not in WORD:
                            status += 1
                        passed.append(letter[0])
                        letter[3] = False

        if status == 6:
            display_message('YOU LOST!')
            end = True
            break
        elif '_' not in WORD_TO_DISPLAY:
            display_message('YOU WON!')
            end = True
            break

        draw(win)

end = False
running = True
main()
if run:
    while running:
        letters = []
        for letter in string.ascii_uppercase:
            letters.append([letter, 100 + 50 * (string.ascii_uppercase.index(letter) % 13),
                            370 + (string.ascii_uppercase.index(letter) // 13) * 60, True])
        words = ['DEVELOPER', 'PYTHON', 'PYGAME', 'WINDOW', 'TEXT EDITOR']
        WORD = random.choice(words)
        WORD_TO_DISPLAY = ''
        passed = []
        FPS = 60
        clock = pygame.time.Clock()
        run = True
        status = 0
        again = False

        if end:
            win.fill(WHITE)
            text = [word_font.render('If you want to play again, press the left mouse button.', True, BLACK), word_font.render('Otherwise, press the right mouse button.', True, BLACK)]
            for sentence in text:
                win.blit(sentence, ((WIDTH - sentence.get_width()) / 2, 180 + 70 * text.index(sentence)))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    running = True
                    again = True
                elif event.button == 3:
                    running = False
                    break

        if again:
            main()
            if not run:
                break

pygame.quit()
