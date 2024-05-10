import pygame
import random
from GameEngine.settings import *
from PlayerAndEnemies.tile import Tile
from PlayerAndEnemies.player import Player
from Weapons.weapon import Weapon
from Utilities.ui import UI
from Weapons.shield import Shield
from PlayerAndEnemies.enemy import Enemy
from Utilities.camera import YSortCameraGroup

class Level:
    def __init__(self, levelnum = 1, player_character = "Knight"):

        self.screen = pygame.display.get_surface()
        self.world_data = read_world_data(levelnum)
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.enemy_attack_sprites = pygame.sprite.Group()

        self.ui = UI()

        #Attacks
        self.current_attack = None

        self.create_map()
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collided_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collided_sprites:
                    for target_sprite in collided_sprites:
                        target_sprite.get_damaged(self.player)

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    """def player_shoot(self):
        if self.player.player_type == "Wizard":
            self.projectiles.flame(self.player, [self.attack_sprites, self.player.projectiles])
        if self.player.player_type == "Ranger":
            self.projectiles.arrow(self.player, [self.attack_sprites])
"""
    
    def shield(self):
        Shield(self.player.rect.x, self.player.rect.y, self.player, pygame.display.get_surface())
    
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def mob_attack_logic(self):
        if self.enemy_attack_sprites:
            for attack_sprite in self.enemy_attack_sprites:
                if attack_sprite.rect.colliderect(self.player.rect):
                    collided_sprites = pygame.sprite.spritecollide(attack_sprite.rect, self.player.rect)
                    if collided_sprites:
                        for target_sprite in collided_sprites:
                            attack_sprite.hit()
                            attack_sprite.kill()

    def create_map(self):
        for yi, row in enumerate(self.world_data):
            for xi, col in enumerate(row):
                x = xi * TILE_SIZE
                y = yi * TILE_SIZE

                if int(col) >= 0 and int(col) != 15 and int(col) != 16:
                    Tile((x,y), [self.obstacle_sprites, self.visible_sprites], int(col))
                if int(col) == 16:
                    monster_types = ["Zombie", "Skeleton", "Slime"]
                    Enemy(random.choice(monster_types), (x, y), [self.visible_sprites, self.attackable_sprites]
                        , self.obstacle_sprites, self.damage_player)
                if int(col) == 15:
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                        "Knight", self.create_attack, self.destroy_weapon)
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player, [self.enemy_attack_sprites])
        self.player_attack_logic()
        self.mob_attack_logic()
        self.ui.display(self.player)