from classes.button import Button
from classes.healthbar import HealthBar
from classes.entities import Player, Mob, Entity
from classes.sprite import Sprite, TextLabel
from classes.wall import Wall
import pygame
import random
import math
import csv


pygame.init()
pygame.font.init()

color_constants = {"Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Orange": (255, 165, 0)}

clock = pygame.time.Clock()
FPS = 30

SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 800)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forgotten Frontiers")

# Fonts

credit_font = pygame.font.SysFont("Arial", 40)

# Character Menu Button

knight_button = Button(0, 0, "Buttons\\Knight.png")
ranger_button = Button(0, 0, "Buttons\\Ranger.png")
wizard_button = Button(0, 0, "Buttons\\Wizard.png")

knight_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
ranger_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
wizard_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

# Render Text

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def finish_frame():
    pygame.display.update()
    clock.tick(FPS)

# Draws the Background

def draw_bg(horizontal, vertical, image):
    width = image.get_width()
    for i in range(4):
        screen.blit(image, ((width * i) - horizontal * 0.7, vertical))

# Function to Draw the Grid of Lines

def draw_world(img_list1, data, size, player = None):
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            tile = int(tile)
            if tile == 15:
                pass
            elif tile == 16:
                pass
            elif tile >= 0:
                wall = img_list1[tile]
                wall.rect.center = (x * size, y * size)
                screen.blit(wall.image, wall.rect)

def menu1(boolean):
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
                boolean = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    boolean = False
                    return True
                elif credit_button.rect.collidepoint(event.pos):
                    menu_shown = True
                    display_start = pygame.time.get_ticks()
                elif exit_button.rect.collidepoint(event.pos):
                    boolean = False
                    return False
        
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
        
        finish_frame()

def menu2(boolean):
    knight_button = Button(0, 0, "Buttons\\Knight.png")
    ranger_button = Button(0, 0, "Buttons\\Ranger.png")
    wizard_button = Button(0, 0, "Buttons\\Wizard.png")

    knight_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
    ranger_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    wizard_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

    while boolean:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boolean = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if knight_button.rect.collidepoint(event.pos):
                    player_type = "Knight"
                    boolean = False
                    return player_type
                elif ranger_button.rect.collidepoint(event.pos):
                    player_type = "ranger"
                    boolean = False
                    return player_type
                elif wizard_button.rect.collidepoint(event.pos):
                    player_type = "Wizard"
                    boolean = False
                    return player_type
        
        screen.fill((0, 0, 0))  # Clear the screen
        knight_button.draw(screen)
        ranger_button.draw(screen)
        wizard_button.draw(screen)
        
        finish_frame()

def main_game(boolean, player_character):
    world_data = []
    level = 1

    TILE_SIZE = SCREEN_HEIGHT // 16
    horizontal_scroll = 0
    vertical_scroll = 0
    TILE_TYPES = 21

    monster_type = ["Zombie", "Slime", "Skeleton"]
    img_list = [f"LevelEditor\LevelEditor-main/LevelEditor-main/img/tile/{i}.png" for i in range(TILE_TYPES)]
    img_list1 = [Wall(file, TILE_SIZE, TILE_SIZE) for file in img_list]
    
    mob_group = []
    player = Player(player_character, screen, 0, 0)

    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            tile = tile
            if tile == "15":
                player_spot = (TILE_SIZE * x, TILE_SIZE * y)
                print(tile)
            if tile == 16:
                monster = Mob(random.choice(monster_type), screen, TILE_SIZE * x, TILE_SIZE * y, player)
                mob_group.append(monster)
    
    #player.sprite_rect.center = player_spot

    bg_img = pygame.image.load("Background\StoneBackground.png")

    with open(f"LevelEditor\Levels\Level{level}data.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            world_data.append(row)

    while boolean:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boolean = False

        draw_bg(horizontal_scroll, vertical_scroll, bg_img)
        draw_world(img_list1, world_data, TILE_SIZE)

        for monster in mob_group:
            monster.draw()
        
        keys_pressed = pygame.key.get_pressed()
        player.draw(keys_pressed, mob_group)

        finish_frame()
        
if __name__ == "__main__":
    is_menu2 = menu1(True)
    if is_menu2:
        player_character = menu2(True)
    win = main_game(True, player_character)