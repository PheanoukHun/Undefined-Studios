# Importing Libraries
import pygame
import math
import json
from GameEngine.settings import *
from PlayerAndEnemies.entity import Entity
from PlayerAndEnemies.spritesheet import SpriteSheet

# Enemy Classes
class Enemy(Entity):
    def __init__(self, monster_type, pos, groups, obstacle_sprites, damage_player, skeleton_shot):
        
        # Sprites Setup
        super().__init__(groups)
        self.monster_type = monster_type
        with open(f"MonsterAssets/{monster_type}/CharacterInfo.json") as file:
            self.data = json.load(file)
        self.sprite_type = "Mob"

        # Projectile Group
        self.arrows = pygame.sprite.Group()

        # Stats Variable
        self.speed = self.data["VEL"]
        self.hp = self.data["Health"]
        self.damage = self.data["AttackDamage"]
        self.resistance = self.data["Resistance"]
        
        # Notice and Attack Radius
        self.notice_radius = 750
        if self.monster_type == "Skeleton" :
            self.attack_radius = 500
        else:
            self.attack_radius = 60

        # Attack Variables
        self.can_attack = True
        self.attack_time = 0
        self.damage_player = damage_player
        self.skeleton_shot = skeleton_shot

        if self.monster_type != "Skeleton":
            self.cooldown_time = 400
        else:
            self.cooldown_time = 800

        # Vulnerability Variables
        self.invisibility_duration = 300
        self.vulnerable = True
        self.hit_time = None

        # States and Positioning
        self.previous_state = None
        self.state = "Idle"
        self.image = pygame.Surface((self.data["Width"], self.data["Height"]))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-30, -30)
        self.walls = obstacle_sprites

    # Enemy Animation
    def animate(self):

        #Loop over to next frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= self.data["AnimationSteps"]:
            if self.state == "Attack":
                self.frame_index = 0
            self.frame_index = 0

        # Set the Image
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.sprite_sheet = SpriteSheet(self.data[self.state])
            self.frame_index = 0

        # Image Size
        height = self.data["Height"]
        width = self.data["Width"]

        self.image = self.sprite_sheet.get_image(int(self.frame_index), width, height, 1, (0, 0, 0))

        #Flicker Logic
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # Player Tracking
    def get_player_distance_direction(self, player):

        # Finding Coordinate Differences
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        diff = (player_vec - enemy_vec)
        distance = diff.magnitude()

        # Finding the Direction
        if distance > 0:
            direction = diff.normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    # Change the State of the Mob
    def get_status(self, player):

        self.distance = self.get_player_distance_direction(player)[0]

        if self.distance <= self.attack_radius and self.can_attack:
            self.state = "Attack"
        elif self.distance <= self.notice_radius:
            self.state = "Move"
        else:
            self.state = "Idle"
    
    # Use the Mob's State to Perform Different Actions
    def actions(self, player):

        if self.state == 'Attack':
            self.attack_time = pygame.time.get_ticks()
            self.direction = pygame.math.Vector2()
            self.animation_speed = 0.15

            if self.monster_type != "Skeleton":
                if self.rect.colliderect(player.rect):
                    self.damage_player(self.damage)
                    self.can_attack = False
            else:
                if len(self.arrows) <= 4:
                    arrow = self.skeleton_shot(self.rect.center)
                    self.can_attack = False
                    self.arrows.add(arrow)

        elif self.state == "Move":
            self.direction = self.get_player_distance_direction(player)[1]
            self.animation_speed = 0.15
        else:
            self.direction = pygame.math.Vector2()
            self.animation_speed = 0

    # Cooldowns for Attack and Vulnerability Periods
    def cooldown(self):

        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time > self.cooldown_time:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time > self.invisibility_duration:
                self.vulnerable = True

    # The function used to Damage the Mob
    def get_damaged(self, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.hp -= player.damage
            self.check_death()

            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    # Function to Calculate the Knockback Value of the Mob
    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    # Checks for the Death Condition of the Mob
    def check_death(self):
        if self.hp < 0:
            self.player.score += 1
            self.kill()

    # Update the Mob
    def update(self):
        self.knockback()
        self.cooldown()
        self.animate()
        self.move(self.speed)
    
    # Update the Mob's Tracking for the Player
    def enemy_update(self, player):

        self.player = player
        if player.rect.x > self.rect.x:
            self.image = pygame.transform.flip(self.image.convert_alpha(), True, False)
        else:
            self.image = pygame.transform.flip(self.image.convert_alpha(), False, False)

        self.get_status(player)
        self.actions(player)