import pygame
from utils import *
from pygame.locals import *

class UnitType( object ):
        def __init__( self, imagetype, movementRange, attackRange, health, attack, defense):
                self.image_set(imagetype)
                self.movementRange_set(movementRange)
                self.attackRange_set(attackRange)
                self.health_set(health)
                self.attack_set(attack)
                self.defense_set(defense)

        def image_get( self ):
                return self._image

        def image_set( self, value):
                self._image = value

        image = property(image_get, image_set)

        def movementRange_get( self ):
                return self._movementRange

        def movementRange_set( self, value ):
                self._movementRange = value

        movementRange = property(movementRange_get, movementRange_set)

        def attackRange_get( self ):
                return self._attackRange

        def attackRange_set( self, value ):
                self._attackRange = value

        attackRange = property(attackRange_get, attackRange_set)

        def health_get( self ):
                return self._health

        def health_set( self, value ):
                self._health = value

        health = property(health_get, health_set)

        def health_get( self ):
                return self._health

        def health_set( self, value ):
                self._health = value

        health = property(health_get, health_set)

        def attack_get( self ):
                return self._attack

        def attack_set( self, value ):
                self._attack = value

        attack = property(attack_get, attack_set)

        def defense_get( self ):
                return self._defense

        def defense_set( self, value ):
                self._defense = value

        defense = property(defense_get, defense_set)

class Unit( pygame.sprite.Sprite):
	def __init__(self, utype, xy, owner):
                pygame.sprite.Sprite.__init__(self)
		self.currentHealth = utype.health
		self.image = utype.image
		x, y = xy

	def draw(self, screen, imagedict):
                screen.blit(imagedict[self.image], (x, y))
