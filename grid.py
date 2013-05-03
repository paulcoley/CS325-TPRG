import pygame
from utils import *
from pygame.locals import *

class Grid( object ):
    def __init__( self, screen ):
        self.tilewidth = 100 #Width a grid tile
        self.tileheight = 100 #Height a grid tile
        self.gridwidth = screen.get_width()/self.tilewidth #Coordinate width of the grid
        self.gridheight = (screen.get_height() - 100)/self.tileheight #Coordinate width of the grid
        self.black = 0, 0, 0 #Color of the Grid lines
        self.tilelist = {} #List of grid tiles
        for x in range(0, self.gridwidth): #Fills out the list of tiles
            for y in range(0, self.gridheight):
                self.tilelist.update( {(x,y): Tile()} )

    def draw(self, screen, imagedict): #Draws the tiles on the screen as well as draws the grid lines
        for x in range (0, self.gridwidth):
            for y in range (0, self.gridheight):
                self.tilelist[(x, y)].draw(screen, (self.tilewidth*x, self.tileheight*y), imagedict)
        
        for x in range (1, self.gridwidth):
            pygame.draw.line(screen, self.black, (self.tilewidth*x,0), (self.tilewidth*x, screen.get_height() - 100))

        for y in range (1, self.gridheight + 1):
            pygame.draw.line(screen, self.black, (0,self.tileheight*y), (screen.get_width(), self.tileheight*y))

class Tile( object ): # Stores properties of a tile that are then applied to the grid and units on them
    def __init__( self ):
        self.terrain = 'Plains' #Set terrain type
        if self.terrain == 'Mountain': #If mountainous, make it so that the tile is considered occupied
            self.occupied = True
        else:
            self.occupied = False

    def draw( self, screen, xy, imagedict): #Draws tiles on the screen
        screen.blit(imagedict[self.terrain], xy)
