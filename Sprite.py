import pygame

pygame.init()
pygame.font.init()

class Sprite:
    def __init__(self, x, y, width, height, image, window):
        
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        self.image = image
        self.window = window

        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0

        self.is_flipped_x = False
        self.is_flipped_y = False
        
        self.sprite_image = pygame.image.load(image)
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
        self.sprite_image = pygame.transform.flip(self.sprite_image, boolean, self.is_flipped_y)

    def flip_y(self, boolean):
        self.is_flipped_y = boolean
        self.sprite_image = pygame.transform.flip(self.sprite_image, self.is_flipped_x, boolean)
    
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

    def draw(self):
        self.window.blit(self.sprite_image, (self.sprite_rect.x, self.sprite_rect.y))

class AnimatedSprites(Sprite):
    def __init__(self, x, y, width, height, images, window):
        super.__init__(x, y, width, height, images[0], window)
    
    def update_animation(self):
        # Update animation frame based on time elapsed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed * 1000:
                self.image_index = (self.image_index + 1) % len(self.images)
                self.sprite_image = pygame.transform.scale(pygame.image.load(self.images[self.image_index]), (self.width, self.height))
                self.last_update_time = current_time

    def draw(self):
        self.update_animation()
        self.sprite_image = pygame.transform.flip(self.sprite_image, self.is_flipped_x, self.is_flipped_y)
        self.sprite_image = pygame.transform.rotate(self.sprite_image, self.angle)
        super.draw()

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
    _character_width, _character_height = (60, 60)

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

    _character = Sprite(100, 100, _character_width, _character_height,
                        "assets\pixel_knight.png",
                        _window)

    def handle_character_movement(keys_pressed, character):
        if keys_pressed[pygame.K_a] and character.sprite_rect.x - 5 > 0:
            character.move_x_units(-5)
        if keys_pressed[pygame.K_d] and character.sprite_rect.x + 5 + character.width < _width:
            character.move_x_units(5)
        if keys_pressed[pygame.K_w] and character.sprite_rect.y - 5> 0:
            character.move_y_units(-5)
        if keys_pressed[pygame.K_s] and character.sprite_rect.x + 5 + character.height < _height:
            character.move_y_units(5)
        
    def draw_window(character):
        
        _window.fill(_color_constants["Blue"])
        character.draw()
        pygame.display.update()

    while _run:
        _clock.tick(_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False
            
            key_pressed = pygame.key.get_pressed()
            handle_character_movement(key_pressed, _character)

        draw_window(_character)
