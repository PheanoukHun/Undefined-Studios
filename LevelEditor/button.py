import pygame

pygame.init()

class Button():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.image = pygame.image.load(image).convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def scale(self, number):

        self.width = int(self.width * number)
        self.height = int(number * self.height)
        
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        window.blit(self.image, (self.rect.x, self.rect.y))
        return action