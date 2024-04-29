import pygame
import json
import random
import math
from sprite import AnimatedSprite, Sprite

HIT_USER = pygame.USEREVENT + 1
HIT_MONSTER = pygame.USEREVENT + 3

pygame.init()

class Entity(): 
    def __init__(self, data, window, screen_width, screen_height, x, y):
        
        self.data = data

        self.speed_x = 0
        self.speed_y = 0

        self.death = True

        self.health = self.data["Health"]
        self.attack_damage = self.data["AttackDamage"]
        self.resistance = 0
        self.attacked = False
        
        self.previous_state = "Idle"
        self.previous_direction = "North"
        
        self.state = "Walking"
        self.direction = "East"
        
        self.image = self.data[self.state][self.direction]
        self.width = self.data[self.state]["Width"]
        self.height = self.data[self.state]["Height"]
        self.frame = self.data[self.state]["AnimationSteps"]

        self.attack_key_pressed = False
        self.attack_animation_time = data["Attack"]["AnimationSteps"] * data["Attack"]["AnimationSpeed"]
        self.last_attack_animation_start = 0

        self.hurt_animation_length = data["Hurt"]["AnimationSteps"] * data["Hurt"]["AnimationSpeed"]
        self.death = False
        
        self.VEL = self.data["VEL"]
        self.window = window

        self.window_width = screen_width
        self.window_height = screen_height

        self.projectiles = pygame.sprite.Group()
        self.resistance = random.randint(0,2)

        self.sprite = AnimatedSprite(x, y, self.width, self.height, self.data[self.state][self.direction], self.window, self.frame, self.data[self.state]["AnimationSpeed"])

    @property
    def states(self):
        return self.state
    @states.setter
    def states(self, value):
        self.previous_state = self.state
        self.state = value

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

    def shoot(self, angle, image = "OtherAssets\\ArrowSprite.png"):

        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack_animation_start > self.attack_animation_time:
            if self.direction == "North":
                arrow = Projectile(self.sprite.x + self.width // 2, self.sprite.y + 10, angle, self.window, image)
            if self.direction == "South":
                arrow = Projectile(self.sprite.x + self.width // 2, self.sprite.y + self.height + 10, angle, self.window, image)

            if self.direction == "West":
                arrow = Projectile(self.sprite.x + 10, self.sprite.y + self.height // 2 , angle, self.window, image)
            if self.direction == "East":
                arrow = Projectile(self.sprite.x + 10 + self.width, self.sprite.y + self.height // 2 , angle, self.window, image)
            
            self.projectiles.add(arrow)
            self.last_attack_animation_start = current_time

    def update_info(self):
        self.image = self.data[self.state][self.direction]
        self.frame = self.data[self.state]["AnimationSteps"]
        self.animation_time = self.data[self.state]["AnimationSpeed"]
        self.update_sprite_actions()

    def update_sprite_actions(self):

        x = self.sprite.x
        y = self.sprite.y

        self.width = self.data[self.state]["Width"]
        self.height = self.data[self.state]["Height"]
        
        self.sprite = AnimatedSprite(x, y, self.width, self.height, self.image, self.window, self.frame, self.animation_time)
        self.x_speed = self.speed_x
        self.y_speed = self.speed_y

    def hurt(self, damage_amount):
        
        reduced = int(damage_amount * (1/self.resistance))
        self.health -= damage_amount - reduced

        if self.health <= 0:
            self.state = "Hurt"
            self.death = True
            self.hurt_animation_start = pygame.time.get_ticks()

    def draw(self):
        if self.death:
            self.update_info()
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_animation_start > self.hurt_animation_length:
                return True
        self.sprite.draw()
        return False

class Player(Entity):

    def __init__(self, player_type, window, screen_width, screen_height, x, y):
        
        with open(f"CharacterAssets\\{player_type}\\CharacterInfo.json") as json_file:
            data = json.load(json_file)
        
        super().__init__(data, window, screen_width, screen_height, x, y)
        
        self.last_shield_ended = -10000
        self.shield = None

        self.player_type = player_type

        if player_type == "Knight":
            self.resistance = 3
        elif player_type == "Ranger":
            self.resistance = 2
        else:
            self.resistance = 1

    def create_shield(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shield_ended > 10000:
            self.last_shield_ended = current_time
            self.shield = Shield(self.sprite.x, self.sprite.y, self, self.window)

    def handle_character_states(self, keys_pressed, monsters = []):

        if keys_pressed[pygame.K_RCTRL] and not self.state == "Attack":
            self.create_shield()

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
        
        if not self.attacked:
            if keys_pressed[pygame.K_UP]:
                self.state = "Attack"
                self.direction = "North"
                
            elif keys_pressed[pygame.K_DOWN]:
                self.state = "Attack"
                self.direction = "South"
                
            elif keys_pressed[pygame.K_LEFT]:
                self.state = "Attack"
                self.direction = "West"
                
            elif keys_pressed[pygame.K_RIGHT]:
                self.state = "Attack"
                self.direction = "East"
            
        
        if not any(keys_pressed):
            self.state = "Idle"
        
        if self.player_type == "Knight":
            if self.state == "Attack":
                self.y_speed = 0
                self.x_speed = 0

        if self.state == "Attack":
            self.attack()

        if self.state != self.previous_state or self.previous_direction != self.direction:
            self.previous_state = self.state
            self.previous_direction = self.direction
            self.update_info()
    
    def attack(self, monster_list = []):

        if self.player_type == "Ranger":
            if len(monster_list) != 0:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_animation_start > self.attack_animation_time:
                    for monster in monster_list:
                        if monster.distance < 250:

                            y_difference = self.sprite.y - monster.sprite.y
                            x_difference = self.sprite.x - monster.sprite.x
                            angle = math.atan2(y_difference, x_difference)
                            self.shoot(angle)

                        else:
                            if self.direction == "North":
                                self.shoot(90)
                            if self.direction == "South":
                                self.shoot(270)
                            if self.direction == "West":
                                self.shoot(180)
                            else:
                                self.shoot(0)

        elif self.player_type == "Wizard":
            current_time = pygame.time.get_ticks() - 1500
            if current_time - self.last_attack_animation_start > self.attack_animation_time:
                if len(monster_list) != 0:
                    for monster in monster_list:
                        if monster.distance < 300:

                            y_difference = self.sprite.y - monster.sprite.y
                            x_difference = self.sprite.x - monster.sprite.x
                            angle = math.atan2(y_difference, x_difference)
                            self.shoot(angle, "OtherAssets\\FireBall.png")

                        else:
                            if self.direction == "North":
                                self.shoot(90, "OtherAssets\\FireBall.png")
                            if self.direction == "South":
                                self.shoot(270, "OtherAssets\\FireBall.png")
                            if self.direction == "West":
                                self.shoot(180, "OtherAssets\\FireBall.png")
                            else:
                                self.shoot(0, "OtherAssets\\FireBall.png")
        
        else:
            if len(monster_list) != 0:
                if self.sprite.sprite_rect.collidelist(monster_list):
                    monster = monster_list[self.sprite.sprite_rect.collidelist(monster_list)]
                    if self.sprite.collide_with(monster):
                        if self.state == "North":
                            if monster.sprite.y < self.sprite.y:
                                monster.hurt(self.attack_damage)
                        if self.state == "West":
                            if monster.sprite.x < self.sprite.x:
                                monster.hurt(self.attack_damage)
                        if self.state == "East":
                            if monster.sprite.x > self.sprite.x:
                                monster.hurt(self.attack_damage)
                        else:
                            if monster.sprite.y > self.sprite.y:
                                monster.hurt(self.attack_damage)

    def hurt(self, damage_amount):

        if self.shield == None:
            reduced = int(damage_amount * (1/self.resistance))
            self.health -= damage_amount - reduced
        else:
            self.shield.shield_started -= 1000

        if self.health <= 0:
            self.state = "Hurt"
            self.death = True
            self.hurt_animation_start = pygame.time.get_ticks()

    def draw(self, event, mob_group = []):

        self.handle_character_states(event)
        if len(self.projectiles) > 0:
            for projectile in self.projectiles:
                for mob in mob_group:
                    hit_mob, hit_player, hit_wall = projectile.hit(mob)
                    if hit_mob:
                        if self.player_type == "Ranger":
                            mob.hurt(8)
                        if self.player_type == "Wizard":
                            mob.hurt(10)
                if hit_mob or hit_wall:
                    projectile.kill()

        if self.shield != None:
            self.shield.update()
            if self.shield.is_shield_deactived() or self.state == "Attack":
                self.shield = None
            else:
                self.window.blit(self.shield.sprite_image, self.shield.sprite_rect.topleft)
        
        death = super().draw()
        return death

class Shield(Sprite):
    def __init__(self, x,  y, character, window):
        super().__init__(x, y, "OtherAssets\\AuraShield.png", window)
        
        self.shield_started = pygame.time.get_ticks()
        self.sprite_image = pygame.transform.scale(self.sprite_image, (character.sprite.width + 10, character.sprite.height + 10))
        
        self.sprite_rect = self.sprite_image.get_rect(topleft=(character.sprite.x, character.sprite.y))
        self.character = character
    
    def is_shield_deactived(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.shield_started > 5000:
            return True
        
        return False
    
    def update(self):

        is_inactive = self.is_shield_deactived()
        
        self.flip_x = not self.flip_x
        self.flip_y = not self.flip_y
        
        self.update_transform()

        self.x = self.character.sprite.x - 10
        self.y = self.character.sprite.y - 5

        return is_inactive

class Projectile(Sprite):
    def __init__(self, x, y, angle, window, image = "OtherAssets\\ArrowSprite.png"):

        self._projectile_angle = math.radians(angle)
        self.speed = 15
        
        super().__init__(x, y, image, window)
        self.rotate = angle
        self.scale = 0.15

        self.x_speed = self.speed * math.cos(angle)
        self.y_speed = self.speed * math.sin(angle)

        if angle == 0 or angle == 180:
            self.y_speed = 0
        elif 0 < angle < 180:
            self.y_speed *= -1
        else:
            self.y_speed *= 1
        
        if angle == 90 or angle == 270:
            self.y_speed = 0
        elif 90 < angle < 270:
            self.y_speed *= -1
        elif 0 < angle < 90 or 270 < angle < 360:
            self.y_speed *= 1
    
    def hit(self, other_character):

        hit_mob, hit_player, hit_wall = (False, False, False)

        if self.collide_with(other_character):
            if isinstance(other_character, Mob):
                hit_mob = True
            if isinstance(other_character, Player):
                hit_player = True
            if isinstance(other_character, Sprite):
                hit_wall = True
                self.x_speed = 0
                self.y_speed = 0
        
        return (hit_mob, hit_player, hit_wall)
        
class Mob(Entity):

    def __init__(self, monster_type, window, screen_width, screen_height, x, y, player):

        with open(f"MonsterAssets\\{monster_type}\\CharacterInfo.json") as json_file:
            data = json.load(json_file)
        
        self.attack_animation_time = data["Attack"]["AnimationSteps"] * data["Attack"]["AnimationSpeed"]
        self.last_attack_animation_start = 0

        self.player = player
        self.creature = monster_type
        
        self.last_state_change_time = pygame.time.get_ticks()
        self.state_change_time = data["Change"]
        self.player_tracked = False

        self.distance = 1000

        super().__init__(data, window, screen_width, screen_height, x, y, player)

    def handle_character_states(self):
        states = ["Walking", "Idle"]
        directions = ["North", "West", "East", "South"]

        self.previous_state = self.direction
        self.previous_state = self.state

        self.state = random.choice(states)
        self.direction = random.choice(directions)

        if self.state == "Walking":
            if self.direction == "West":
                self.x_speed = -self.VEL
            if self.direction == "East":
                self.x_speed = self.VEL
        else:
            self.x_speed = 0

        if self.state == "Walking":
            if self.direction == "North":
                self.y_speed = -self.VEL
            if self.direction == "South":
                self.y_speed = self.VEL
        else:
            self.y_speed = 0

        self.update_info()

    def track_player(self):

        x_difference = self.sprite.x - self.player.sprite.x
        y_difference = self.sprite.y - self.player.sprite.y

        self.distance = int(math.sqrt(x_difference ** 2 + y_difference ** 2))
        character_diagonal = int(math.sqrt(self.width ** 2 + self.height ** 2))
        angle = math.degrees(math.atan2(y_difference, x_difference))

        if angle < 0:
            angle += 360

        if self.distance < 450:
            self.player_tracked = True
            if self.creature != "Skeleton":
                if self.distance > character_diagonal + 10:
                    self.state = "Walking"
                    if y_difference < -5:
                        self.y_speed = self.VEL
                    if y_difference > 5:
                        self.y_speed = -self.VEL
                    else:
                        self.y_speed = 0
                    
                    if x_difference < -5:
                        self.x_speed = self.VEL
                        self.direction = "East"
                    if y_difference > 5:
                        self.x_speed = -self.VEL
                        self.direction = "West"
                    else:
                        self.x_speed = 0
            
                if self.distance < character_diagonal + 10:
                    self.state = "Attack"
                    
                    if 45 <= angle <= 135:
                        self.direction = "North"
                    elif 225 <= angle <= 315:
                        self.direction = "South"
                    elif 135 <= angle <= 225:
                        self.direction = "West"
                    else:
                        self.direction = "East"
            else:
                if self.distance < 150:
                    self.state = "Attack"
                    if 45 <= angle <= 135:
                        self.direction = "North"
                    elif 225 <= angle <= 315:
                        self.direction = "South"
                    elif 135 <= angle <= 225:
                        self.direction = "West"
                    else:
                        self.direction = "East"
                    
                    if len(self.projectiles) > 2:
                        self.shoot(angle)

        if self.state != self.previous_state or self.previous_direction != self.direction:
            self.previous_state = self.state
            self.previous_direction = self.direction
            self.update_info()

    def draw(self):
        self.track_player()
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_state_change_time > self.state_change_time) and not self.player_tracked:
            self.handle_character_states()

        super().draw()

if __name__ == "__main__":
    _screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Test")
    _clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    _player_character = Player("Knight", _screen, 1000, 750, 100, 100)
    _arrow = Projectile(100, 500, 45, _screen)

    #_slime = Mob("Slime", _screen, 1000, 750, 533, 195, _player_character)
    #_skeleton = Mob("Skeleton", _screen, 1000, 750, 533, 195, _player_character)
    #_zombie = Mob("Zombie", _screen, 1000, 750, 533, 195, _player_character)

    _run = True
    while _run:
        
        _screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False

        _keys_pressed = pygame.key.get_pressed()
        _player_character.draw(_keys_pressed)
        #_slime.draw()

        _arrow.draw()
        pygame.display.update()
        _clock.tick(60)
    pygame.quit()
