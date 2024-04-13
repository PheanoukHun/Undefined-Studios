import pygame

pygame.init()
pygame.font.init()

class Sprite:
  
  def __init__(self, x, y, width, height, image):
    self.sprite_image = pygame.image.load(image)
    self.sprite_rect = pygame.Rect(x, y, width, height)

  def scale(self, width, height, x, y):
    self.sprite_image = pygame.transform.scale(self.sprite_image, (width, height))
    self.sprite_rect = pygame.Rect(x, y, width, height)

  def rotate(self, angle):
    self.sprite_image = pygame.transform.rotate(self.sprite_image, angle)

  def flip_x(self, boolean):
    self.sprite_image = pygame.transform.flip(self.sprite_image, boolean, False)

  def flip_y(self, boolean):
    self.sprite_image = pygame.transform.flip(self.sprite_image, False, boolean)
  
  def draw(self, window):
    window.blit(self.sprite_image, (self.sprite_rect.x, self.sprite_rect.y))

class TextLabel:
  
  def __init__ (self, text, x, y, color, window, font):
    
    self.text = text
    self.font = font
    self.window = window

    self.x = x
    self.y = y
    
    self.text_label = font.render(text, 1, color)
    window.blit(self.rendered_text, (x, y))
  
  def change_color(self, color):
    self.text_label = self.font.render(self.text, 1, color)
    self.window.blit(self.text_label, (self.x, self.y))
