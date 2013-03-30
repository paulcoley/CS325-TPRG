#!/usr/bin/env python2.7

import os, pygame
from random import randint
from pygame.locals import *

def load_image( name, colorkey = None ):
    '''
    Given a filename 'name' in the data directory and
    a color 'colorkey' whose RGB value (or color map index) will be treated as transparent,
    loads the image and returns a pygame.Surface.
    
    NOTE: The default 'colorkey' parameter, None, causes the image
          to be entirely opaque.
    NOTE: The special 'colorkey' value of -1 causes the top-left pixel color
          in the image to be used as the transparent color.
    '''
    
    ## Find 'name' within the 'data' directory independent of
    ## operating system path character.
    fullname = os.path.join( 'data', name )
    try:
        image = pygame.image.load( fullname )
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at( (0,0) )
        ## accelerate
        image.set_colorkey( colorkey, RLEACCEL )
    return image, image.get_rect()

def load_sound( name ):
    '''
    Given a filename 'name' in the data directory,
    loads the sound and returns a pygame.mixer.Sound().
    If sound functionality is not available, returns a dummy sound object
    whose play() method is a no-op.
    '''
    
    class NoneSound:
        def play( self ): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    
    fullname = os.path.join( 'data', name )
    try:
        sound = pygame.mixer.Sound( fullname )
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    
    return sound
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
			
	def update(self):
		##if self.attacking, play sprite animation
		return
	##def _Attack(self):
		##
		
def main():
	pygame.init()
	screen = pygame.display.set_mode ((800,400))
	pygame.display.set_caption("Tactical Warfare")
	pygame.mouse.set_visible(1)
	
	background = pygame.Surface( screen.get_size() )
	background = background.convert()
	background.fill((250,250,250))
	
	
	unit_seperation = 5
	
	player1 = None
	player2 = None
	
	player1win = False
	player2win = False
	
	player1turn = True
	# implement a while loop to handle character selection
	while player1 == None:
		if pygame.font:
			font = pygame.font.Font(None, 26)
			infotxt = font.render("Player 1 please press the key to the corresponding unit you would like to have:",1,(10,10,10))
			background.blit(infotxt, (50, 30))
			infotxt = font.render(" 1) Cavalier: 3 movement, 1 attack range, 100 health, 10 attack, 10 defense",1,(10,10,10))
			background.blit(infotxt, (100, 50))
			infotxt = font.render(" 2) Archer: 2 movement, 2 attack range, 80 health, 15 attack, 5 defense",1,(10,10,10))
			background.blit(infotxt, (100, 70))
			infotxt = font.render(" 3) Knight: 1 movement, 1 attack range, 120 health, 10 attack, 15 defense",1,(10,10,10))
			background.blit(infotxt, (100, 90))
			screen.blit(background, (0, 0))
			
			pygame.display.flip()
			
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					return
				elif event.type == KEYDOWN and event.key == K_1:
					player1 = Unit(1, 200, 200)
					background.fill((250,250,250))
				elif event.type == KEYDOWN and event.key == K_2:
					player1 = Unit(2, 200, 200)
					background.fill((250,250,250))
				elif event.type == KEYDOWN and event.key == K_3:
					player1 = Unit(3, 200, 200)
					background.fill((250,250,250))
	while player2 == None:
		if pygame.font:
			font = pygame.font.Font(None, 26)
			infotxt = font.render("Player 2 please press the key to the corresponding unit you would like to have:",1,(10,10,10))
			background.blit(infotxt, (50, 30))
			infotxt = font.render(" 1) Cavalier: 3 movement, 1 attack range, 100 health, 10 attack, 10 defense",1,(10,10,10))
			background.blit(infotxt, (100, 50))
			infotxt = font.render(" 2) Archer: 2 movement, 2 attack range, 80 health, 15 attack, 5 defense",1,(10,10,10))
			background.blit(infotxt, (100, 70))
			infotxt = font.render(" 3) Knight: 1 movement, 1 attack range, 120 health, 10 attack, 15 defense",1,(10,10,10))
			background.blit(infotxt, (100, 90))
			screen.blit(background, (0, 0))
			
			pygame.display.flip()
			
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					return
				elif event.type == KEYDOWN and event.key == K_1:
					player2 = Unit(1, 600, 200)
					background.fill((250,250,250))
				elif event.type == KEYDOWN and event.key == K_2:
					player2 = Unit(2, 600, 200)
					background.fill((250,250,250))
				elif event.type == KEYDOWN and event.key == K_3:
					player2 = Unit(3, 600, 200)
					background.fill((250,250,250))
	
	moves_remaining = player1.move_r
	
	allsprites = pygame.sprite.OrderedUpdates( ( player1, player2 ) )
	
	if pygame.font:
		font = pygame.font.Font(None, 18)
		infotxt = font.render("Left arrow key moves away from opponent, Right arrow moves toward opponent",1,(10,10,10))
		background.blit(infotxt, (150, 30))
		infotxt = font.render("Press the a key to make an attack against your opponent.",1,(10,10,10))
		background.blit(infotxt, (200, 50))
		
		
		font = pygame.font.Font(None, 36)
		text = font.render("Defeat your opponent by reducing their health to 0",1,(10,10,10))
		textpos = text.get_rect(centerx = background.get_width()/2)
		background.blit(text,textpos)
		
		healthtxt1 = font.render(str(player1.health), 1, (10,10,10))
		background.blit(healthtxt1, (200,150))
		healthtxt2 = font.render(str(player2.health), 1, (10,10,10))
		background.blit(healthtxt2, (600,150))
		
		distancetxt = font.render(str(unit_seperation), 1, (10,10,10))
		background.blit(distancetxt, (400,150))
		
		screen.blit(background, (0,0))
		pygame.display.flip()
		
	clock = pygame.time.Clock()
	
	while True:
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == KEYDOWN and event.key == K_a:
				if player1turn == True and unit_seperation == player1.arange:
					temprand = randint(1, 20)
					tempatt = player1.attack + temprand
					if moves_remaining != player1.move_r:
						tempatt = tempatt - 5
					if tempatt > player2.defense:
						player2.health = player2.health-tempatt
					player1turn = False
					moves_remaining = player2.move_r
					if player2.health <= 0:
						player1win = True
				elif player1turn == False and unit_seperation == player2.arange:
					temprand = randint(1, 20)
					tempatt = player2.attack + temprand
					if moves_remaining != player2.move_r:
						tempatt = tempatt - 5
					if tempatt > player1.defense:
						player1.health = player1.health-tempatt
					player1turn = True
					moves_remaining = player1.move_r
					if player1.health <= 0:
						player2win = True
				background.fill((250,250,250))
			##elif event.type == KEYDOWN and event.key == K_d:
			##	defense action
			elif event.type == KEYDOWN and event.key == K_LEFT:
				if player1turn == True and moves_remaining > 0:
					unit_seperation = unit_seperation + 1
					moves_remaining = moves_remaining - 1
					if moves_remaining == 0 and unit_seperation != player1.arange:
						player1turn = False
						moves_remaining = player2.move_r
					background.fill((250,250,250))
				elif player1turn == False and moves_remaining > 0:
					unit_seperation = unit_seperation + 1
					moves_remaining = moves_remaining - 1
					if moves_remaining == 0 and unit_seperation != player2.arange:
						player1turn = True
						moves_remaining = player1.move_r
					background.fill((250,250,250))
			elif event.type == KEYDOWN and event.key == K_RIGHT:
				if player1turn == True and moves_remaining > 0 and unit_seperation > 1:
					unit_seperation = unit_seperation - 1
					moves_remaining = moves_remaining - 1
					if moves_remaining == 0 and unit_seperation != player1.arange:
						player1turn = False
						moves_remaining = player2.move_r
					background.fill((250,250,250))
				elif player1turn == False and moves_remaining > 0 and unit_seperation > 1:
					unit_seperation = unit_seperation - 1
					moves_remaining = moves_remaining - 1
					if moves_remaining == 0 and unit_seperation != player2.arange:
						player1turn = True
						moves_remaining = player1.move_r
					background.fill((250,250,250))
		
		
        	## Draw Everything
        	if player1win == False and player2win == False:
        		allsprites.update()
			screen.blit(background, (0, 0))
        		allsprites.draw(screen)
        		
        		healthtxt1 = font.render(str(player1.health), 1, (10,10,10))
        		background.blit(healthtxt1, (200,150))
        		healthtxt2 = font.render(str(player2.health), 1, (10,10,10))
        		background.blit(healthtxt2, (600,150))
        		
        		if(player1turn == True):
        			turntxt = font.render("Player 1's turn",1,(10,10,10))
        		elif(player1turn == False):
        			turntxt = font.render("Player 2's turn",1,(10,10,10))
        		background.blit(turntxt, (300,100))
        		
			distancetxt = font.render(str(unit_seperation), 1, (10,10,10))
			background.blit(distancetxt, (400,150))
		else:
			font = pygame.font.Font(None, 24) 
			if player1win == True:
				screen.blit(background, (0, 0))
				wintxt = font.render("Congratulations player 1 you won the match. Press the escape key to exit.",1, (10,10,10))
				textpos = text.get_rect( centerx = background.get_width()/2 , centery = background.get_height()/2)
				background.blit(wintxt, textpos)
			if player2win == True:
				screen.blit(background, (0, 0))
				wintxt = font.render("Congratulations player 2 you won the match. Press the escape key to exit.",1, (10,10,10))
				textpos = text.get_rect( centerx = background.get_width()/2 , centery = background.get_height()/2)
				background.blit(wintxt, textpos)
        	
		pygame.display.flip()
        	
if __name__ == '__main__': main()
