import pygame
import math
from GameEngine.settings import *
from PlayerAndEnemies.spritesheet import SpriteSheet

class Arrows(pygame.sprite.Sprite):
    def __init__(self, groups, pos, target, walls):
        
        # Sprite Setup

        super().__init__(groups)
        
        self.speed = 7
        self.walls = walls

        self.image = pygame.transform.scale(
            pygame.image.load("OtherAssets/ArrowSprite.png").convert_alpha(), (34, 10))

        # Calcatulating Direction and Repositioning

        self.rect = self.image.get_rect(center = pos)

        self.arrow_vec = pygame.math.Vector2(self.rect.center)
        self.target_vec = pygame.math.Vector2(target.rect.center)
        
        diff = (self.target_vec - self.arrow_vec)
        if diff.magnitude() > 0:
            self.direction = diff.normalize()
        else:
            self.direction = pygame.math.Vector2()

        angle = -math.degrees(math.atan2(diff[1], diff[0]))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def update(self):

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.kill()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

class FireBall(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.frame_index = 0
        self.scale = 0.5
        self.spritesheet = SpriteSheet("OtherAssets\\FireBallSpriteSheet.png")
        self.image = self.spritesheet.get_image(self.frame_index, 20,
                                                22, self.scale, (0, 0, 0))
        self.rect = self.image.get_rect(center = player.rect.center)
        
        self.time_started = pygame.time.get_ticks()
        self.animation_speed = 0.35
    
    def update_frame(self):
        self.frame_index += self.animation_speed
        self.scale += 0.4
        self.rect = self.image.get_rect(center = self.player.rect.center)
        self.image = self.spritesheet.get_image(int(self.frame_index), 20,
                                                22, self.scale, (0, 0, 0))
        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_started > 1000:
            self.player.fireball = None
            self.kill()

            self.player.attacking = False

        else:
            self.update_frame()