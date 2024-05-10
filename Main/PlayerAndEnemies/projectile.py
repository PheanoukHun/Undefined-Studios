import pygame
import math
from GameEngine.settings import *

class ProjectilePlayer(pygame.sprite.Sprite):
    def __init__(self, groups, image, width, height, angle, pos, damage_player):

        self.damage_player = damage_player

        super().__init__(groups)
        angle_rotate = math.degrees(angle)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (width, height)), angle_rotate)
        self.rect = self.image.get_rect(midleft = pos)

        self.speed = 7
        self.x_speed = math.cos(angle) * self.speed
        self.y_speed = math.sin(angle) * self.speed
    
    def update(self):
        self.rect.move(self.x_speed, self.y_speed)

    def hit(self):
        self.damage_player(7)