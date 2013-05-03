import pygame, math, random
from utils import *
from grid import *
from units import *
from modes import *
from pygame.locals import *

class GamePlayScreen( GameMode ): #Responsible for all gameplay in the game
    def __init__( self, screen ):
        random.seed('Shadows of the Knight') #Seed for the chance to hit and miss calculations
        self.currentPlayer = 1 #Tracker for current player
        self.font = pygame.font.Font(None, 26) #Create font for drawing text on the screen
        self.infotxt = self.font.render("Player " + str(self.currentPlayer) + "'s Turn",1,(10,10,10)) #Create render for drawing text that states the current player's turn
        self.imagedict = {'Archer': load_image_alpha_only( 'Archer_single.png' ), #Store images to be drawn in-game to be later called
                          'Cavalier': load_image_alpha_only( 'Cavalier_single.png' ),
                          'Knight': load_image_alpha_only( 'Knight_single.png' ),
                          'Forest': load_onlyimage( 'forest.png'),
                          'Plains': load_onlyimage( 'plains.jpg'),
                          'Mountain': load_onlyimage( 'mountain.png')} # Store unit types to be later called in-game
        self.unitclasses = {'Archer': UnitType( 'Archer', 2, 3, 50, 1, 1),
                            'Cavalier': UnitType( 'Cavalier', 3, 1, 75, 3, 1),
                            'Knight': UnitType( 'Knight', 1, 1, 100, 3, 3)}
        self.units = {'1K1': Unit(self.unitclasses['Knight'], 2, 0, 1), #Create one list of units that stores all the units for both players
                      '1K2': Unit(self.unitclasses['Knight'], 3, 0, 1),
                      '1K3': Unit(self.unitclasses['Knight'], 4, 0, 1),
                      '1K4': Unit(self.unitclasses['Knight'], 5, 0, 1),
                      '1A1': Unit(self.unitclasses['Archer'], 2, 1, 1),
                      '1A2': Unit(self.unitclasses['Archer'], 3, 1, 1),
                      '1A3': Unit(self.unitclasses['Archer'], 4, 1, 1),
                      '1C1': Unit(self.unitclasses['Cavalier'], 2, 2, 1),
                      '1C2': Unit(self.unitclasses['Cavalier'], 3, 2, 1),
                      '2K1': Unit(self.unitclasses['Knight'], 2, 5, 2),
                      '2K2': Unit(self.unitclasses['Knight'], 3, 5, 2),
                      '2K3': Unit(self.unitclasses['Knight'], 4, 5, 2),
                      '2K4': Unit(self.unitclasses['Knight'], 5, 5, 2),
                      '2A1': Unit(self.unitclasses['Archer'], 2, 4, 2),
                      '2A2': Unit(self.unitclasses['Archer'], 3, 4, 2),
                      '2A3': Unit(self.unitclasses['Archer'], 4, 4, 2),
                      '2C1': Unit(self.unitclasses['Cavalier'], 2, 3, 2),
                      '2C2': Unit(self.unitclasses['Cavalier'], 3, 3, 2)}
        self.grid = Grid(screen) #Initialize the grid
        self.currentlySelectedUnit = None #Set the currently selected unit to none
        for x in self.units: #Set the coordinates of all units in the grid to have the occupied property
            self.grid.tilelist[self.units[x].coordinate].occupied = True

    def mouse_button_down( self, event ): #Game State code
        self.mouse_down_pos = event.pos
    
    def mouse_button_up( self, event ):
        
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )

        def attack( attacker, defender ): #Takes care of combat between two units
            x1, x2, y1, y2 = attacker.coordinate[0], defender.coordinate[0], attacker.coordinate[1], defender.coordinate[1]
            dist = math.fabs(x2 - x1) + math.fabs(y2 - y1) #Calculates the distance on the grid between both units
            if(dist <= self.unitclasses[attacker.unit_type].attackRange): # If a unit is close enough to attack, caluclate whether or not the attack is sucessful
                toHit = random.randint(1, 20) + self.unitclasses[attacker.unit_type].attack
                toMiss = random.randint(1, 20) + self.unitclasses[defender.unit_type].defense
                if toHit >= toMiss: #If the Hit sum is higher than the Miss sum, subtract the hit sum from the health of the defending unit and end the attacking unit's turn
                    defender.currentHealth -= toHit
                    attacker.turnTaken = True
                    self.currentlySelectedUnit = None
                    print 'Damage = ' + str(toHit)
                else: #If the Miss sum is higher than the Hit sum, no damage is taken by the defending unit and the attacking unit's turn ends.
                    attacker.turnTaken = True
                    self.currentlySelectedUnit = None
                    print 'Miss'
            else: #If a unit is not close enough to attack, print the appropiate message
                print 'Not close enough'

        def move( mover ): #Takes care of the movement of a unit from grid tile to another.
            x1, x2, y1, y2 = mover.coordinate[0], math.floor(self.mouse_down_pos[0]/100), mover.coordinate[1], math.floor(self.mouse_down_pos[1]/100)
            dist = math.fabs(x2 - x1) + math.fabs(y2 - y1)
            if self.grid.tilelist[(x2, y2)].occupied == True: #If a tile is occupied already, print the appropiate message.
                print 'Can\'t move there because occupied.'
            elif self.unitclasses[mover.unit_type].movementRange < dist: #If a tile is out of movement range, print an appropiate message.
                print 'Can\'t move there because too far.'
            else: #If a tile is within movement range and the user selects it, move the unit to that position and mark that unit as having taken a turn.
                self.grid.tilelist[mover.coordinate].occupied = False
                mover.coordinate = (x2, y2)
                self.grid.tilelist[mover.coordinate].occupied = True
                mover.position = (x2*100, y2*100)
                mover.position_rect.topleft = mover.position
                mover.turnTaken = True
                self.currentlySelectedUnit = None
                
        if self.currentlySelectedUnit == None: #If no unit is selected and the player clicks their mouse, check to see if it collides with one of the current player's units that hasn't taken a turn.
            for x in self.units:
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].turnTaken == False and self.units[x].owner == self.currentPlayer: #If conditions are met, the unit is selected and print out the unit id.
                    self.currentlySelectedUnit = x
                    print x
                    return
        elif self.currentlySelectedUnit != None: #If a unit is selected, check to see if a player clicks on a unit they own, the opposing player's unit, or on an empty tile.
            for x in self.units:
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].turnTaken == False and self.units[x].owner == self.currentPlayer: #If conditions are met, the unit is selected and print out the unit id.
                    self.currentlySelectedUnit = x
                    print x
                    return
            for x in self.units: #If another unit is not selected, then check to see whther the current unit is being told to attack another unit. If so, execute the attack function.
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].owner != self.currentPlayer:
                    attack(self.units[self.currentlySelectedUnit], self.units[x])
                    return
            move(self.units[self.currentlySelectedUnit]) #If the current player doesn't choose another unit or a unit to attack, execute the move function.

    def key_down( self, event ):
        ## By default, quit when the escape key is pressed.
        if event.key == K_ESCAPE:
            self.quit()
        if event.key == K_SPACE and self.currentlySelectedUnit != None: #Skip the turn of a unit by pressing the space bar.
            self.units[self.currentlySelectedUnit].turnTaken = True
            self.currentlySelectedUnit = None

    def update( self, clock ):
        for k, v in self.units.items(): #Remove units that have had their health reduced to less than one and mark the tile as unoccupied.
            if v.currentHealth < 1:
                self.grid.tilelist[self.units[k].coordinate].occupied = False
                del self.units[k]

        takenATurn = 0
        turnsToTake = 0
        for k, v in self.units.items(): #Store the amount of actions the player can take depending on the number of units they have, and record how many they have taken as of thus far.
            if v.owner == self.currentPlayer:
                turnsToTake += 1
                if v.turnTaken == True:
                    takenATurn += 1
        if takenATurn == turnsToTake: #If the number of turns taken equals the number of turns a player can take, then switch players.
            if self.currentPlayer == 1:
                self.currentPlayer = 2
            elif self.currentPlayer == 2:
                self.currentPlayer = 1
            for x in self.units:
                if self.units[x].owner == self.currentPlayer:
                    self.units[x].turnTaken = False
        
        unitCount = 0
        for x in self.units: #Check to see how many units the current player possesses.
            if self.units[x].owner == self.currentPlayer:
                unitCount += 1
        if unitCount == 0: #If a player has no units, they lose.
            print 'Player ' + str(self.currentPlayer) + ' loses'
            self.quit()

    def border( self, screen, color, position ): #Draw a 100x100 square of lines.
        pygame.draw.lines(screen, color, True, [(position),
                                                (position[0] + 100, position[1]),
                                                (position[0] + 100, position[1] + 100),
                                                (position[0], position[1] + 100)])

    def draw( self, screen ): #Draw everything in the gameplay
        screen.fill((255, 255, 255))
        self.grid.draw(screen, self.imagedict) #Draw the grid
        self.infotxt = self.font.render("Player " + str(self.currentPlayer) + "'s Turn",1,(10,10,10))
        for x in self.units: #Draw units in their appropiate places on the grid.
            self.units[x].draw(screen, self.imagedict)
            if self.units[x].owner == 1: #Player 1 is red
                self.border(screen, (255, 0, 0), self.units[x].position)
            if self.units[x].owner == 2: #Player 2 is blue
                self.border(screen, (0, 0, 255), self.units[x].position)
            if self.currentlySelectedUnit != None and self.units[x].owner == self.currentPlayer: #The currently selected unit is yellow.
                self.border(screen, (255, 255, 0), self.units[self.currentlySelectedUnit].position)
        screen.blit(self.infotxt, (50, 30)) #Print who is the current player
        pygame.display.flip()
