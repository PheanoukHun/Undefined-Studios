import pygame

class Slash(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = "Melee"
        direction = player.state.split("_")[0]

        #graphic
        if direction == "Left" or direction == "Right":
            self.image = pygame.Surface((120, player.image.get_height())).convert_alpha()
        elif direction == "Up" or direction == "Down":
            width = player.image.get_width()
            if width - 100 < 0:
                width = 64
            else:
                width -= 100
            self.image = pygame.Surface((player.image.get_width(), 60)).convert_alpha()
        
        self.image.set_colorkey((0, 0, 0))

        #Placement
        if direction == "Left":
            self.rect = self.image.get_rect(topright = player.rect.topleft + pygame.math.Vector2(100, 0))
        elif direction == "Right":
            self.rect = self.image.get_rect(topleft = player.rect.topright + pygame.math.Vector2(-100, 0))
        elif direction == "Up":
            self.rect = self.image.get_rect(bottomleft = player.rect.topleft + pygame.math.Vector2(0, 50))
        else:
            self.rect = self.image.get_rect(topleft = player.rect.bottomleft + pygame.math.Vector2(0, -50))

class Shield(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        
        self.flip_x = True
        self.flip_y = False

        self.image = pygame.transform.scale(pygame.image.load("OtherAssets\\AuraShield.png").convert_alpha(), (player.image.get_width() + 10, player.image.get_height() + 10))
        self.rect = self.image.get_rect(center = (player.rect.center))
        self.time_started = pygame.time.get_ticks()
    
    def update(self):

        self.flip_x = not self.flip_x
        self.flip_y = not self.flip_y

        self.image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)
        self.rect.center = self.player.rect.center
        current_time = pygame.time.get_ticks()
        if current_time - self.time_started > 5000 or "Attack" in self.player.state:
            self.player.shield_cooldown_start = current_time
            self.player.shield_cooldown = True
            self.player.shield = None
            self.kill()