import pygame, math, random
from utils import *
from grid import *
from units import *
from pygame.locals import *

class ModeManager( object ):
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

class GameMode( object ):
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
		
class SplashScreen( GameMode ):
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
        screen.blit( self.image, ( 0,0 ) )
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

class StartScreen( GameMode ):
    def __init__( self ):
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image, _ = load_image( 'start_screen.png' )
        self.start, self.start_rect = load_image_alpha( 'start.png' )
        self.quit, self.quit_rect = load_image_alpha( 'quit.png' )
        self.start_rect.topleft = ( 271, 30 )
        self.quit_rect.topleft = ( 255, 150 )
        
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
    
    def draw( self, screen ):
        ## Draw the HUD.
        screen.blit( self.image, ( 0,0 ) )
        screen.blit( self.start, ( 271, 30 ) )
        screen.blit( self.quit, ( 255, 150 ) )
        pygame.display.flip()

class GamePlayScreen( GameMode ):
    def __init__( self, screen ):
        random.seed('Shadows of the Knight')
        self.currentPlayer = 1
        self.font = pygame.font.Font(None, 26)
        self.infotxt = self.font.render("Player " + str(self.currentPlayer) + "'s Turn",1,(10,10,10))
        self.imagedict = {'Archer': load_image_alpha_only( 'Archer_single.png' ),
                          'Cavalier': load_image_alpha_only( 'Cavalier_single.png' ),
                          'Knight': load_image_alpha_only( 'Knight_single.png' ),
                          'Forest': load_onlyimage( 'forest.png'),
                          'Plains': load_onlyimage( 'plains.jpg'),
                          'Mountain': load_onlyimage( 'mountain.png'),
                          'Player1': load_image_alpha_only('Player1_Color.png'),
                          'Player2': load_image_alpha_only('Player2_Color.png'),
                          'Select': load_image_alpha_only('PlayerSelect_Color.png')}
        self.unitclasses = {'Archer': UnitType( 'Archer', 2, 3, 50, 1, 1),
                            'Cavalier': UnitType( 'Cavalier', 3, 1, 75, 3, 1),
                            'Knight': UnitType( 'Knight', 1, 1, 100, 3, 3)}
        self.player1units = {'1K1': Unit(self.unitclasses['Knight'], 2, 0),
                             '1K2': Unit(self.unitclasses['Knight'], 3, 0),
                             '1K3': Unit(self.unitclasses['Knight'], 4, 0),
                             '1K4': Unit(self.unitclasses['Knight'], 5, 0),
                             '1A1': Unit(self.unitclasses['Archer'], 2, 1),
                             '1A2': Unit(self.unitclasses['Archer'], 3, 1),
                             '1A3': Unit(self.unitclasses['Archer'], 4, 1),
                             '1C1': Unit(self.unitclasses['Cavalier'], 2, 2),
                             '1C2': Unit(self.unitclasses['Cavalier'], 3, 2)}
        self.player2units = {'2K1': Unit(self.unitclasses['Knight'], 2, 5),
                             '2K2': Unit(self.unitclasses['Knight'], 3, 5),
                             '2K3': Unit(self.unitclasses['Knight'], 4, 5),
                             '2K4': Unit(self.unitclasses['Knight'], 5, 5),
                             '2A1': Unit(self.unitclasses['Archer'], 2, 4),
                             '2A2': Unit(self.unitclasses['Archer'], 3, 4),
                             '2A3': Unit(self.unitclasses['Archer'], 4, 4),
                             '2C1': Unit(self.unitclasses['Cavalier'], 2, 3),
                             '2C2': Unit(self.unitclasses['Cavalier'], 3, 3)}
        self.grid = Grid(screen)
        self.currentlySelectedUnit = None
        for x in self.player1units:
            self.grid.tilelist[self.player1units[x].coordinate].occupied = True
        for x in self.player2units:
            self.grid.tilelist[self.player2units[x].coordinate].occupied = True

    def mouse_button_down( self, event ):
        self.mouse_down_pos = event.pos
    
    def mouse_button_up( self, event ):
        
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )

        def attack( attacker, defender ):
            #Work on this
            x1, x2, y1, y2 = attacker.coordinate[0], defender.coordinate[0], attacker.coordinate[1], defender.coordinate[1]
            dist = math.fabs(x2 - x1) + math.fabs(y2 - y1)
            if(dist <= self.unitclasses[attacker.unit_type].attackRange):
                toHit = random.randint(1, 20) + self.unitclasses[attacker.unit_type].attack
                toMiss = random.randint(1, 20) + self.unitclasses[defender.unit_type].defense
                print dist
                if toHit >= toMiss:
                    defender.currentHealth -= toHit
                    attacker.turnTaken = True
                    self.currentlySelectedUnit = None
                    print 'Close enough'
                else:
                    attacker.turnTaken = True
                    self.currentlySelectedUnit = None
                    print 'Miss'
            else:
                print 'Not close enough'

        def move( mover ):
            x1, x2, y1, y2 = mover.coordinate[0], math.floor(self.mouse_down_pos[0]/100), mover.coordinate[1], math.floor(self.mouse_down_pos[1]/100)
            dist = math.fabs(x2 - x1) + math.fabs(y2 - y1)
            if self.grid.tilelist[(x2, y2)].occupied == True:
                print 'Can\'t move there because occupied.'
            elif self.unitclasses[mover.unit_type].movementRange < dist:
                print 'Can\'t move there because too far.'
            else:
                print dist
                self.grid.tilelist[mover.coordinate].occupied = False
                mover.coordinate = (x2, y2)
                self.grid.tilelist[mover.coordinate].occupied = True
                mover.position = (x2*100, y2*100)
                mover.position_rect.topleft = mover.position
                mover.turnTaken = True
                self.currentlySelectedUnit = None
                

        if self.currentlySelectedUnit == None:
            if self.currentPlayer == 1:
                for x in self.player1units:
                    if collides_down_and_up(self.player1units[x].position_rect) and self.player1units[x].turnTaken == False:
                        self.currentlySelectedUnit = x
                        print x
                        return
            if self.currentPlayer == 2:
                for x in self.player2units:
                    if collides_down_and_up(self.player2units[x].position_rect)  and self.player2units[x].turnTaken == False:
                        self.currentlySelectedUnit = x
                        print x
                        return
        elif self.currentlySelectedUnit != None:
            if self.currentPlayer == 1:
                for x in self.player1units:
                    if collides_down_and_up(self.player1units[x].position_rect) and self.player1units[x].turnTaken == False:
                        self.currentlySelectedUnit = x
                        print x
                        return
                for x in self.player2units:
                    if collides_down_and_up(self.player2units[x].position_rect):
                        attack(self.player1units[self.currentlySelectedUnit], self.player2units[x])
                        return
                move(self.player1units[self.currentlySelectedUnit])
            if self.currentPlayer == 2:
                for x in self.player2units:
                    if collides_down_and_up(self.player2units[x].position_rect) and self.player2units[x].turnTaken == False:
                        self.currentlySelectedUnit = x
                        print x
                        return
                for x in self.player1units:
                    if collides_down_and_up(self.player1units[x].position_rect):
                        attack(self.player2units[self.currentlySelectedUnit], self.player1units[x])
                        return
                move(self.player2units[self.currentlySelectedUnit])

    def key_down( self, event ):
        ## By default, quit when the escape key is pressed.
        if event.key == K_ESCAPE:
            self.quit()
        if event.key == K_SPACE and self.currentlySelectedUnit != None:
            if self.currentPlayer == 1:
                self.player1units[self.currentlySelectedUnit].turnTaken = True
                self.currentlySelectedUnit = None
            if self.currentPlayer == 2:
                self.player2units[self.currentlySelectedUnit].turnTaken = True
                self.currentlySelectedUnit = None

    def update( self, clock ):
        for k, v in self.player1units.items():
            if v.currentHealth < 1:
                self.grid.tilelist[self.player1units[k].coordinate].occupied = False
                del self.player1units[k]

        for k, v in self.player2units.items():
            if v.currentHealth < 1:
                self.grid.tilelist[self.player2units[k].coordinate].occupied = False
                del self.player2units[k]

        if self.currentPlayer == 1:
            takenATurn = 0
            for k, v in self.player1units.items():
                if v.turnTaken == True:
                    takenATurn += 1
            if takenATurn == len(self.player1units):
                self.currentPlayer = 2
                for x in self.player1units:
                    self.player1units[x].turnTaken = False
            if len(self.player2units) == 0:
                print 'Player 1 Wins!'
                self.quit()

        if self.currentPlayer == 2:
            takenATurn = 0
            for k, v in self.player2units.items():
                if v.turnTaken == True:
                    takenATurn += 1
            if takenATurn == len(self.player2units):
                self.currentPlayer = 1
                for x in self.player2units:
                    self.player2units[x].turnTaken = False
            if len(self.player1units) == 0:
                print 'Player 2 Wins!'
                self.quit()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.grid.draw(screen, self.imagedict)
        self.infotxt = self.font.render("Player " + str(self.currentPlayer) + "'s Turn",1,(10,10,10))
        for x in self.player1units:
            self.player1units[x].draw(screen, self.imagedict)
            screen.blit(self.imagedict['Player1'], self.player1units[x].position)
            if self.currentlySelectedUnit != None and self.currentPlayer == 1:
                screen.blit(self.imagedict['Select'], self.player1units[self.currentlySelectedUnit].position)
        for x in self.player2units:
            self.player2units[x].draw(screen, self.imagedict)
            screen.blit(self.imagedict['Player2'], self.player2units[x].position)
            if self.currentlySelectedUnit != None and self.currentPlayer == 2:
                screen.blit(self.imagedict['Select'], self.player2units[self.currentlySelectedUnit].position)
        screen.blit(self.infotxt, (50, 30))
        pygame.display.flip()


kQuittingMode = GameMode()
