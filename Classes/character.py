import pygame
import os
import json
from sprite import AnimatedSprites

pygame.init()

class Player():
    def __init__(self, player_type, window, screen_width, screen_height, x, y):
        with open(f"CharacterAssets\{player_type}\CharacterInfo.json") as json_file:
            self.data = json.load(json_file)
        
        self.x = x
        self.y = y
        
        self.health = self.data["Health"]
        self.attack_damage = self.data["AttackDamage"]
        self.state = "Idle"
        self.direction = "East"

        self.attack_key_pressed = False
        
        self.VEL = self.data[self.state]["VEL"]
        self.window = window

        self.window_width = screen_width
        self.window_height = screen_height
        
        self.sprite = AnimatedSprites(self.x, self.y, self.data[self.state]["Height"], self.data[self.state]["Width"], self.data[self.state][self.direction])
        self.update_sprite_actions()
    
    def update_sprite_actions(self):
        self.sprite = AnimatedSprites(self.x, self.y, self.data[self.state]["Height"], self.data[self.state]["Width"], self.data[self.state][self.direction])

    def update_info(self):
        self.VEL = self.data[self.state]["VEL"]
        self.sprite.image = self.sprites[self.state][self.direction]
        self.sprite.animation_speed = self.data[self.state]["AnimationSpeed"]

    def handle_character_states(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.state = "Walking"
                self.direction = "North"
                self.update_info()
                self.sprite.y_speed = self.VEL
            if event.key == pygame.K_s:
                self.state = "Walking"
                self.direction = "South"
                self.update_info()
                self.sprite.y_speed = -self.VEL
            if event.key == pygame.K_a:
                self.state = "Walking"
                self.direction = "West"
                self.update_info()
                self.sprite.x_speed = -self.VEL
            if event.key == pygame.K_d:
                self.state = "Walking"
                self.direction = "East"
                self.update_info()
                self.sprite.x_speed = self.VEL

            if event.key == pygame.K_UP and not self.attack_key_pressed:
                self.state = "Slashing"
                self.direction = "North"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
                self.attack_key_pressed = True
            if event.key == pygame.K_DOWN and not self.attack_key_pressed:
                self.state = "Slashing"
                self.direction = "South"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
                self.attack_key_pressed = True
            if event.key == pygame.K_LEFT and not self.attack_key_pressed:
                self.state = "Slashing"
                self.direction = "East"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
                self.attack_key_pressed = True
            if event.key == pygame.K_RIGHT and not self.attack_key_pressed:
                self.state = "Slashing"
                self.direction = "WEST"
                self.sprite.x_speed = 0
                self.sprite.y_speed = 0
                self.attack_key_pressed = True
    
    def draw(self, keys_pressed):
        self.handle_character_states(keys_pressed)
        self.window.blit(self.sprite.sprite_image, (self.sprite.sprite_rect.x, self.sprite.sprite_rect.y))