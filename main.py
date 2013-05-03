#!/usr/bin/python

import os, pygame, json, random, time
from pygame.locals import *
from utils import *
from modes import *
from gameplay import *

kDataDir = 'data'
kGlobals = 'globals.json'

def main():
    ### Load global variables.
    globals = json.load( open( os.path.join( kDataDir, kGlobals ) ) )
    
    
    ### Initialize pygame.
    pygame.init()
    screen = pygame.display.set_mode( globals['screen_size'] )
    pygame.display.set_caption( globals['window_title'] )
    clock = pygame.time.Clock()
    
    ### Set up the modes.
    modes = ModeManager()
    
    ## The splash screen.
    splash_image, _ = load_image( globals['splash_screen'] )
    modes.register_mode( 'splash_screen', SplashScreen( splash_image, 3000, 'start' ) )

    #Default font
    font = pygame.font.Font( None, 36 )
    
    ## A dummy "select" mode.
    modes.register_mode( 'start', StartScreen() )
    modes.register_mode( 'playing', GamePlayScreen(screen) )
    
    ## Start with the splash screen.
    modes.switch_to_mode( 'splash_screen' )
    
    ### The main loop.
    fps = globals['fps']
    while not modes.quitting():
        clock.tick( fps )
        
        ## Handle Input Events
        for event in pygame.event.get():
            
            if event.type == QUIT:
                break
            
            elif event.type == KEYDOWN:
                modes.current_mode.key_down( event )
            
            elif event.type == KEYUP:
                modes.current_mode.key_up( event )
            
            elif event.type == MOUSEMOTION:
                modes.current_mode.mouse_motion( event )
            
            elif event.type == MOUSEBUTTONUP:
                modes.current_mode.mouse_button_up( event )
            
            elif event.type == MOUSEBUTTONDOWN:
                modes.current_mode.mouse_button_down( event )
        
        modes.current_mode.update( clock )
        modes.current_mode.draw( screen )
    
    
    ### Game over.
    
    ## TODO: Save game state (see pygame.register_quit()).


## this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
