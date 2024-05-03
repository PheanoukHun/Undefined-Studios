import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = "Melee"
        direction = player.state.split("_")[0]

        #graphic
        if direction == "Left" or direction == "Right":
            self.image = pygame.Surface((40, player.image.get_height())).convert_alpha()
        if direction == "Up" or direction == "Down":
            self.image = pygame.Surface((player.image.get_width(), 40)).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        #Placement
        if direction == "Left":
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(20, -75))
        if direction == "Right":
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(20, -75))
        if direction == "Up":
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0, 20))
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0, -20))