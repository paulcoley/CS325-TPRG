import pygame
from utils import *
from pygame.locals import *

class Grid( object ):
    def __init__( self, screen ):
        self.tilewidth = 100
        self.tileheight = 100
        self.gridwidth = screen.get_width()/self.tilewidth
        self.gridheight = screen.get_height()/self.tileheight
        self.black = 0, 0, 0
        self.tilelist_set({})
        for x in range(0, self.gridwidth):
            for y in range(0, self.gridheight):
                self.tilelist_get().update( {(x,y): Tile()} )

    def tilelist_get( self ):
        return self._tilelist

    def tilelist_set( self, value ):
        self._tilelist = value

    tilelist = property(tilelist_get, tilelist_set)

    def draw(self, screen, imagedict):
        for x in range (0, self.gridwidth):
            for y in range (0, self.gridheight):
                self.tilelist_get()[(x, y)].draw(screen, (self.tilewidth*x, self.tileheight*y), imagedict)
        
        for x in range (1, self.gridwidth):
            pygame.draw.line(screen, self.black, (self.tilewidth*x,0), (self.tilewidth*x, screen.get_height()))

        for y in range (1, self.gridheight):
            pygame.draw.line(screen, self.black, (0,self.tileheight*y), (screen.get_width(), self.tileheight*y))

class Tile( object ):
    def __init__( self ):
        self.terrain_set('Plains')
        if self.terrain_get() == 'Mountain':
            self.occupied_set(True)
        else:
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

    def draw( self, screen, xy, imagedict):
        screen.blit(imagedict[self.terrain], xy)
