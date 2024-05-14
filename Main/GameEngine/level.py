
# Importing the Libraries and Modules
import pygame
import random
from GameEngine.settings import *
from PlayerAndEnemies.tile import Tile
from PlayerAndEnemies.player import Player
from Weapons.weapon import Slash, Shield
from Weapons.ranged import FireBall, Arrows
from Weapons.medkit import Medkit
from Utilities.ui import UI
from PlayerAndEnemies.enemy import Enemy
from Utilities.camera import YSortCameraGroup
from Utilities.debug import debug

# Level Class
class Level:

    # Initiatization Function
    def __init__(self, levelnum = 1, player_character = "Knight"):

        # Miscilaneous Data
        self.screen = pygame.display.get_surface()
        self.world_data = read_world_data(levelnum)
        self.player_type = player_character
        
        # Sprite Groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.healing_sprites = pygame.sprite.Group()
        
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.enemy_attack_sprites = pygame.sprite.Group()

        # HealthBar Setup
        self.ui = UI()

        #Attacks
        self.current_attack = None

        # Create the Maps
        self.create_map()
    
    # Checks to see the player's attacks are Connecting with Mobs
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collided_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collided_sprites:
                    for target_sprite in collided_sprites:
                        target_sprite.get_damaged(self.player)

    # Function to Damage the Player
    def damage_player(self, amount):
        if self.player.vulnerable:
            if self.player.shield != None:
                if amount - 5 < 0:
                    amount = 0
                else:
                    amount -= 5
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    # Create the Slash Attack
    def create_attack(self):
        self.current_attack = Slash(self.player, [self.visible_sprites, self.attack_sprites])

    # Create the Fireball Attack
    def create_fireball(self):
        self.current_attack = FireBall(self.player, [self.visible_sprites, self.attack_sprites])

    # Create the Player's Arrow Attack
    def player_arrow(self, pos):

        distance_sorted_list = []
        for sprite in sorted(self.attackable_sprites, key = lambda sprite: sprite.distance):
            distance_sorted_list.append(sprite)

        arrow = Arrows([self.visible_sprites, self.attack_sprites], pos, distance_sorted_list[0], self.obstacle_sprites)
        return arrow

    # Checks to See if the Player is colliding with a healthblock or not
    def player_heal_logic(self):
        if self.healing_sprites:
            collided_sprites = pygame.sprite.spritecollide(self.player, self.healing_sprites, False)
            if collided_sprites:
                for health_block in collided_sprites:
                    self.player.hp = self.player.data["Health"]
                    health_block.kill()

    # Create the Mob's Arrow Attack
    def mob_arrow(self, pos):
        arrow = Arrows([self.visible_sprites, self.enemy_attack_sprites], pos, self.player, self.obstacle_sprites)
        return arrow

    # Create the Player's shield
    def shield(self):
        shield = Shield(self.player, [self.visible_sprites])
        return shield
    
    # Destroy the Slash Attack
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # Checks to See if the Skeleton's arrow are colliding with the player
    def mob_attack_logic(self):
        if self.enemy_attack_sprites:
            for attack_sprite in self.enemy_attack_sprites:
                if attack_sprite.rect.colliderect(self.player.rect):
                    collided_sprites = pygame.sprite.spritecollide(self.player, self.enemy_attack_sprites, False)
                    if collided_sprites:
                        for target_sprite in collided_sprites:
                            self.damage_player(5)
                            attack_sprite.kill()

    # Create the Maps for the Level to Include Tiles, Players, Enemy, and Boss.
    def create_map(self):
        for yi, row in enumerate(self.world_data):
            for xi, col in enumerate(row):
                x = xi * TILE_SIZE
                y = yi * TILE_SIZE

                if int(col) >= 0 and int(col) != 15 and int(col) != 16 and int(col) != 19 and int(col) != 11:
                    Tile((x,y), [self.obstacle_sprites, self.visible_sprites], int(col))
                if int(col) == 19:
                    Medkit(x, y, [self.visible_sprites, self.healing_sprites])
                if int(col) == 11:
                    Enemy("Cyclops", (x, y), [self.visible_sprites, self.attackable_sprites],
                        self.obstacle_sprites, self.damage_player, self.mob_arrow)
                if int(col) == 16:
                    monster_types = ["Zombie", "Skeleton", "Slime"]
                    Enemy(random.choice(monster_types), (x, y), [self.visible_sprites, self.attackable_sprites]
                        , self.obstacle_sprites, self.damage_player, self.mob_arrow)
                if int(col) == 15:
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                        self.player_type, self.create_attack,
                                        self.destroy_weapon, self.shield,
                                        self.create_fireball, self.player_arrow)
    
    # Displays the Level
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.mob_attack_logic()
        self.player_heal_logic()
        self.ui.display(self.player)