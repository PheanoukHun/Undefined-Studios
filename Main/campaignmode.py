# Importing the Necessary Libraries

import pygame
import sys
from GameEngine.level import Level
from GameEngine.settings import *
from Utilities.button import Button
from Utilities.debug import debug
from Utilities.ui import score_display

# Game Class
class Game:
    """
    Main game class responsible for managing game states and logic.
    """

    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()

        # Set up the display
        pygame.display.set_caption("Forgotten Frontiers")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize game state variables
        self.pause = False
        self.resume_button = Button(0, 0, "Buttons\\Resume.png")
        self.exit_button = Button(0, 0, "Buttons\\Exit.png")
        self.resume_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - self.resume_button.image.get_height() // 2 - 30)
        self.exit_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.exit_button.image.get_height() // 2 + 30)

    def update(self, player):
        """
        Update the game state.
        
        Args:
            player (str): Type of player character.
        """
        self.level.player.player_type = player
        self.level.player.import_player_assets()

    def change_level(self, levelnum, player_character):
        """
        Change the game level.
        
        Args:
            levelnum (int): Number of the level.
            player_character (str): Type of player character.
        """

        transition(f"Level {levelnum + 1}")
        self.level = Level(levelnum, player_character)
        self.levelnum = levelnum
        self.player_character = player_character

    def run(self):
        """
        Main game loop.
        
        Returns:
            bool: True if the game is won, False if the game is over.
        """
        while True:

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Pause Function
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.pause:
                            self.pause = False
                        else:
                            self.pause = True
            
            # Screen Display
            self.screen.fill(color_constants["Black"])
            if not self.pause:
                self.level.run()
                score_display(self.level.player.score * 5)
            else:
                if self.exit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
                if self.resume_button.draw(self.screen):
                    self.pause = False

            # Screen Updating
            pygame.display.update()
            self.clock.tick(FPS)

            # Level Transition
            if self.level.player.hp <= 0:
                return False
            if len(self.level.attackable_sprites) == 0:
                self.levelnum += 1
                if self.levelnum == 5:
                    return True
                elif self.levelnum == 4:
                    current_score = self.level.player.score
                    
                    transition("Boss Level")
                    self.level = Level(self.levelnum, self.player_character)

                    self.level.player.score = current_score
                else:
                    current_score = self.level.player.score
                    
                    transition(f"Level {self.levelnum + 1}")
                    self.level = Level(self.levelnum, self.player_character)

                    self.level.player.score = current_score

# Transition Screen In between the Level
def transition(text):

    # Graphics Window
    screen = pygame.display.get_surface()

    # Text Display Setup
    font = pygame.font.SysFont("Arial", 100)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Time
    start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    while current_time - start_time < 50:
        
        # Event Handler
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Screen Fill
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)

        # Screen Update
        game.clock.tick(FPS)
        pygame.display.update()

# Menu1 Function
def menu1():
    """
    First menu screen.
    
    Returns:
        None: Returns to the Main Loop.
    """
    
    # Get the Screen
    
    screen = pygame.display.get_surface()
    
    # Create the Buttons

    start_button = Button(0, 0, "Buttons/Start.png")
    credit_button = Button(0, 0, "Buttons/Credit.png")
    exit_button = Button(0, 0, "Buttons/Exit.png")
    info_button = Button(0, 0, "Buttons/Info.png")
    
    # Variable is Shown

    menu_shown = False
    info_shown = False

    # Centers the Button on the Screen

    start_button.rect.center = (SCREEN_WIDTH // 2, 125)
    credit_button.rect.center = (SCREEN_WIDTH // 2, 310)
    info_button.rect.center = (SCREEN_WIDTH // 2, 490)
    exit_button.rect.center = (SCREEN_WIDTH // 2, 675)
    
    # Menu Main Loop

    while True:

        # Event Getter

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            # Buttons Pressed Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    return
                elif credit_button.rect.collidepoint(event.pos):
                    menu_shown = True
                    display_start = pygame.time.get_ticks()
                
                elif info_button.rect.collidepoint(event.pos):
                    info_shown = True
                    display_start = pygame.time.get_ticks()

                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        # Draws the Screen

        screen.fill((0, 0, 0))
        start_button.draw(screen)
        credit_button.draw(screen)
        exit_button.draw(screen)
        info_button.draw(screen)
        
        # Credit Menu Opened

        if menu_shown:
            current_time = pygame.time.get_ticks()
            if current_time - display_start > 5000:
                menu_shown = False
            pygame.draw.rect(screen, (85, 85, 85), (50, 50, 850, 700))
            blit_text(screen, 800, "Game Created by Undefined Studios. Images are Credited in the Game Files.", (100, 75), credit_font, color_constants["Black"])
        
        # Info Menu Opened

        if info_shown:
            current_time = pygame.time.get_ticks()
            if current_time - display_start > 7500:
                info_shown = False
            pygame.draw.rect(screen, (85, 85, 85), (50, 50, 850, 700))
            blit_text(screen, 800, "This is a Dungeon Crawler Game where you get to choose the level you will play and the character you play as. Player Movements are WASD, Attack button is Right Alt, and Shield is Right Ctrl. There will be medical packs that when ran into will heal the player.", (100, 75), credit_font, color_constants["Black"])

        # Refresh the Frame

        game.clock.tick(FPS)
        pygame.display.update()

# Menu2 Function
def menu2():
    """
    Second menu screen for selecting player character.
    
    Args:
        boolean (bool): Boolean controlling menu loop.
    
    Returns:
        str: Type of selected player character.
    """
    screen = pygame.display.get_surface()

    knight_button = Button(0, 0, "Buttons\\Knight.png")
    ranger_button = Button(0, 0, "Buttons\\Ranger.png")
    wizard_button = Button(0, 0, "Buttons\\Wizard.png")

    knight_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
    ranger_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    wizard_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

    while True:
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
        pygame.display.update()

# Results Function
def results(text):
    """
    Display the game result.
    
    Args:
        text (str): Text to be displayed.
    """

    # Fonts
    font = pygame.font.SysFont("Arial", 100)
    score_font = pygame.font.SysFont(None, 50)
    
    # Render Fonts
    text = font.render(text, True, (255, 255, 255))
    score_text = score_font.render(f"Score: {game.level.player.score * 5}", True, color_constants["Black"])
    
    # Text Rects
    text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    score_rect = score_text.get_rect(midtop = text_rect.midbottom)

    # Scores Printed
    print("Congratulations!")
    print(f"You got: {game.level.player.score * 5}")

    #Time
    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Screen Display
        game.screen.fill(color_constants["Black"])
        game.screen.blit(text, text_rect)
        game.screen.blit(score_text, score_rect)
        
        # Display Update
        game.clock.tick(FPS)
        pygame.display.update()

        # Timer
        if current_time - start_time > 10000:
            pygame.quit()
            sys.exit()

# Main Game if This is the main function
if __name__ == "__main__":
    
    # Initialize the game
    game = Game()

    # Display menu screens and get user inputs
    menu1()
    player_character = menu2()
    
    # Start the selected game level
    game.change_level(levelnum, player_character)
    result = game.run()

    # Display game result
    if result:
        results("You Win!")
    else:
        results("Game Over.")