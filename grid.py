import pygame
from utils import *
from pygame.locals import *

class Grid( object ):
    def __init__( self, x, y ):
        self.gridwidth = x
        self.gridheight = y
        self.tilewidth = 800/x;
        self.tileheight = 400/y;
        self.black = 0, 0, 0

    def draw(self, screen):
        for x in range (1, self.gridwidth):
            pygame.draw.line(screen, self.black, (self.tilewidth*x,0), (self.tilewidth*x, 400))

        for y in range (1, self.gridheight):
            pygame.draw.line(screen, self.black, (0,self.tileheight*y), (800, self.tileheight*y))
