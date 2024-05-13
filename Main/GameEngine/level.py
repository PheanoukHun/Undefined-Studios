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

class Level:

    def __init__(self, levelnum = 1, player_character = "Knight"):

        self.screen = pygame.display.get_surface()
        self.world_data = read_world_data(levelnum)
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.healing_sprites = pygame.sprite.Group()
        
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.enemy_attack_sprites = pygame.sprite.Group()

        self.ui = UI()
        self.player_type = player_character

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
            if self.player.shield != None:
                if amount - 5 < 0:
                    amount = 0
                else:
                    amount -= 5
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def create_attack(self):
        self.current_attack = Slash(self.player, [self.visible_sprites, self.attack_sprites])

    def create_fireball(self):
        self.current_attack = FireBall(self.player, [self.visible_sprites, self.attack_sprites])

    def player_arrow(self, pos):

        distance_sorted_list = []
        for sprite in sorted(self.attackable_sprites, key = lambda sprite: sprite.distance):
            distance_sorted_list.append(sprite)

        arrow = Arrows([self.visible_sprites, self.attack_sprites], pos, distance_sorted_list[0], self.obstacle_sprites)
        return arrow

    def player_heal_logic(self):
        if self.healing_sprites:
            for health_block in self.healing_sprites:
                if self.player.rect.colliderect(health_block.rect):
                    self.player.hp = self.player.data["Health"]
                    health_block.kill()

    def mob_arrow(self, pos):
        arrow = Arrows([self.visible_sprites, self.enemy_attack_sprites], pos, self.player, self.obstacle_sprites)
        return arrow

    def shield(self):
        shield = Shield(self.player, [self.visible_sprites])
        return shield
    
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def mob_attack_logic(self):
        if self.enemy_attack_sprites:
            for attack_sprite in self.enemy_attack_sprites:
                if attack_sprite.rect.colliderect(self.player.rect):
                    collided_sprites = pygame.sprite.spritecollide(self.player, self.enemy_attack_sprites, False)
                    if collided_sprites:
                        for target_sprite in collided_sprites:
                            self.damage_player(5)
                            attack_sprite.kill()

    def create_map(self):
        for yi, row in enumerate(self.world_data):
            for xi, col in enumerate(row):
                x = xi * TILE_SIZE
                y = yi * TILE_SIZE

                if int(col) >= 0 and int(col) != 15 and int(col) != 16 and int(col) != 19:
                    Tile((x,y), [self.obstacle_sprites, self.visible_sprites], int(col))
                if int(col) == 19:
                    Medkit(x, y, [self.visible_sprites, self.healing_sprites])
                if int(col) == 16:
                    monster_types = ["Zombie", "Skeleton", "Slime"]
                    Enemy(random.choice(monster_types), (x, y), [self.visible_sprites, self.attackable_sprites]
                        , self.obstacle_sprites, self.damage_player, self.mob_arrow)
                if int(col) == 15:
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                        self.player_type, self.create_attack,
                                        self.destroy_weapon, self.shield,
                                        self.create_fireball, self.player_arrow)
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.mob_attack_logic()
        self.ui.display(self.player)