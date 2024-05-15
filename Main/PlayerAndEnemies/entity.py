# Importing the Libraries
import pygame
import math

# Entity Class
class Entity(pygame.sprite.Sprite):
    # Initialization Function
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.data = None
        self.projectiles = pygame.sprite.Group()
        self.direction = pygame.math.Vector2()
    
    # Scales up the image
    def scale(self, value):
        width = self.data["Width"] * value
        height = self.data["Height"] * value

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center = self.rect.center)

    # Gets the collision condition for the direction
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.walls:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
        if direction == "vertical":
            for sprite in self.walls:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    # Checks to see if the alpha value is 255 or 0
    def wave_value(self):
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    # Moves the Entity sprite based on the speed and direction
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center