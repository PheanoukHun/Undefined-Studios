import pygame, sys
from level import Level
from settings import *
from button import Button
from debug import debug

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Forgotten Frontiers")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.pause = False
        self.resume_button = Button(0, 0, "Buttons\\Resume.png")
        self.exit_button = Button(0, 0, "Buttons\\Exit.png")
        self.resume_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - self.resume_button.image.get_height() // 2 - 30)
        self.exit_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.exit_button.image.get_height() // 2 + 30)

    def update(self, player):
        self.level.player.player_type = player
        self.level.player.import_player_assets()

    def change_level(self, levelnum):
        self.level = Level(levelnum)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = True
            
            self.screen.fill(color_constants["Black"])
            if not self.pause:
                self.level.run()
            else:
                if self.exit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
                if self.resume_button.draw(self.screen):
                    self.pause = False

            #debug(self.level.player.data[self.level.player.state])

            pygame.display.update()
            self.clock.tick(FPS)

            if self.level.player.hp <= 0:
                return False
            if len(self.level.attackable_sprites) == 0:
                return True

def finish_frame():
    pygame.display.update()

def menu1(boolean):
    screen = pygame.display.get_surface()
    start_button = Button(0, 0, "Buttons\\Start.png")
    credit_button = Button(0, 0, "Buttons\\Credit.png")
    exit_button = Button(0, 0, "Buttons\\Exit.png")

    start_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    credit_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    exit_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

    menu_shown = False
    
    while boolean:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    boolean = False
                    return True
                elif credit_button.rect.collidepoint(event.pos):
                    menu_shown = True
                    display_start = pygame.time.get_ticks()
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.fill((0, 0, 0))  # Clear the screen
        start_button.draw(screen)
        credit_button.draw(screen)
        exit_button.draw(screen)
        
        if menu_shown:
            current_time = pygame.time.get_ticks()
            if current_time - display_start > 5000:
                menu_shown = False
            credit_rect = pygame.draw.rect(screen, (85, 85, 85), (50, 50, 850, 700))
            blit_text(screen, "Game Created by Undefined Studios. Images are Credited in the Game Files.", (50, 50), credit_font, color_constants["Black"])
        
        game.clock.tick(FPS)
        finish_frame()

def menu2(boolean):
    
    screen = pygame.display.get_surface()

    knight_button = Button(0, 0, "Buttons\\Knight.png")
    ranger_button = Button(0, 0, "Buttons\\Ranger.png")
    wizard_button = Button(0, 0, "Buttons\\Wizard.png")

    knight_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
    ranger_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    wizard_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

    while boolean:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if knight_button.rect.collidepoint(event.pos):
                    player_type = "Knight"
                    return player_type
                elif ranger_button.rect.collidepoint(event.pos):
                    player_type = "Ranger"
                    return player_type
                elif wizard_button.rect.collidepoint(event.pos):
                    player_type = "Wizard"
                    return player_type
        
        screen.fill((0, 0, 0))  # Clear the screen
        knight_button.draw(screen)
        ranger_button.draw(screen)
        wizard_button.draw(screen)
        
        game.clock.tick()
        finish_frame()

def menu3():
    screen = pygame.display.get_surface()
    level1 = Button(0, 0, "Buttons\\Level1.png")
    level2 = Button(0, 0, "Buttons\\Level2.png")
    level3 = Button(0, 0, "Buttons\\Level3.png")

    level1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    level2.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    level3.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.rect.collidepoint(event.pos):
                    levelnum = 1
                    return levelnum
                elif level2.rect.collidepoint(event.pos):
                    levelnum = 2
                    return levelnum
                elif level3.rect.collidepoint(event.pos):
                    levelnum = 3
                    return levelnum
        
        screen.fill((0, 0, 0))  # Clear the screen
        
        level1.draw(screen)
        level2.draw(screen)
        level3.draw(screen)
        
        game.clock.tick(FPS)
        finish_frame()

def results(text):
    font = pygame.font.SysFont("Arial", 100)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game.screen.fill(color_constants["Black"])
        game.screen.blit(text, text_rect)
        
        game.clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    is_menu2 = menu1(True)
    if is_menu2:
        player_character = menu2(True)
    levelnum = menu3()
    game.change_level(levelnum)
    result = game.run()

    if result:
        results("You Win!")
    else:
        results("Game Over.")