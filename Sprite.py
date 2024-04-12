import pygame

class Sprite:
  def __init__(self, x, y, width, height, image):
    self.sprite_image = pygame.image.load(image)
    self.sprite_rect = pygame.Rect(x, y, width, height)

  def scale(self, width, height, x, y):
    self.sprite_image = pygame.transform.scale(self.sprite_image, (width, height))
    self.sprite_rect = pygame.Rect(x, y, width, height)

  def rotate(self, angle):
    self.sprite_image = pygame.transform.rotate(self.sprite_image, angle)

  def draw(self, window):
    window.blit(self.sprite_image, (self.sprite_rect.x, self.sprite_rect.y))
