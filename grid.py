import pygame
from utils import *
from pygame.locals import *

class Grid( object ):
    def __init__( self, width, height ):
        self.gridwidth = width
        self.gridheight = height
        self.tilewidth = 800/width;
        self.tileheight = 400/height;
        self.black = 0, 0, 0
        self.tilelist_set({})
        for x in range(0, width):
            for y in range(0, height):
                self.tilelist_get().update( {(x,y): Tile()} )

    def tilelist_get( self ):
        return self._tilelist

    def tilelist_set( self, value ):
        self._tilelist = value

    tilelist = property(tilelist_get, tilelist_set)

    def draw(self, screen):
        for x in range (1, self.gridwidth):
            pygame.draw.line(screen, self.black, (self.tilewidth*x,0), (self.tilewidth*x, 400))

        for y in range (1, self.gridheight):
            pygame.draw.line(screen, self.black, (0,self.tileheight*y), (800, self.tileheight*y))

class Tile( object ):
    def __init__( self ):
        self.terrain_set('default')
        self.occupied_set(False)

    def terrain_get( self ):
        return self._terrain

    def terrain_set( self, value ):
        self._terrain = value

    terrain = property(terrain_get, terrain_set)

    def occupied_get( self ):
        return self._occupied

    def occupied_set( self, value ):
        self._occupied = value

    occupied = property(occupied_get, occupied_set)
