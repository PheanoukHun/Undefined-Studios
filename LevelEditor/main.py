# Import Libraries


import pygame
from button import Button
import csv
import os
import pickle

# Variables


SCREEN_WIDTH, SCREEN_HEIGHT = (800, 800)
LOWER_MARGIN, SIDE_MARGIN = (100, 300)

ROWS = 150
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // 16
TILE_TYPES = 21

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll = 0
scroll_vertical = 0
scroll_speed = 1

current_tile = 0
button_col = 0
button_row = 0

level = 0

FPS = 60
clock = pygame.time.Clock()

GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Create Empty Tile List


world_data = []

for i in range(ROWS):
    row = [-1] * MAX_COLS
    world_data.append(row)

# Create Ground

for i in range(0, MAX_COLS):
    world_data[ROWS - 1][i] = 0

# Pygame Initiation

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")
font = pygame.font.SysFont("Futura", 30)

# Loads the Images

pine1_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\pine1.png").convert_alpha()
pine2_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\pine2.png").convert_alpha()
mountain_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\mountain.png").convert_alpha()
sky_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\sky_cloud.png").convert_alpha()

# Function to draw the Backgrounds scrolling

def draw_BG():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for i in range(4):
        screen.blit(sky_img, ((width * i) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((width * i) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((width * i) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((width * i) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

# Function to Draw the Grid of Lines

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list1[tile], (x * TILE_SIZE, y * TILE_SIZE))

# Draws the Grid Lines

def draw_grid():

    # Vertical Line
    for i in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, SCREEN_HEIGHT))

    # Horizontal Line
    for i in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE - scroll_vertical), (SCREEN_WIDTH, i * TILE_SIZE - scroll_vertical))

# All the Tiles

img_list = [f"LevelEditor\LevelEditor-main/LevelEditor-main/img/tile/{i}.png" for i in range(TILE_TYPES)]
img_list1 = [pygame.transform.scale(pygame.image.load(file).convert_alpha(), (TILE_SIZE, TILE_SIZE)) for file in
            img_list]
button_list = []

# Button Creation for the Tiles

for i in range(len(img_list)):

    button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i])
    scale = TILE_SIZE / button.image.get_width()
    button.scale(scale)
    button_list.append(button)

    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

# Button Creation for Save and Load Buttons

save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + (LOWER_MARGIN // 4),
                    "LevelEditor\LevelEditor-main/LevelEditor-main/img/save_btn.png")
load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + (LOWER_MARGIN // 4),
                    "LevelEditor\LevelEditor-main/LevelEditor-main/img/load_btn.png")

# Function for drawing the World Tiles

# Function for drawing the World Tiles

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list1[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE - scroll_vertical))

# Function for Outputting text onto the Screen

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Refresh the Frame

def finish_frame():
    clock.tick(FPS)
    pygame.display.update()

# Main Loop

run = True
while run:

    # Draw Scene

    draw_BG()
    draw_grid()
    draw_world()

    # Draws the Texts

    draw_text(f"Level: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text("Press Up or Down to Change Level", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 50)

    # Save and Load Data

    if save_button.draw(screen):
        with open(os.path.join("LevelEditor\Levels", "Level" + str(level) + "data.csv"), "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            for row in world_data:
                writer.writerow(row)

        # Pickle Version
        """pickle_out = open(os.path.join("LevelEditor\Levels", "Level" + str(level) + "data.csv"), "wb")
        pickle.dump(world_data, pickle_out)
        pickle_out.close()"""

    if load_button.draw(screen):
        scroll = 0
        with open(os.path.join("LevelEditor\Levels", "Level" + str(level) + "data.csv"), newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        # Pickle Version
        """world_data = []
        pickle_in = open(os.path.join("LevelEditor\Levels", "Level" + str(level) + "data.csv"), "rb")
        world_data = pickle.load(pickle_in)
        pickle_in.close()"""

    # Draw Tile Panel and Titles

    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT, SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Choose a Tile
    button_count = 0
    for button_count, button in enumerate(button_list):
        if button.draw(screen):
            current_tile = button_count

    # Highlight Selected Tile

    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE - SCREEN_WIDTH):
        scroll += 5 * scroll_speed
    if scroll_down and scroll_vertical < (ROWS * TILE_SIZE - SCREEN_HEIGHT):
        scroll_vertical += 5 * scroll_speed
    if scroll_up and scroll_vertical > 0:
        scroll_vertical -= 5 * scroll_speed

    # Mouse Handling

    # Get Mouse Position
    mouse_position = pygame.mouse.get_pos()
    x = (mouse_position[0] + scroll) // TILE_SIZE
    y = mouse_position[1] // TILE_SIZE

    # Change World Data

    # Change World Data
    if mouse_position[0] < SCREEN_WIDTH and mouse_position[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            grid_x = (mouse_position[0] + scroll) // TILE_SIZE
            grid_y = (mouse_position[1] + scroll_vertical) // TILE_SIZE  # Adjust for vertical scroll
            if 0 <= grid_x < MAX_COLS and 0 <= grid_y < ROWS:
                if world_data[grid_y][grid_x] != current_tile:
                    world_data[grid_y][grid_x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            grid_x = (mouse_position[0] + scroll) // TILE_SIZE
            grid_y = (mouse_position[1] + scroll_vertical) // TILE_SIZE  # Adjust for vertical scroll
            if 0 <= grid_x < MAX_COLS and 0 <= grid_y < ROWS:
                world_data[grid_y][grid_x] = -1

    # Event Handler
    for event in pygame.event.get():

        # Scroll Handling

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_PERIOD:
                level += 1
            if event.key == pygame.K_COMMA and level > 0:
                level -= 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

        # Quit Handling

        if event.type == pygame.QUIT:
            run = False

    finish_frame()
pygame.quit()