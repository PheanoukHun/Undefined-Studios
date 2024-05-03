import pygame

pygame.init()
pygame.font.init()

class Sprite (pygame.sprite.Sprite):

    # Initilization Function

    def __init__(self, x, y, image, window):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_image = pygame.image.load(image).convert_alpha()
        self.width = self.sprite_image.get_width()
        self.height = self.sprite_image.get_height()

        self.sprite_rect = self.sprite_image.get_rect(topleft=(x, y))

        self.x_coord = x
        self.y_coord = y
        self.x_center = self.sprite_rect.centerx
        self.y_center = self.sprite_rect.centery

        self.image_file = image
        self.window = window

        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0

        self.is_flipped_x = False
        self.is_flipped_y = False

    # Coordinate Place of the Sprite Property and Setter

    @property
    def x(self):
        return self.sprite_rect.x

    @x.setter
    def x(self, value):
        self.x_coord = value
        self.x_center = value + self.width // 2
        self.sprite_rect.x = value

    @property
    def y(self):
        return self.sprite_rect.y

    @y.setter
    def y(self, value):
        self.y_coord = value
        self.y_center = value + self.height // 2
        self.sprite_rect.y = value

    @property
    def center_x(self):
        return self.x_center

    @center_x.setter
    def center_x(self, value):
        if isinstance(value, (int, float)):
            self.sprite_rect.centerx = value
            self.x = value - self.width // 2

    @property
    def center_y(self):
        return self.sprite_rect.centery
    
    @center_y.setter
    def center_y(self, value):
        if isinstance(value, (int, float)):
            self.sprite_rect.centery = value
            self.y = value - self.height // 2

    # Scale Property and Setter

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.width = int(self.sprite_image.get_width() * value)
        self.height = int(self.sprite_image.get_height() * value)
        self.sprite_image = pygame.transform.scale(self.sprite_image, (self.width, self.height))

    # Rotation Property and Setter

    @property
    def rotate(self):
        return self.angle

    @rotate.setter
    def rotate(self, angle):
        if isinstance(angle, int):
            self.angle = angle
            self.sprite_image = pygame.transform.rotate(self.sprite_image, self.angle)

    # Image Property and Setter

    @property
    def image(self):
        return self.image_file

    @image.setter
    def image(self, filename):
        self.image_file = filename
        self.sprite_image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(), (self.width, self.height))
        self.update_transform()

    # X and Y Axis Flip Property and Setter

    @property
    def flip_x(self):
        return self.is_flipped_x

    @flip_x.setter
    def flip_x(self, boolean):
        if isinstance(boolean, bool):
            self.is_flipped_x = boolean
            self.update_transform()

    @property
    def flip_y(self):
        return self.is_flipped_y

    @flip_y.setter
    def flip_y(self, boolean):
        if isinstance(boolean, bool):
            self.is_flipped_y = boolean
            self.update_transform()

    # X and Y Speed Property and Setter

    @property
    def x_speed(self):
        return self.speed_x

    @x_speed.setter
    def x_speed(self, value):
        if isinstance(value, (int, float)):
            self.speed_x = value

    @property
    def y_speed(self):
        return self.speed_y

    @y_speed.setter
    def y_speed(self, value):
        if isinstance(value, (int, float)):
            self.speed_y = value

    # Collision detection method
    def collide_with(self, other_sprite):
        
        if self.sprite_rect.colliderect(other_sprite.sprite_rect):
            self_mask = pygame.mask.from_surface(self.sprite_image)
            other_mask = pygame.mask.from_surface(other_sprite.sprite_image)

            if self_mask.overlap(other_mask, other_sprite.sprite_rect.topleft):
                return True

        return self.sprite_rect.colliderect(other_sprite.sprite_rect)

    # Function Used to Update Transformations

    def update_transform(self):
        self.sprite_image = pygame.transform.flip(
            pygame.transform.rotate(self.sprite_image, self.angle), self.is_flipped_x, self.is_flipped_y)
        self.sprite_rect.size = self.sprite_image.get_size()
        self.widht, self.height = self.sprite_image.get_size()

    #Function used to draw the Sprite

    def draw(self, horizontal_scroll = 0, vertical_scroll = 0):
        pygame.draw.rect(self.window, (255, 255, 255), self.sprite_rect, 2)
        self.sprite_rect.move_ip(self.speed_x + horizontal_scroll, self.speed_y + vertical_scroll)
        self.window.blit(self.sprite_image, self.sprite_rect)

class SpriteSheet:
    def __init__(self, image):
        self.sheet = pygame.image.load(image).convert_alpha()

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

class AnimatedSprite(Sprite):

    #Initiation Function

    def __init__(self, x, y, width, height, image, window, frames, animation_time, scale=1):
        super().__init__(x, y, image, window)
        self.sprite_sheet = SpriteSheet(image)
        self.frames = [i for i in range(frames)]
        self.animation_time = animation_time
        self.scale = scale
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        self.width = width
        self.height = height

    @property
    def frame(self):
        return len(self.frames)
    
    @frame.setter
    def frame(self, value):
        
        try:
            value = int(value)
        except:
            value = 1
        
        self.frames = [i for i in range(value)]

    # Update the sprite image

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_time:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    # Changes the Image

    def change_spritesheet(self, image):
        self.sprite_sheet = SpriteSheet(image)

    # Draws the sprite

    def draw(self):

        self.sprite_rect.x += self.speed_x
        self.sprite_rect.y += self.speed_y

        self.update()
        image = self.sprite_sheet.get_image(self.frames[self.current_frame], self.width, self.height, self.scale, (0, 0, 0))
        self.window.blit(image, self.sprite_rect.topleft)

class TextLabel(Sprite):

    #Initiation Function
    def __init__(self, text, x, y, color, window, font, size):
        self.x = x
        self.y = y

        self.window = window
        
        self._text = text
        self._color = color
        self._font_type = font
        self._font_size = size
        self._update_text()

    # Text Properties
    @property
    def text(self):
        return self._text

    # Text Setter
    @text.setter
    def text(self, value):
        self._text = value
        self._update_text()

    # Text Color Properties
    @property
    def color(self):
        return self._color

    # Text Color Setter
    @color.setter
    def color(self, value):
        self._color = value
        self._update_text()

    # Text Font Properties
    @property
    def font_type(self):
        return self._font_type

    # Text Font Setter
    @font_type.setter
    def font_type(self, value):
        self._font_type = value
        self._update_text()

    # Text Font Size Properties
    @property
    def font_size(self):
        return self._font_size

    # Text Font Size Setter
    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self._update_text()


    # Update the Texts
    def _update_text(self):
        self._font = pygame.font.SysFont(self._font_type, self._font_size)
        self._text_label = self._font.render(self._text, True, self._color)
        self.image = self._text_label
        self.rect = self._text_label.get_rect(topleft=(self.x, self.y))

    #Draws the Text
    def draw(self):
        self.window.blit(self._text_label, self.rect.topleft)

# If this file is the main file ran
if __name__ == "__main__":

    _width, _height = (1018, 573)
    _character_width, _character_height = (150, 150)

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

    _character = Sprite(100, 100, "PixelCharacters\pixel_knight.png", _window)
    
    _character.center_x = 500
    _character.center_y = 250

    def _handle_character_movement(keys_pressed, character):
        if keys_pressed[pygame.K_a] and character.sprite_rect.x - 5 >= 0:
            character.x_speed = -5
        elif keys_pressed[pygame.K_d] and character.sprite_rect.x + 5 + character.width < _width:
            character.x_speed = 5
        else:
            character.x_speed = 0

        if keys_pressed[pygame.K_w] and character.sprite_rect.y - 5> 0:
            character.y_speed = -5
        elif keys_pressed[pygame.K_s] and character.sprite_rect.y + 5 + character.height < _height:
            character.y_speed = 5
        else:
            character.y_speed = 0
        
        if character.x < 0:
            character.x = 0
        if character.y < 0:
            character.y = 0
        if character.x + character.width > _width:
            character.x = _width - character.width
        if character.y + character.height > _height:
            character.y = _height - character.height

    def _draw_window(character):
        _window.fill(_color_constants["Blue"])
        character.draw()
        pygame.display.update()

    while _run:
        _clock.tick(_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False
            
            _key_pressed = pygame.key.get_pressed()
            _handle_character_movement(_key_pressed, _character)

        _draw_window(_character)
    pygame.quit()