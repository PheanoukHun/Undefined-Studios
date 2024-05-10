import pygame
import json
from PlayerAndEnemies.spritesheet import SpriteSheet
from GameEngine.settings import *
from PlayerAndEnemies.entity import Entity
from Weapons.shield import Shield

class Player(Entity):
    def __init__(self, position, groups, wall, player_type, create_attack, destroy_weapon):
        
        super().__init__(groups)
        self.player_type = player_type
        self.sprite_type = "Player"
        self.visible_sprite = groups[0]

        # Animation Data

        self.previous_state = None

        #Image and Rect

        self.image = pygame.transform.scale(pygame.image.load(f"CharacterAssets\{player_type}\{player_type}Single.png").convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-50, -30)

        # Obstacles

        self.walls = wall

        # Shield

        self.shield = None
        self.shield_cooldown = 5000
        self.shield_start = 0
        self.shield_down = False

        #Attacks

        self.attacking = False
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.shield_down = True
        self.shield_available = True

        # Damage Player

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #Graphics Setup

        self.state = "Down"
        self.import_player_assets()

    # Animation

    def animate(self):

        #loop over to next frame index

        self.frame_index += self.animation_speed
        if not self.attacking:
            if self.frame_index >= self.data["AnimationSteps"]:
                self.frame_index = 0
        else:
            if self.frame_index >= self.data["AttackAnimationSteps"]:
                self.frame_index = 0

        # Set the Image

        if self.state != self.previous_state:
            self.previous_state = self.state
            self.sprite_sheet = SpriteSheet(self.data[self.state])

        if self.attacking:
            height = self.data["AttackHeight"]
            width = self.data["AttackWidth"]
        else:
            height = self.data["Height"]
            width = self.data["Width"]

        self.image = self.sprite_sheet.get_image(int(self.frame_index), width, height, 1, (0, 0, 0))
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Flicker Logic

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # Import Player JSON

    def import_player_assets(self):
        with open(f"CharacterAssets/{self.player_type}/CharacterInfo.json") as file:
            self.data = json.load(file)

        self.hp = self.data["Health"]
        self.damage = self.data["AttackDamage"]
        self.speed = self.data["VEL"]

        if self.player_type == "Knight":
            self.attack_cooldown = 400
        elif self.player_type == "Ranger":
            self.attack_cooldown = 800
        else:
            self.attack_cooldown = 1200

    # Change Player Status

    def get_status(self):

        # Idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not "Idle" in self.state and not "Attack" in self.state:
                self.state = self.state + "_Idle"
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "Attack" in self.state:
                if "Idle" in self.state:
                    self.state = self.state.replace("Idle", "Attack")
                else:
                    self.state = self.state + "_Attack"
        else:
            if "Attack" in self.state:
                self.state = self.state.replace("_Attack", "")

    # Input Options

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            #Movement Input

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.state = "Up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.state = "Down"
            else:
                self.direction.y = 0
            
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.state = "Right"
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.state = "Left"
            else:
                self.direction.x = 0

            #Attack Input
            if keys[pygame.K_RALT]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                if self.player_type == "Knight":
                    self.create_attack()
                else:
                    self.shoot()
            
            # Shield Input
            if self.shield_available:
                if keys[pygame.K_RCTRL]:
                    self.shield = Shield(self)
                    self.shield_available = False
                    self.shield_start = pygame.time.get_ticks()
        
    # Attack Cooldown

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time > self.attack_cooldown:
                self.attacking = False
                self.destroy_weapon()
        if not self.vulnerable:
            if current_time - self.hurt_time > self.invulnerability_duration:
                self.vulnerable = True
        if self.shield_down:
            if current_time - self.shield_cooldown > 0:
                self.shield_available = True
                self.shield_down = False

    def update(self):

        self.animate()
        self.cooldown()
        self.input()
        self.get_status()
        self.move(self.speed)

        if self.shield != None:
            self.shield.update()
            self.shield_start = current_time
            self.shield = None
            self.shield_down = False
            self.shield_available = False
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_start > 5000:
                    self.shield_start = current_time
                    self.shield = None
                    self.shield_down = False
                    self.shield_available = False