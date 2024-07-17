import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the size of each segment (same as player size)
SEGMENT_SIZE = 50

# Define a player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.head = pygame.Surface((SEGMENT_SIZE, SEGMENT_SIZE))
        self.head.fill((255, 255, 255))
        self.head_rect = self.head.get_rect()
        self.head_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Start at the center of the screen
        self.direction = None  # Start staying still
        self.body_segments = [self.head_rect.copy()]  # Start with the head segment

    @property
    def rect(self):
        return self.head_rect

    # Move the sprite based on the current direction
    def update(self):
        if self.direction:
            # Insert the current position of the head at the beginning of the body_segments list
            self.body_segments.insert(0, self.head_rect.copy())
            # Remove the last segment if the body has grown
            if len(self.body_segments) > len(fruit) + 1:  # +1 because the initial body contains only the head
                self.body_segments.pop()
            
            if self.direction == K_UP:
                self.head_rect.move_ip(0, -SEGMENT_SIZE)
            elif self.direction == K_DOWN:
                self.head_rect.move_ip(0, SEGMENT_SIZE)
            elif self.direction == K_LEFT:
                self.head_rect.move_ip(-SEGMENT_SIZE, 0)
            elif self.direction == K_RIGHT:
                self.head_rect.move_ip(SEGMENT_SIZE, 0)

            # Keep player on the screen
            if self.head_rect.left < 0 or self.head_rect.right > SCREEN_WIDTH or \
               self.head_rect.top < 0 or self.head_rect.bottom > SCREEN_HEIGHT:
                return False
        return True

    # Set the direction of the player
    def set_direction(self, key):
        if key == K_UP and self.direction != K_DOWN:
            self.direction = K_UP
        elif key == K_DOWN and self.direction != K_UP:
            self.direction = K_DOWN
        elif key == K_LEFT and self.direction != K_RIGHT:
            self.direction = K_LEFT
        elif key == K_RIGHT and self.direction != K_LEFT:
            self.direction = K_RIGHT

    # Add a new segment to the player
    def grow(self):
        if self.body_segments:
            self.body_segments.append(self.body_segments[-1].copy())
        else:
            self.body_segments.append(self.head_rect.copy())

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.surf = pygame.Surface((SEGMENT_SIZE, SEGMENT_SIZE))
        self.surf.fill((255, 0, 0))  # Change color of apple to red
        self.rect = self.surf.get_rect()
        self.spawn_in_safe_zone()

    def spawn_in_safe_zone(self):
        # Generate a random position for the apple and check if it overlaps with any body segments
        while True:
            self.rect.center = (
                random.randint(0, SCREEN_WIDTH // SEGMENT_SIZE - 1) * SEGMENT_SIZE + SEGMENT_SIZE // 2,
                random.randint(0, SCREEN_HEIGHT // SEGMENT_SIZE - 1) * SEGMENT_SIZE + SEGMENT_SIZE // 2,
            )
            overlaps = False
            for segment in player.body_segments:
                if self.rect.colliderect(segment):
                    overlaps = True
                    break
            if not overlaps:
                break

    @staticmethod
    def new():
        new_apple = Apple()
        fruit.add(new_apple)
        all_sprites.add(new_apple)

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold apple sprites and all sprites
fruit = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
Apple.new()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True

# Variable to allow change of movement once per tick
turn = False

# Initialize score
score = 0

# Font for displaying the score and game over text
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

def display_game_over():
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    exit_text = font.render("Press Esc to Exit", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

# Main loop
while running:

    # Reset turn limit
    turn = False

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            # Update the player's direction based on the key pressed
            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT] and turn == False:
                player.set_direction(event.key)
                turn = True
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Check if any apples have collided with the player
    collided_fruit = pygame.sprite.spritecollide(player, fruit, True)
    if collided_fruit:
        player.grow()
        Apple.new()
        score += 10  # Increase score by 10 points for each apple consumed

    # Check if the player's head has collided with any body segments
    for segment in player.body_segments[1:]:  # Ignore the head itself which is the first segment
        if player.head_rect.colliderect(segment):
            running = False

    # Update the player sprite based on the current direction
    if not player.update():
        running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all apples
    for apple in fruit:
        screen.blit(apple.surf, apple.rect)

    # Draw all body segments of the player
    for segment in player.body_segments:
        screen.blit(player.head, segment)

    # Draw the head of the player
    screen.blit(player.head, player.head_rect)

    # Render the score at the top of the screen
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 3 frames per second (determines speed of snake)
    clock.tick(3)

# Display game over screen
screen.fill((0, 0, 0))
screen.blit(score_text, (10, 10))
display_game_over()
pygame.display.flip()

# Wait for the user to press Esc to exit
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            waiting = False
        elif event.type == QUIT:
            waiting = False

# Quit Pygame
pygame.quit()
