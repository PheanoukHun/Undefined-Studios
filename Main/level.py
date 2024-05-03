import pygame
import random
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from shield import Shield
from enemy import Enemy
from projectile import Projectile

class Level:
    def __init__(self, levelnum = 1):

        self.screen = pygame.display.get_surface()
        self.world_data = read_world_data(levelnum)
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.ui = UI()
        self.projectiles = Projectile()

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
            print(self.player.hp)
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
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General Setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_height = self.screen.get_size()[0] // 2
        self.half_width = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.background = pygame.transform.scale(pygame.image.load("Background\StoneBackground.png").convert(), (5000, 5000))
        self.background_rect = self.background.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.background_rect.topleft - self.offset
        self.screen.blit(self.background, floor_offset_pos)

        for sprite in self.sprites():
            offset_position = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_position)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "Mob"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

