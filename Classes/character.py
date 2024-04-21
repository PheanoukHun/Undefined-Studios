import pygame
from sprite import AnimatedSprites

class Player():
    def __init__(self, player_type, level):
        self.sprites = {}
        self.health = 0
        self.attack_damage = 0
        