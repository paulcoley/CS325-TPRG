CS325-TPRG
==========
Version 1:

Currently the overall code structure is based around a single game mode (to be modified
to contain a main menu, info screen, and unit select at a later date). The screen
that is initally visible at this point contains A text message at the top of the screen
stating the goal of the game, also below that message are other lines of text stating the
controls of the game, use the arrow keys to either move closer or further away from your
opponent and the 'a' key to attack the opponent if you are in range.  The currently 
implemented character is a horseman using a sprite of a fire emblem cavalier to save time
creating an avatar from scratch in favor of implementing more units faster and spending more
time to develop the combat system.

The current planned units are all merely variations of my self created Unit class and
the differences in stats are determined by the parameters passed to the class during
construction.  The cavalier is a balanced unit in terms of health, attack, and defense
with his only stand out statistic being the ability to move 3 spaces a turn.  The planned
knight unit is going to be primarily focused on outlasting an opponent with an above average
health and defense rating of 120 and 15 respectively, with the primary drawback of the unit 
being able to only move one space per turn.  The archer unit is a strong attacker with weaker
defensive stats with only being 80 health, 5 defense, but a 15 attack and range of 2 spaces.
(Stats may be altered to balance the game in later testing)


The game itself consists of the players taking turns moving, and then attacking or defending
(details of possible affects of movement on these actions pending more playtesting). You can
move a number of spaces equal to your movement range per turn and then make one attack at this
stage of development. During an attack, your unit's attack plus a random "roll" between 1 and 20
is compared with the opponent's defense value and the difference subtracted from the defender's health.
(subject to change)

On screen above each player's unit, their health is displayed. Between the health values there 
is a number representing the number of spaces between the units currently. In the current state of
the game I have opted to represent distance by that singular linear number for simplicity as 
it allows for a simpler implementation and less bug prone solution to a grid based map right now.

The current implementation planning has stripped out the grid based movement system that I indicated
within the pitch document in favor of a stronger focus on the core mechanics of combat. Also at this
stage in development the players are limited to singular units until gameplay balancing in a 1 vs 1
has been primarily achieved, it is at that state where the grid based implementation will become 
necessary to display all the units controlled by a singular player.

Version 2:

Modified the code to add character select screens for both players and implemented the two additional
characters intended to be within the game.  Also fixed movement code that was found to have a bug
in which turn transfer was not occuring properly when any character attempted to move to retreat
after he or another unit was in attack range.  Added a penalty to attacking when a unit had moved in a turn
to encourage some more mobile units to use their speed to their advantage, seemed to balance out the knight's
superior durability in a stand up fight though more play testing is needed. Currently the player must
re-run the code to play multiple times and is an issue to be addressed soon. Also a splash screen and
conversion of the code to make use of game_modes is also an area to address in the near future along
with an accessible information screen.