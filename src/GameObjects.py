import pygame
from BaseClasses import *

# Image paths
VIRUS_IMAGE_PATH = "res/virus.png"
VIRUS_TAGGED_IMAGE_PATH = "res/virus_tagged.png"
ANTIBODY_IMAGE_PATH = "res/antibody.png"
CELL_IMAGE_PATH = "res/cell.png"
NUCLEUS_IMAGE_PATH = "res/nucleus.png"
PROTEASOME_IMAGE_PATH = "res/proteasome.png"
PROTEASOME_SELECTED_IMAGE_PATH = "res/proteasome_selected.png"

# Object constants
VIRUS_SPEED = 2
VIRUS_TAGGED_SPEED = 0.7
VIRUS_RADIUS = 10 # Used for collision detection between tagged and untagged viruses
PROTEASOME_SPEED = 3

MOUSECLICK_COLLISION_CHECK_SIZE = 20 # Used for collision detection between mouse clicks and any other point

class Cell(Image_Sprite):
    def __init__(self, center):
        Image_Sprite.__init__(self, CELL_IMAGE_PATH, center)
        self.radius = (self.rect.width / 2) - 20

class Nucleus(Image_Sprite):
    def __init__(self, center):
        Image_Sprite.__init__(self, NUCLEUS_IMAGE_PATH, center)
        self.radius = (self.rect.width / 2) 


class Virus(Moving_Image_Sprite):
    def __init__(self, position, target):
        Moving_Image_Sprite.__init__(self, position, target, VIRUS_SPEED, VIRUS_IMAGE_PATH)
        # Used by collide_circle to generate a circle for the sprite to use in collision detection
        self.radius = VIRUS_RADIUS

    def tag(self):
        self.set_moving_image(VIRUS_TAGGED_IMAGE_PATH)
        self.speed = VIRUS_TAGGED_SPEED


class Proteasome(Moving_Image_Sprite):
    def __init__(self, position):
        Moving_Image_Sprite.__init__(self, position, position, PROTEASOME_SPEED, PROTEASOME_IMAGE_PATH)

    def select(self):
        self.set_moving_image(PROTEASOME_SELECTED_IMAGE_PATH)

    def unselect(self):
        self.set_moving_image(PROTEASOME_IMAGE_PATH)

    def move_to(self, target):
        self.target = target

class Antibody(Image_Sprite):
    def __init__(self, position):
        Image_Sprite.__init__(self, ANTIBODY_IMAGE_PATH, position)

class MouseClickSprite(pygame.sprite.Sprite):
    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, MOUSECLICK_COLLISION_CHECK_SIZE, MOUSECLICK_COLLISION_CHECK_SIZE)
        self.rect.center = coords.as_array()
