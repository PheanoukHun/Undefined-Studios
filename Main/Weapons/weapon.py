import pygame

class Weapon(pygame.sprite.Sprite):
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