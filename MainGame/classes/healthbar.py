import pygame

pygame.init()

class HealthBar():
    def __init__(self, x, y, width, height, max_hp, window):
        self.x, self.y = (x, y)
        self.width, self.height = (width, height)

        self.max_hp = max_hp
        self.hp = max_hp

        self.window = window
    
    def draw(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.window, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.window, (0, 255, 0), (self.x, self.y, int(self.width * ratio), self.height))

if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 400))
    healthbar = HealthBar(250, 200, 300, 40, 100, screen)
    healthbar.hp = 75

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        healthbar.draw()
        pygame.display.update()
    pygame.quit()