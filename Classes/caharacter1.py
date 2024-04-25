import pygame
import json
from sprite import AnimatedSprite, SpriteSheet, Sprite

class PlayerCharacter(AnimatedSprite):
    def __init__(self, x, y, width, height, animations, window):
        super().__init__(x, y, width, height, animations["Idle"]["North"][0], window, animations["Idle"]["AnimationSteps"], animations["Idle"]["AnimationSpeed"])
        self.animations = animations
        self.current_animation = "Idle"
        self.current_direction = "North"  # Start facing North
        self.vel = animations["Idle"]["VEL"]
        self.attack_damage = 5
        self.health = 25

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.sprite_rect.x - self.vel >= 0:
            self.x_speed = -self.vel
            self.current_direction = "West"
            self.current_animation = "Walking"
        elif keys_pressed[pygame.K_d] and self.sprite_rect.x + self.vel + self.width < _width:
            self.x_speed = self.vel
            self.current_direction = "East"
            self.current_animation = "Walking"
        else:
            self.x_speed = 0

        if keys_pressed[pygame.K_w] and self.sprite_rect.y - self.vel > 0:
            self.y_speed = -self.vel
            self.current_direction = "North"
            self.current_animation = "Walking"
        elif keys_pressed[pygame.K_s] and self.sprite_rect.y + self.vel + self.height < _height:
            self.y_speed = self.vel
            self.current_direction = "South"
            self.current_animation = "Walking"
        else:
            self.y_speed = 0

        if keys_pressed[pygame.K_UP]:
            self.current_animation = "Attack"
            self.current_direction = "North"
            # Handle attack logic here
        elif keys_pressed[pygame.K_DOWN]:
            self.current_animation = "Attack"
            self.current_direction = "South"
            # Handle attack logic here
        elif keys_pressed[pygame.K_LEFT]:
            self.current_animation = "Attack"
            self.current_direction = "West"
            # Handle attack logic here
        elif keys_pressed[pygame.K_RIGHT]:
            self.current_animation = "Attack"
            self.current_direction = "East"
            # Handle attack logic here

        if not any(keys_pressed):
            self.current_animation = "Idle"

    def update_animation(self):
        animation_data = self.animations[self.current_animation]
        self.frame = animation_data["AnimationSteps"]
        self.animation_time = animation_data["AnimationSpeed"]
        self.sprite_sheet = SpriteSheet(animation_data[self.current_direction][0])

    def update(self, keys_pressed):
        self.handle_movement(keys_pressed)
        self.update_animation()
        super().update()

    def draw(self):
        super().draw()

if __name__ == "__main__":
    # Inside your main loop

    pygame.init()
    
    _width, _height = (1018,573)
    
    _clock = pygame.time.Clock()
    _window = pygame.display.set_mode((_width, _height))

    with open("CharacterAssets\Knight\CharacterInfo.json") as json_file:
        animation_data = json.load(json_file)

    _FPS = 30
    _player_character = PlayerCharacter(100, 100, 64, 64, animation_data, _window)

    def _draw_window(character):
        _window.fill((0, 0, 255))  # Fill window with blue color
        character.draw()  # Draw the player character
        pygame.display.update()  # Update the display

    _run = True
    while _run:
        _clock.tick(_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False

        _keys_pressed = pygame.key.get_pressed()
        _player_character.update(_keys_pressed)  # Pass keys_pressed argument here
        _draw_window(_player_character)

        
    pygame.quit()
