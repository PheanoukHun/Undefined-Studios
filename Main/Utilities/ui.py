import pygame
from GameEngine.settings import *

# Healthbar Class
class UI:

    # Initialization Function
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)
        self.health_bar_rect = pygame.Rect(10, 10 , HEALTH_BAR_WIDTH, BAR_HEIGHT)
    
    # Displays the Healthbar
    def display(self, player):
        pygame.draw.rect(self.screen, UI_BG_COLOR, self.health_bar_rect)
        left = int((player.hp / player.data["Health"]) * HEALTH_BAR_WIDTH)
        current_rect = self.health_bar_rect.copy()
        current_rect.width = left
        pygame.draw.rect(self.screen, HEALTH_COLOR, current_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, self.health_bar_rect, 3)

# Displays the Score
def score_display(score):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 45)
    text_rendered = font.render(f"Score: {score}", True, color_constants["White"])
    score_rect = text_rendered.get_rect(topright = (SCREEN_WIDTH - 25, 25))
    pygame.draw.rect(text_rendered, color_constants["Black"], score_rect)
    screen.blit(text_rendered, score_rect)