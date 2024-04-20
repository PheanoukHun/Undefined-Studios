import pygame
from button import Button

WIDTH, HEIGHT = (750, 500)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buttons")

START_BUTTON_PRESSED = pygame.USEREVENT + 1
EXIT_BUTTON_PRESSED = pygame.USEREVENT + 2

start_button = Button(100, 200, "buttons\start_btn.png", START_BUTTON_PRESSED)
exit_button = Button(450, 200, "buttons\exit_btn.png", EXIT_BUTTON_PRESSED)

start_button.scale(0.5)
exit_button.scale(0.5)

run = True
while run:

    screen.fill((202, 228, 241))

    start_button.draw(screen)
    exit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == START_BUTTON_PRESSED:
            print("Start")
        if event.type == EXIT_BUTTON_PRESSED:
            run = False

    pygame.display.update()

pygame.quit()
