import pygame

class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        self.image = pygame.transform.scale(pygame.image.load("OtherAssets\\AuraShield.png").convert_alpha(), (player.image.get_width() + 10, player.image.get_height() + 10))
        self.rect = self.image.get_rect(center = (player.hitbox.center))
        
    def update(self):
        self.rect.center = self.player.hitbox.center
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)