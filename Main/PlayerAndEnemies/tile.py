import pygame
from GameEngine.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, indexes):
        super().__init__(groups)
        self.sprite_type = "Wall"
        self.image = pygame.transform.scale(pygame.image.load(f"LevelEditor\LevelEditor-main/LevelEditor-main/img/tile/{indexes}.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -10)