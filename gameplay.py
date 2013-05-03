import pygame, math, random
from utils import *
from grid import *
from units import *
from modes import *
from pygame.locals import *

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
        self.units = {'1K1': Unit(self.unitclasses['Knight'], 2, 0, 1),
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
        self.grid = Grid(screen)
        self.currentlySelectedUnit = None
        for x in self.units:
            self.grid.tilelist[self.units[x].coordinate].occupied = True

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
                toMiss = 0 #random.randint(1, 20) + self.unitclasses[defender.unit_type].defense
                print dist
                if toHit >= toMiss:
                    defender.currentHealth -= toHit
                    attacker.turnTaken = True
                    self.currentlySelectedUnit = None
                    print 'Damage = ' + str(toHit)
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
                self.grid.tilelist[mover.coordinate].occupied = False
                mover.coordinate = (x2, y2)
                self.grid.tilelist[mover.coordinate].occupied = True
                mover.position = (x2*100, y2*100)
                mover.position_rect.topleft = mover.position
                mover.turnTaken = True
                self.currentlySelectedUnit = None
                
        if self.currentlySelectedUnit == None:
            for x in self.units:
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].turnTaken == False and self.units[x].owner == self.currentPlayer:
                    self.currentlySelectedUnit = x
                    print x
                    return
        elif self.currentlySelectedUnit != None:
            for x in self.units:
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].turnTaken == False and self.units[x].owner == self.currentPlayer:
                    self.currentlySelectedUnit = x
                    print x
                    return
            for x in self.units:
                if collides_down_and_up(self.units[x].position_rect) and self.units[x].owner != self.currentPlayer:
                    attack(self.units[self.currentlySelectedUnit], self.units[x])
                    return
            move(self.units[self.currentlySelectedUnit])

    def key_down( self, event ):
        ## By default, quit when the escape key is pressed.
        if event.key == K_ESCAPE:
            self.quit()
        if event.key == K_SPACE and self.currentlySelectedUnit != None:
            self.units[self.currentlySelectedUnit].turnTaken = True
            self.currentlySelectedUnit = None

    def update( self, clock ):
        for k, v in self.units.items():
            if v.currentHealth < 1:
                self.grid.tilelist[self.units[k].coordinate].occupied = False
                del self.units[k]

        takenATurn = 0
        turnsToTake = 0
        for k, v in self.units.items():
            if v.owner == self.currentPlayer:
                turnsToTake += 1
                if v.turnTaken == True:
                    takenATurn += 1
        if takenATurn == turnsToTake:
            if self.currentPlayer == 1:
                self.currentPlayer = 2
            elif self.currentPlayer == 2:
                self.currentPlayer = 1
            for x in self.units:
                if self.units[x].owner == self.currentPlayer:
                    self.units[x].turnTaken = False
        
        unitCount = 0
        for x in self.units:
            if self.units[x].owner == self.currentPlayer:
                unitCount += 1
        if unitCount == 0:
            print 'Player ' + str(self.currentPlayer) + ' loses'
            self.quit()

    def border( self, screen, color, position ):
        pygame.draw.lines(screen, color, True, [(position),
                                                (position[0] + 100, position[1]),
                                                (position[0] + 100, position[1] + 100),
                                                (position[0], position[1] + 100)])

    def draw( self, screen ):
        screen.fill((255, 255, 255))
        self.grid.draw(screen, self.imagedict)
        self.infotxt = self.font.render("Player " + str(self.currentPlayer) + "'s Turn",1,(10,10,10))
        for x in self.units:
            self.units[x].draw(screen, self.imagedict)
            if self.currentPlayer == 1:
                self.border(screen, (255, 0, 0), self.units[x].position)
            if self.currentPlayer == 2:
                self.border(screen, (0, 0, 255), self.units[x].position)
            if self.currentlySelectedUnit != None and self.units[x].owner == self.currentPlayer:
                self.border(screen, (255, 255, 0), self.units[self.currentlySelectedUnit].position)
        screen.blit(self.infotxt, (50, 30))
        pygame.display.flip()
