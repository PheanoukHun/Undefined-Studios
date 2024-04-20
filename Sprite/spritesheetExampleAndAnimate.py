import pygame
from spritesheet import SpriteSheet

WIDTH = 1000
HEIGHT = 500
BG = (50, 50, 50)
BLACK = (0, 0, 0)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spritesheet")

sprite_sheet_image = pygame.image.load("CharacterAssets\Knight\KnightWalkingRight.png").convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

animation_step = 8
animation_time = 200
last_update = pygame.time.get_ticks()
frame = 0
animation_list = [sprite_sheet.get_image(i, 64, 64, 2, BLACK) for i in range(animation_step)]

run = True
while run:

    current_time = pygame.time.get_ticks()
    if current_time - last_update > animation_time:
        last_update = pygame.time.get_ticks()
        frame = (frame + 1) % animation_step

    screen.fill(BG)
    screen.blit(animation_list[frame], (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()