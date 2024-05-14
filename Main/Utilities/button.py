# Library Import
import pygame

# Pygame Initialization
pygame.init()

# Button Class
class Button():

    # Initialization Function
    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.image = pygame.image.load(image).convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    # Draws the Button and Checks for the Button is Pressed or not
    def draw(self, window):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        window.blit(self.image, (self.rect.x, self.rect.y))
        return action