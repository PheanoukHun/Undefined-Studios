import pygame

pygame.init()
pygame.font.init()

class Sprite:
    def __init__(self, x, y, width, height, image, window):

        self.x = x
        self.y = y

        self.x_center = 0
        self.y_center = 0
        
        self.width = width
        self.height = height
        
        self.image = image
        self.window = window

        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0

        self.is_flipped_x = False
        self.is_flipped_y = False
        
        self.sprite_image = pygame.transform.scale(
            pygame.image.load(image), (width, height))
        self.sprite_rect = pygame.Rect(x, y, width, height)

    def scale(self, width, height):
    
        self.width = width
        self.height = height
        
        self.sprite_image = pygame.transform.scale(self.sprite_image, (width, height))
        self.sprite_rect = pygame.Rect(self.x, self.y, width, height)

    def rotate(self, angle):
        self.angle = angle
        self.sprite_image = pygame.transform.rotate(self.sprite_image, angle)

    def flip_x(self, boolean):
        self.is_flipped_x = boolean
        self.sprite_image = pygame.transform.flip(self.sprite_image, boolean, False)

    def flip_y(self, boolean):
        self.is_flipped_y = boolean
        self.sprite_image = pygame.transform.flip(self.sprite_image, False, boolean)

    def add_object(self):
        _window = self.window
        _window.blit(self.sprite_image, (self.sprite_rect.x, self.sprite_rect.y))

    def move_x_units(self, speed):
        self.speed_x = speed
        self.sprite_rect.x += speed

    def move_y_units(self, speed):
        self.speed_y = speed
        self.sprite_rect.y += speed

    @property
    def center_x(self):
        return self.x_center
    
    @center_x.setter
    def center_x(self, value):
        if str(value).isdigit():
            self.x_center = value
            self.x = value - (self.width)//2
    
    @property
    def center_y(self):
        return self.y_center
    
    @center_y.setter
    def center_y(self, value):
        if str(value).isdigit():
            self.y_center = value
            self.y = value - (self.height)//2

class TextLabel(Sprite):

    def __init__ (self, text, x, y, color, window, font):
    
        self.text = text
        self.font = font
        self.window = window

        self.x = x
        self.y = y

        self.angle = 0

        self.is_flipped_x = False
        self.is_flipped_y = False

        self.color = color
        
        self.text_label = font.render(text, 1, color)

    def change_color(self, color):
        self.text_label = self.font.render(self.text, 1, color)
        self.window.blit(self.text_label, (self.x, self.y))

if __name__ == "__main__":

    _width, _height = (1018, 573)
    _character_width, _character_height = (500, 500)

    _clock = pygame.time.Clock()
    pygame.display.set_caption("Forgotten Frontiers")

    _FPS = 30
    _VEL = 5

    _CHARACTER_HIT = pygame.USEREVENT + 1
    _MOB_HIT = pygame.USEREVENT + 2

    _run = True

    _color_constants = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Orange": (255, 165, 0)}

    _window = pygame.display.set_mode((_width, _height))

    _character = Sprite(509, 250, _character_width, _character_height, 
                        "pixel_knight.png", 
                        _window)
    
    _character.center_y = 250
    _character.center_x = 509

    def draw_window(character):
        _window.fill(_color_constants["White"])
        _window.blit(character.sprite_image, (character.x, character.y))
        pygame.display.update()

    while _run:
        _clock.tick(_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False

        draw_window(_character)
    
    pygame.quit()
