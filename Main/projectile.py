import pygame
from settings import *

class ProjectilePlayer(pygame.sprite.Sprite):
    def __init__(self, groups, image, width, height):
        super().__init__(groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

class Projectile:
    def __init__(self):
        pass
    """def player_arrow(self, character, groups, mob):
        if len(character.projectiles) > 4:
            ProjectilePlayer(groups, "OtherAssets\ArrowSprite.png", 34, 6)"""

    """def flame(self, character, groups):
        if len(character.projectiles) > 4:
            pass"""

    def shield(self, character, groups):
        pass

    def mob_arrow(self, mob, player, groups):
        pass