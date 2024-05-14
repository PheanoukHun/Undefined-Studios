# Pygame Info and Libary Import
import pygame
from GameEngine.settings import *

# Medkit Class
class Medkit(pygame.sprite.Sprite):
    # Initialization Function
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.sprite_type = "Healing"
        self.image = pygame.transform.scale(
            pygame.image.load("OtherAssets/Tiles/19.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))