import pygame 
import os
import random

pygame.init() 
pygame.font.init()
pygame.mixer.init()
# Initializes Pygame, font, and mixer modules


Width, Height = 900, 500
fps = 60
speed = 5
bullet_speed = 7
max_bullets = 3
spaceship_size = (60, 50)
obstacle_size = (40, 40)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
gray = (60, 60, 60)
obstacle_color = (100, 100, 100)

Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("ABDUL Spaceship Game")
#creates game window and set the title of the game

seperator = pygame.Rect(Width // 2- 5, 0, 10, Height)
#draw a black border in the middle of the screen as seperator between 2 players

laser_sound = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))
hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
powerup_sound = pygame.mixer.Sound(os.path.join('Assets', 'powerup.mp3'))
win_sound = pygame.mixer.Sound(os.path.join('Assets', 'win.mp3'))
# initializing the sound effects

yellow_image = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')), spaceship_size), 90)
red_image = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), spaceship_size), 270)
background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (Width, Height))
#load the spaceship and scale and rotate ships so they are facing each other

health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comicsans', 100)


yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2
#Custom event IDs to track collisions.



class Spaceship:
    def __init__(self, x, y, image, controls, facing):
        self.rect = pygame.Rect(x, y, *spaceship_size)
        self.image = image
        self.controls = controls
        self.facing = facing
        self.bullets = []
        self.health = 10
        self.max_health = 10
        self.rapid_fire = False
        self.rapid_fire_end_time = 0
        #initialise movement keys, direction, bullet list, health values, and rapid fire state.

    def move(self, keys):
        #Moves spaceship left if within allowed area

        if keys[self.controls['left']] and self.rect.x - speed > self.controls['x_min']:
            self.rect.x -= speed
        if keys[self.controls['right']] and self.rect.x + speed + self.rect.width < self.controls['x_max']:
            self.rect.x += speed
        if keys[self.controls['up']] and self.rect.y - speed > 0:
            self.rect.y -= speed
        if keys[self.controls['down']] and self.rect.y + speed + self.rect.height < Height:
            self.rect.y += speed
        # Handles movement in all directions, preventing out-of-bounds.

    def shoot(self):
        # Fires bullets based on current direction, respects max_bullets or rapid_fire.
        if len(self.bullets) < max_bullets or self.rapid_fire:
            direction = 1 if self.facing == 'right' else -1
            bullet_x = self.rect.right if direction == 1 else self.rect.left - 10
            bullet_y = self.rect.centery - 2
            laser_sound.play()
            self.bullets.append(Bullet(bullet_x, bullet_y, direction))

    def draw(self):
        Window.blit(self.image, (self.rect.x, self.rect.y))
        # Draws the spaceship on the screen.


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.direction = direction
    #  first line defines a rectabngle box for the bullet hit
    #  define movement direction
    def move(self):
        self.rect.x += bullet_speed * self.direction
    # Moves the bullet horizontally.

    def draw(self):
        color = yellow if self.direction == 1 else red
        pygame.draw.rect(Window, color, self.rect)
    # Draws the bullet in the corresponding color.

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *obstacle_size)
    def draw(self):
        pygame.draw.rect(Window, obstacle_color, self.rect)
    #draw a rectangle box that blocks bullet
class healthPowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, Width - 120), random.randint(50, Height - 70), 20, 20)
        self.active = True
# a rectangle box that spawn at random location
    def apply(self, ship):
        if self.active and self.rect.colliderect(ship.rect): 
            ship.health = min(ship.health + 1, ship.max_health)
            self.active = False
            powerup_sound.play()
# adds 1 health (up to max), then dissapear after collecting as self. active turns to false
    def draw(self):
        if self.active:
            pygame.draw.rect(Window, (0, 222, 121), self.rect)
#  draws a rectangle 
class RapidFirePowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, Width - 120), random.randint(50, Height - 70), 20, 20)
        self.active = True

    def apply(self, ship):
        if self.active and self.rect.colliderect(ship.rect):
            ship.rapid_fire = True
            ship.rapid_fire_end_time = pygame.time.get_ticks() + 5000
            self.active = False
#  a rapid fire power up for 5 seconds 
    def draw(self):
        if self.active:
            pygame.draw.rect(Window, (255, 100, 0), self.rect)

def draw_health_bar(x, y, current, max_val, color):
    bar_width = max_val * 10
    fill = int((current / max_val) * bar_width)
    pygame.draw.rect(Window, color, (x, y, fill, 12))
    pygame.draw.rect(Window, white, (x, y, bar_width, 12), 2)
# Renders a colored health bar with white border.

def draw_window(yellow_ship, red_ship, powerup, rapid_powerup, obstacles):
    Window.blit(background, (0,0))
    pygame.draw.rect(Window, black, seperator)
    draw_health_bar(10, 10, yellow_ship.health, yellow_ship.max_health, yellow)
    draw_health_bar(Width - 10 - red_ship.max_health * 10, 10, red_ship.health, red_ship.max_health, red)
# draws bacground , seperator, and health ber for yellow and red ship
    for obj in [*obstacles, yellow_ship, red_ship, powerup, rapid_powerup, *yellow_ship.bullets, *red_ship.bullets]:
        obj.draw()
    pygame.display.update()
#  draws all object and update them on screen

def handle_bullets(yellow_ship, red_ship, obstacles):
# Moves bullets and checks for hits on players or obstacles.
    for ship, target, event in [(yellow_ship, red_ship, red_hit), (red_ship, yellow_ship, yellow_hit)]:
        for bullet in ship.bullets[:]:
# Iterates over a copy of the bullet list using
            bullet.move()
            if bullet.rect.colliderect(target.rect):
# Checks if the bullet hits the enemy ship using Pygame’s colliderect(), which returns True if two rectangles overlap.
                pygame.event.post(pygame.event.Event(event))
                ship.bullets.remove(bullet)
            elif bullet.rect.right < 0 or bullet.rect.left > Width:
                ship.bullets.remove(bullet)
            else:
                for obs in obstacles:
                    if bullet.rect.colliderect(obs.rect):
                        ship.bullets.remove(bullet)
#  If it does, the bullet is removed, and we break out of the inner loop to avoid redundant checks — the bullet is already destroyed.
                        break

def draw_winner(text):
    text_surface = winner_font.render(text, True, white)
    Window.blit(text_surface, (Width // 2 - text_surface.get_width() // 2, Height // 2 - text_surface.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
# Displays a winning message for 5 seconds.


def main():
    yellow = Spaceship(100, 300, yellow_image, {
        'left': pygame.K_a, 'right': pygame.K_d,
        'up': pygame.K_w, 'down': pygame.K_s,
        'x_min': 0, 'x_max': seperator.left}, 'right')
    red = Spaceship(700, 300, red_image, {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
        'up': pygame.K_UP, 'down': pygame.K_DOWN,
        'x_min': seperator.right, 'x_max': Width}, 'left')
# inititalizing both spaceship and calling function
    healthpowerup = healthPowerUp()
    rapid_powerup = RapidFirePowerUp()
    obstacles = [Obstacle(random.randint(100, 750), random.randint(50, 400)) for _ in range(3)]
    clock = pygame.time.Clock()
    running = True
# Sets up game objects and loop.


    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
# Ensures frame rate, captures keys, gets current time.

        for event in pygame.event.get():
# loops through all the events in the event queue
            if event.type == pygame.QUIT:
                running = False
# If the player clicks the window’s close button, this sets running = False to exit the main loop and quit the game.
            if event.type == pygame.KEYDOWN:
# Checks if a key has been pressed (key down event).
                if event.key == pygame.K_LCTRL:
                    yellow.shoot()
                if event.key == pygame.K_RCTRL:
                    red.shoot()
            if event.type == yellow_hit:
                yellow.health -= 1
                hit_sound.play()

            if event.type == red_hit:
                red.health -= 1
                hit_sound.play()


        if yellow.rapid_fire and current_time < yellow.rapid_fire_end_time:
            if current_time % 150 < 20:
                yellow.shoot()
# once every 150 ms . <20 give a time where shooting is allowed
            
        else:
            yellow.rapid_fire = False

        if red.rapid_fire and current_time < red.rapid_fire_end_time:
            if current_time % 150 < 20:
                red.shoot()
        else:
            red.rapid_fire = False

        yellow.move(keys)
        red.move(keys)
        handle_bullets(yellow, red, obstacles)
        healthpowerup.apply(yellow)
        healthpowerup.apply(red)
        rapid_powerup.apply(yellow)
        rapid_powerup.apply(red)

        if red.health <= 0:
            draw_winner("Yellow Wins!")
            running = False
        elif yellow.health <= 0:
            draw_winner("Red Wins!")
            running = False

        draw_window(yellow, red, healthpowerup, rapid_powerup, obstacles)

    pygame.quit()

if __name__ == "__main__":
    main()
