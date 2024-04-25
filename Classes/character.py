import pygame
import os
import json
from sprite import AnimatedSprite

pygame.init()

class Player():
    def __init__(self, player_type, window, screen_width, screen_height, x, y):
        with open(f"CharacterAssets\{player_type}\CharacterInfo.json") as json_file:
            self.data = json.load(json_file)

        self.speed_x = 0
        self.speed_y = 0

        self.health = self.data["Health"]
        self.attack_damage = self.data["AttackDamage"]
        self.state = "Walking"
        self.direction = "East"
        
        self.image = self.data[self.state][self.direction]
        self.width = self.data[self.state]["Width"]
        self.height = self.data[self.state]["Height"]
        self.frame = self.data[self.state]["AnimationSteps"]

        self.attack_key_pressed = False
        
        self.VEL = self.data[self.state]["VEL"]
        self.window = window

        self.window_width = screen_width
        self.window_height = screen_height
        

        self.sprite = AnimatedSprite(x, y, self.width, self.height, self.data[self.state][self.direction], self.window, self.frame, self.data[self.state]["AnimationSpeed"])

    @property
    def x_speed(self):
        return self.sprite.speed_y
    @x_speed.setter
    def x_speed(self, value):
        self.sprite.speed_x = value
        self.speed_x = value

    @property
    def y_speed(self):
        return self.sprite.speed_y
    @y_speed.setter
    def y_speed(self, value):
        self.sprite.speed_y = value
        self.speed_y = value

    def update_sprite_actions(self):

        x = self.sprite.x
        y = self.sprite.y

        if self.state == "Attack":
            if self.direction == "West" or self.direction == "East":
                self.height = self.data[self.state]["Width"]
                self.width = self.data[self.state]["Height"]
            else:
                self.width = self.data[self.state]["Width"]
                self.height = self.data[self.state]["Height"]
        else:
            self.width = self.data[self.state]["Width"]
            self.height = self.data[self.state]["Height"]
        
        self.sprite = AnimatedSprite(x, y, self.width, self.height, self.image, self.window, self.frame, self.animation_time)
        self.x_speed = self.speed_x
        self.y_speed = self.speed_y

    def update_info(self):
        self.image = self.data[self.state][self.direction]
        self.VEL = self.data[self.state]["VEL"]
        self.frame = self.data[self.state]["AnimationSteps"]
        self.animation_time = self.data[self.state]["AnimationSpeed"]
        self.update_sprite_actions()

    def handle_character_states(self, keys_pressed):

        if keys_pressed[pygame.K_a] and self.sprite.sprite_rect.x - self.VEL >= 0:
            self.x_speed = -self.VEL
            self.direction = "West"
            self.state = "Walking"
        elif keys_pressed[pygame.K_d] and self.sprite.sprite_rect.x + self.VEL + self.width < self.window_width:
            self.x_speed = self.VEL
            self.direction = "East"
            self.state = "Walking"
        else:
            self.x_speed = 0

        if keys_pressed[pygame.K_w] and self.sprite.sprite_rect.y - self.VEL > 0:
            self.y_speed = -self.VEL
            self.direction = "North"
            self.state = "Walking"
        elif keys_pressed[pygame.K_s] and self.sprite.sprite_rect.y + self.VEL + self.height < self.window_height:
            self.y_speed = self.VEL
            self.direction = "South"
            self.state = "Walking"
        else:
            self.y_speed = 0

        if keys_pressed[pygame.K_UP]:
            self.state = "Attack"
            self.direction = "North"
            # Handle attack logic here
        elif keys_pressed[pygame.K_DOWN]:
            self.state = "Attack"
            self.direction = "South"
            # Handle attack logic here
        elif keys_pressed[pygame.K_LEFT]:
            self.state = "Attack"
            self.direction = "West"
            # Handle attack logic here
        elif keys_pressed[pygame.K_RIGHT]:
            self.state = "Attack"
            self.direction = "East"
            # Handle attack logic here

        if not any(keys_pressed):
            self.state = "Idle"
        self.update_info()
        #self.x_speed = self.VEL * directions[self.direction][0]
        #self.y_speed = self.VEL * directions[self.direction][1]
    
    def draw(self, event):
        self.handle_character_states(event)
        self.sprite.draw()

if __name__ == "__main__":
    _screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Test")
    _clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    _player_character = Player("Knight", _screen, 1000, 750, 100, 100)

    _run = True
    while _run:
        
        _screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False

        _keys_pressed = pygame.key.get_pressed()
        _player_character.draw(_keys_pressed)
        pygame.display.update()
        _clock.tick(60)
    pygame.quit()
