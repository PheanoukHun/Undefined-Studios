# Main File

# Libraries #

import random
import pygame
import os

# Game Engine Initiated

pygame.font.init()
pygame.init()

# Initiated Variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_Bullets = 3

spaceship_width, spacehip_height = (60, 60)
width, height = 1018, 573

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("Arial", 40)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 100)

#Window Creation

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Forgetten Frontiers")
BORDER = pygame.Rect(width//2 - 5, 0, 10, height)

# Sprite Image Creation

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")),
    (spaceship_width, spacehip_height)), 270)

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "spaceship_red.png")),
    (spaceship_width, spacehip_height)), 90)

SPACE = pygame.transform.scale(
    pygame.image.load(
    os.path.join("Assets", "space.png")), (width, height))

# Window Refresh Function

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE, (0, 0))

    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text= HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (width - yellow_health_text.get_width() - 10, 10))

    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

# Red Spaceship Movement

def red_movement(key_pressed, red):
    if key_pressed[pygame.K_a] and red.x - VEL > 0:
            red.x -= VEL
    if key_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
        red.x += VEL
    if key_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_s] and red.y + VEL + spacehip_height < height:
        red.y += VEL

# Yellow Spaceship Movement

def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_LEFT] and yellow.x - 3 * VEL > BORDER.x:
            yellow.x -= VEL
    if key_pressed[pygame.K_RIGHT] and yellow.x + VEL + spaceship_width < width:
        yellow.x += VEL
    if key_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_DOWN] and yellow.y + VEL + spacehip_height < height:
        yellow.y += VEL

# Handle Bullets Function

def handle_bullets(yellow_list, red_list, yellow, red):

    for bullet in yellow_list:
        bullet.x -= BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_list.remove(bullet)

        elif bullet.x < -15:
            yellow_list.remove(bullet)

    for bullet in red_list:
        bullet.x += BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_list.remove(bullet)

        elif bullet.x > width + 15:
            red_list.remove(bullet)

# Handle Winning

def draw_winner(text):
    rendered_text = GAME_OVER_FONT.render(text, 1, WHITE)
    WIN.blit(rendered_text, (width // 2 - rendered_text.get_width()//2, height // 2 - rendered_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main loop #

def main():

    red = pygame.Rect(250, 250, spaceship_width, spacehip_height)
    yellow =  pygame.Rect(750, 250, spaceship_width, spacehip_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    winner_text = None
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    if len(red_bullets) < MAX_Bullets:
                        bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)

                if event.key == pygame.K_RCTRL:
                    if len(yellow_bullets) < MAX_Bullets:
                        bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != None:
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed, yellow)
        red_movement(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()

if __name__ == "__main__":
    main()