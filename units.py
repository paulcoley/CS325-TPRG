import pygame
from utils import *

class Unit( pygame.sprite.Sprite):
	def __init__(self, utype, x, y):
		pygame.sprite.Sprite.__init__(self)
		##load image and rect based on unit type
		self.attacking = 0
		if (utype == 1):
			self.image, self.rect = load_image('Cavalier_single.gif', -1)
			screen = pygame.display.get_surface()
			self.area = screen.get_rect()
			self.rect.topleft = x, y
			self.move_r = 3
			self.health = 100
			self.attack = 10
			self.defense = 10
			self.arange = 1
		elif(utype == 2):
			self.image, self.rect = load_image('Archer_single.gif', -1)
			screen = pygame.display.get_surface()
			self.area = screen.get_rect()
			self.rect.topleft = x, y
			self.move_r = 2
			self.health = 80
			self.attack = 15
			self.defense = 5
			self.arange = 2
		elif(utype == 3):
			self.image, self.rect = load_image('Knight_single.gif', -1)
			screen = pygame.display.get_surface()
			self.area = screen.get_rect()
			self.rect.topleft = x, y
			self.move_r = 1
			self.health = 120
			self.attack = 10
			self.defense = 15
			self.arange = 1
