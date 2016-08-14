import pygame, math

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)"  % (self.x, self.y)

    def __eq__(self, other): # Called by python to test equality
        return True if (self.x == other.x and self.y == other.y) else False

    def __sub__(self, other): # Called by python to handle subtraction
        return Coordinates(self.x - other.x, self.y - other.y)

    def as_array(self):
        return [self.x, self.y]

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    baby_blue = (137, 207, 240)
    yellow = (255, 255, 0)

class Image_Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.set_image(image_path)
        self.rect.center = initial_position.as_array()

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(pygame.Color(0, 0, 0)) # Any black pixels will be removed
        self.rect = self.image.get_rect()

class Moving_Image_Sprite(Image_Sprite):
    def __init__(self, position, target, speed, image_path):
        Image_Sprite.__init__(self, image_path, position)
        self.position = position # Coordinates
        self.target = target # Coordinates
        self.speed = speed # Float

    def new_coordinates_to_move_to(self):
        distance_to_target = self.target - self.position # Coordinates
        magnitude = math.sqrt((distance_to_target.x**2 + distance_to_target.y**2)) # sqrt(x^2 + y^2) - Pythagorean theorem
        if magnitude > 1:
            return Coordinates(distance_to_target.x / magnitude, distance_to_target.y / magnitude)
        else:
            return None # Already at the desired target

    def set_moving_image(self, image_path):
        # This is needed because set_image sets the rect to (0, 0, W, H) which moves the entire image to the top left
        Image_Sprite.set_image(self, image_path)
        self.rect.center = self.position.as_array()

    def update(self):
        new_position = self.new_coordinates_to_move_to()
        if new_position != None:
            self.position.x += new_position.x * self.speed
            self.position.y += new_position.y * self.speed
            self.rect.center = self.position.as_array()


class Scene:
    def __init__(self, args = None):
      self.screen = pygame.display.get_surface()
      self.background = pygame.Surface(self.screen.get_size())
      self.background = self.background.convert()
      self.background.fill(Color.white)
      self.center_x = self.background.get_rect().centerx
      self.center_y = self.background.get_rect().centery
      self.center = Coordinates(self.center_x, self.center_y)
      self.build_scene(args)
      self.done = False
      self.clock = pygame.time.Clock()
      self.framerate = 60
      self.event_loop()

    def build_scene(self, args):
        # Called on init
        pass

    def render_scene(self):
        # Called every frame
        pass

    def click(self, position):
        pass

    def handle_event(self, event):
        pass

    def event_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    self.click(position)
                else:
                    self.handle_event(event)
            self.background.fill(Color.white)
            self.render_scene()
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.framerate)
