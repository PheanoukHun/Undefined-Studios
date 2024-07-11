# Import Libraries
import csv
import pygame

# Initialize Font
pygame.font.init()

#Use Tiled
color_constants = {"Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Orange": (255, 165, 0)}

# General Info
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 800)
TILE_SIZE = 1000 // 16

#UI Info
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
UI_FONT = "Arial"
UI_FONT_SIZE = 18

HEALTH_COLOR = 'red'
UI_BG_COLOR = "#222222"
TEXT_COLOR = "#EEEEEE"
UI_BORDER_COLOR = "#111111"
WATER_COLOR = "#71ddee"

# Credit Font and Text Label Creation
credit_font = pygame.font.SysFont("Arial", 35)
def blit_text(surface, width, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Level Creation and Level Num
levelnum = 1

def read_world_data(levelnum):
    world_data = []
    with open(f"OtherAssets/Levels/Level{levelnum}data.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            world_data.append(row)
    return world_data

world_data = read_world_data(levelnum)