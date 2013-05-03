import pygame
from utils import *
from pygame.locals import *

class UnitType( object ):
    def __init__( self, imagetype, movementRange, attackRange, health, attack, defense):
        self.image = imagetype
        self.movementRange = movementRange
        self.attackRange = attackRange
        self.health = health
        self.attack = attack
        self.defense = defense

class Unit( pygame.sprite.Sprite):
    def __init__(self, utype, x, y, owner):
        pygame.sprite.Sprite.__init__(self)
        self.currentHealth = utype.health
        self.unit_type = utype.image
        self.coordinate = (x, y)
        self.position = (x*100,y*100)
        self.position_rect = Rect(self.position, (100, 100))
        self.turnTaken = False
        self.owner = owner

    def draw(self, screen, imagedict):
        screen.blit(imagedict[self.unit_type], self.position)
