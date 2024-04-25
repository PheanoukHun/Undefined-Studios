import pygame
import json
from sprite import AnimatedSprite

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("test")

with open("CharacterAssets\Knight\CharacterInfo.json") as json_file:
    data = json.load(json_file)

running_sprite = AnimatedSprite(100, 100, 64, 64, data["Walking"]["East"], screen, 5, 250)
running_sprite.x_speed = 2
running_sprite.y_speed = 2

run = True
while run:

    if (running_sprite.y + running_sprite.height > 500) or (running_sprite.y < 0):
        running_sprite.y_speed *= -1
    
    if (running_sprite.x + running_sprite.width > 1000) or (running_sprite.x < 0):
        running_sprite.x_speed *= -1
        if running_sprite.x_speed < 0:
            running_sprite.change_spritesheet(data["Walking"]["West"][0])
        if running_sprite.x_speed > 0:
            running_sprite.change_spritesheet(data["Walking"]["East"][0])

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    running_sprite.draw()
    clock.tick(60)
    pygame.display.update()
pygame.quit()