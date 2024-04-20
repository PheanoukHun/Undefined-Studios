import pygame
from button import Button

SCREEN_WIDTH, SCREEN_HEIGHT = (800, 640)
LOWER_MARGIN, SIDE_MARGIN = (100, 300)

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0

FPS = 60
clock = pygame.time.Clock()

GREEN = (144, 201, 120)
WHITE= (255, 255, 255)
RED = (200, 25, 25)

#Create Empty Tile List
world_data = []


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

pine1_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\pine1.png").convert_alpha()
pine2_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\pine2.png").convert_alpha()
mountain_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\mountain.png").convert_alpha()
sky_img = pygame.image.load("LevelEditor\LevelEditor-main\LevelEditor-main\img\Background\sky_cloud.png").convert_alpha()

img_list = [f"LevelEditor/LevelEditor-main/LevelEditor-main/img/tile/{i}.png" for i in range(TILE_TYPES)]

def draw_BG():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for i in range(4):
        screen.blit(sky_img, ((width * i) - scroll * 0.5,0))
        screen.blit(mountain_img, ((width * i) - scroll * 0.6,SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((width * i) - scroll * 0.7,SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((width * i) - scroll * 0.8,SCREEN_HEIGHT - pine2_img.get_height()))

button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    
    button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i])
    scale = TILE_SIZE / button.image.get_width()
    button.scale(scale)
    button_list.append(button)
    
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

def draw_grid():

    # Vertical Line
    for i in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, SCREEN_HEIGHT))
    
    # Horizontal Line
    for i in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE), (SCREEN_WIDTH, i * TILE_SIZE))

run = True
while run:
    
    draw_BG()
    draw_grid()

    # Draw Tile Panel and Titles
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
    if scroll_right and scroll < (sky_img.get_width() * 3):
        scroll += 5 * scroll_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
            
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()