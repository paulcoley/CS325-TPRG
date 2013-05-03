import pygame, math, random
from utils import *
from grid import *
from units import *
from pygame.locals import *

class ModeManager( object ): #Game state code ripped from provided game state system
    '''
    A class that manages switching between modes.
    '''
    
    def __init__( self ):
        self.modes = { '__quitting__': kQuittingMode }
        self.current_mode = None
    
    def register_mode( self, mode_name, mode ):
        '''
        Register a new mode with the mode manager.
        '''
        
        assert mode_name not in self.modes
        self.modes[ mode_name ] = mode
        mode._registered_with_manager( self )
    
    def switch_to_mode( self, mode_name ):
        '''
        Switch to the mode named 'mode_name'.
        Calls exit() on the previous mode and enter() on the new mode.
        Passing None for 'mode_name' quits (terminates the game loop).
        
        NOTE: Switching from a mode to the same mode *does* call exit() and enter().
        '''
        ## Handle the special quitting case.
        if mode_name is None: mode_name = '__quitting__'
        
        assert mode_name in self.modes
        
        if self.current_mode is not None:
            self.current_mode.exit()
        
        self.current_mode = self.modes[ mode_name ]
        
        self.current_mode.enter()
    
    def quitting( self ):
        return self.current_mode is kQuittingMode

class GameMode( object ): #Game state code ripped from provided game state system
    def __init__( self ):
        '''
        A base class for game modes.
        '''
        self.manager = None
    
    def enter( self ):
        '''
        Called when this mode is entered, in case there is set-up to do.
        '''
        pass
    
    def exit( self ):
        '''
        Called when this mode is exited, in case there is tear-down to do
        like stopping music.
        '''
        pass
    
    def switch_to_mode( self, mode_name ):
        '''
        Switches to the specified 'mode_name'.
        
        NOTE: This is simply a convenience method for the current mode which could
              use self.manager.switch_to_mode().
        '''
        assert self.manager is not None
        self.manager.switch_to_mode( mode_name )
    
    def quit( self ):
        '''
        Quits.  This is a convenience method for self.switch_to_mode( None ).
        '''
        self.switch_to_mode( None )
    
    def _registered_with_manager( self, manager ):
        self.manager = manager
    
    def key_down( self, event ):
        pass
    
    def key_up( self, event ):
        pass
    
    def mouse_motion( self, event ):
        pass
    
    def mouse_button_up( self, event ):
        pass
    
    def mouse_button_down( self, event ):
        pass
    
    def update( self, clock ):
        '''
        Called once per frame to update the game state.
        Will be passed the pygame.time.Clock object used by the main loop;
        use the clock object for timing inside this method.
        
        NOTE: It is perfectly OK to ignore the key*() and mouse*() methods above
              and call pygame.mouse.* and pygame.key.* functions here inside update().
        '''
        pass
    
    def draw( self, screen ):
        '''
        Called every time a new frame is to be drawn.
        This method is responsible for clearing the screen and calling
        pygame.display.flip() afterwards.
        Passed the screen pygame.Surface.
        '''
        pass

class SplashScreen( GameMode ): #Game state code ripped from provided game state system
    def __init__( self, image, duration_in_milliseconds, next_mode_name ):
        '''
        Given a duration to show the splash screen 'duration_in_milliseconds',
        and the name of the next mode,
        displays 'image' until either a mouse click or 'duration_in_milliseconds'
        milliseconds have elapsed.
        '''
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image = image
        self.duration = duration_in_milliseconds
        self.next_mode_name = next_mode_name
    
    def enter( self ):
        '''
        Reset the elapsed time and hide the mouse.
        '''
        self.so_far = 0
        pygame.mouse.set_visible( 0 )
    
    def exit( self ):
        '''
        Show the mouse.
        '''
        pygame.mouse.set_visible( 1 )
    
    def draw( self, screen ):
        '''
        Draw the splash screen.
        '''
        screen.blit( self.image, ( 100,0 ) )
        pygame.display.flip()
    
    def update( self, clock ):
        '''
        Update the elapsed time.
        '''
        
        self.so_far += clock.get_time()
        
        ## Have we shown the image long enough?
        if self.so_far > self.duration:
            self.switch_to_mode( self.next_mode_name )
    
    def mouse_button_down( self, event ):
        '''
        Switch on mouse click.
        '''
        self.switch_to_mode( self.next_mode_name )

class StartScreen( GameMode ): #Game state code ripped from provided game state system and modified.
    def __init__( self ):
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image, _ = load_image( 'start_screen.png' )
        self.start, self.start_rect = load_image_alpha( 'start.png' )
        self.quit, self.quit_rect = load_image_alpha( 'quit.png' )
        self.start_rect.topleft = ( 428, 250 )
        self.quit_rect.topleft = ( 428, 350 )
        
        self.mouse_down_pos = (-1,-1)
    
    def mouse_button_down( self, event ):
        self.mouse_down_pos = event.pos
    
    def mouse_button_up( self, event ):
        
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )
        
        if collides_down_and_up( self.quit_rect ):
            self.quit()
        
        if collides_down_and_up( self.start_rect ):
            self.switch_to_mode( 'playing' )

    def key_down( self, event ):
        if event.key == K_ESCAPE:
            self.quit()
    
    def draw( self, screen ):
        ## Draw the HUD.
        screen.blit( self.image, ( 100, 0 ) )
        screen.blit( self.start, ( 428, 250 ) )
        screen.blit( self.quit, ( 428, 350 ) )
        pygame.display.flip()

kQuittingMode = GameMode()
