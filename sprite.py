import math
import pygame
import sys
from utils import vector2
from player_movement import player_movement

class sprite_2:

    def __init__(self, _img, _x, _y, _height, _width):
        self.thing = "thing"
        #self.movement = player_movement(self, SPEED, dt, GRAV, vx, vy, isgrounded)
        self.image = _img
        self.y = _y
        self.x = _x
        self.height =_height
        self.width = _width
        mask = pygame.Rect(0,0,self.width,self.height)
        self.surface = pygame.Surface((_height,_width), pygame.SRCALPHA)
        self.surface.blit(self.image,(0,0), area=mask)
        self.mask = pygame.mask.from_surface( self.surface )
        self.rect = pygame.Rect(0,0,self.width,self.height)

    def print_location(self):
        print "X = ", self.x
        print "Y = ", self.y
        return

class player(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, _image):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = _image

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
    

        
