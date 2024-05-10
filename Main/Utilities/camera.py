import pygame

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General Setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_height = self.screen.get_size()[0] // 2
        self.half_width = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.background = pygame.transform.scale(pygame.image.load("Background/StoneBackground.png").convert(), (5000, 5000))
        self.background_rect = self.background.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.background_rect.topleft - self.offset
        self.screen.blit(self.background, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_position)
    
    def enemy_update(self, player, groups):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "Mob"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player, groups)