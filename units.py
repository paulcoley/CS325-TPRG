import pygame
from utils import *
from pygame.locals import *

class UnitType( object ): #Stores the general information of a unit type
    def __init__( self, imagetype, movementRange, attackRange, health, attack, defense):
        self.image = imagetype
        self.movementRange = movementRange
        self.attackRange = attackRange
        self.health = health
        self.attack = attack
        self.defense = defense

class Unit( pygame.sprite.Sprite): #Stores information about an instance of a unit
    def __init__(self, utype, x, y, owner):
        pygame.sprite.Sprite.__init__(self)
        self.currentHealth = utype.health #Unit's current health
        self.maxHealth = utype.health #Unit's max health
        self.unit_type = utype.image #Unit's type
        self.coordinate = (x, y) #Coordinates relative to the grid
        self.position = (x*100,y*100) #Real position relative to the screen
        self.position_rect = Rect(self.position, (100, 100)) #Rect for collisions
        self.turnTaken = False #Whether a unit has taken an action
        self.owner = owner #Which player owns this unit

    def draw(self, screen, imagedict): #Draws the unit on the screen using its real position and its healthbar
        screen.blit(imagedict[self.unit_type], self.position)
        pygame.draw.line(screen,
                         (255, 255, 255),
                         (self.position[0], self.position[1] + 97),
                         (self.position[0] + 100, self.position[1] + 97),
                         5)
        pygame.draw.line(screen,
                         (255, 0, 0),
                         (self.position[0], self.position[1] + 97),
                         (self.position[0] + 100*(float(self.currentHealth)/float(self.maxHealth)), self.position[1] + 97),
                         5)
