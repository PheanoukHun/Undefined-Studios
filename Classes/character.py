import pygame
from sprite import AnimatedSprites

pygame.init()

class Player():
    def __init__(self, player_type, level, window):
        self.sprites = {}
        self.sprite = None
        self.health = 0
        self.attack_damage = 0
        self.state = "Idle"
        self.direction = "East"
        self.attack_key_pressed = False
        self.VEL = 0
        self.window = window
    
    def create_sprites(self):
        pass

    def handle_character_states(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.state = "Walking"
                self.direction = "North"
                self.sprite.y_speed = -self.VEL
            if event.key == pygame.K_s:
                self.state = "Walking"
                self.direction = "South"
                self.sprite.y_speed = self.VEL
            if event.key == pygame.K_a:
                self.state = "Walking"
                self.direction = "West"
                self.sprite.x_speed = -self.VEL
            if event.key == pygame.K_d:
                self.state = "Walking"
                self.direction = "East"
                self.sprite.x_speed = self.VEL

            if event.key == pygame.K_UP:
                self.state = "Slashing"
                self.direction = "North"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
            if event.key == pygame.K_DOWN:
                self.state = "Slashing"
                self.direction = "South"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
            if event.key == pygame.K_RIGHT:
                self.state = "Slashing"
                self.direction = "East"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
            if event.key == pygame.K_RIGHT:
                self.state = "Slashing"
                self.direction = "WEST"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
    


    def draw(self, keys_pressed):
        if self.state == "Idle":
            self.sprite.animation_speed = 999999999999999999999

        self.handle_character_states
        self.window.blit(self.sprite.sprite_image, (self.sprite.sprite_rect.x, self.sprite.sprite_rect.y))