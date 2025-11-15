Abdul spaceship game is a 2 player 2D space shooter game built using pygame.
player control spaceship and try to hit each other while taking in consideration the obstacles and trying to collect power ups . The game ends when one players health reaches zero.

Player1:
Controls: WASD for movement and left ctrl for shooting

Player2:
Controls: arrow keys  for movement and right ctrl for shooting

How to Run the Game:
Requirements:

	Python 3.x
	Pygame (install with pip install pygame)

Assets Folder:

	Ensure there is an Assets folder in the same directory with:
	spaceship_yellow.png
	spaceship_red.png
	space.png

Spaceship class:
Encapsulates player  properties like health, movement , shooting and controls

Bullet class:
Represents bullets shot by spaceship with movement and collision detection

obstacle class:
rectangular size obstacle formed randomly on the screen which blocks bullet

powerup class:
a green small rectangle that spawns randomly and increases health by 1 till max

rapid fire power up:
an orange power-up that make the player fire rapidly for 5 seconds

draw health bar:
display each spaceships current health at the top of screen





