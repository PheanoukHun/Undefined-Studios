import pygame
pygame.init()

class Wall(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()