import pygame
import random
from tiletypes.tiletypes import TILE_TYPES  # Import tile types
from enemies.enemies import spawnenemy, moveenemy
from battle import combat  # Import combat system

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPAWN_INTERVAL = 60  # Frames per spawn attempt

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move 'A' on a 15x15 Tile Map")
clock = pygame.time.Clock()  # Controls frame rate

# Sample 15x15 map using tile type keys
world_map = [["grassland"] * GRID_SIZE for _ in range(GRID_SIZE)]

# Add some rocks manually for testing (impassable areas)
world_map[3][3] = "rock"
world_map[5][6] = "rock"
world_map[7][7] = "rock"
world_map[10][10] = "rock"
world_map[12][14] = "hills"
world_map[14][14] = "hills"
world_map[13][14] = "hills"
world_map[11][14] = "hills"
world_map[10][14] = "hills"

# Player starting position
player_x, player_y = 0, 0
player_level = 2
restore_x, restore_y = None

# Enemy tracking variables (initialized as None)
enemy_present = False
enemy_x, enemy_y, enemy_sprite = None, None, None

# Game loop
running = True
redraw_needed = True  # Only redraw when necessary
frame_counter = 0  # Track frames for enemy spawning

def returntomap():
    """
    Restores the player's position after combat.
    """
    global player_x, player_y
    player_x, player_y = restore_x, restore_y  # Restore previous position

while running:
    clock.tick(60)  # Limit FPS to 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect single key press event (not continuous holding)
        if event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y

            if event.key == pygame.K_LEFT and player_x > 0:
                new_x -= 1
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                new_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                new_y += 1

            # Check if new position is passable
            if TILE_TYPES[world_map[new_y][new_x]].passable:
                player_x, player_y = new_x, new_y
                redraw_needed = True

                # Move the enemy towards the player
                if enemy_present:
                    enemy_x, enemy_y = moveenemy(enemy_x, enemy_y, player_x, player_y, world_map, TILE_TYPES)

                    # If player and enemy collide, initiate combat
                    if enemy_x == player_x and enemy_y == player_y:
                        restore_x, restore_y = player_x, player_y  # Save position
                        combat(player_level)  # Start battle
                        returntomap()  # Restore position after battle
                        enemy_present = False  # Enemy defeated, remove from overworld

    # Spawn enemy every 60 frames
    frame_counter += 1
    if frame_counter >= SPAWN_INTERVAL and not enemy_present:
        spawn_result = spawnenemy(world_map, GRID_SIZE)  # Get enemy spawn data
        if spawn_result:
            enemy_x, enemy_y, enemy_sprite = spawn_result
            enemy_present = True  # Enemy is now on the map
        frame_counter = 0

    # Only redraw if necessary
    if redraw_needed:
        screen.fill(BLACK)

        # Draw the map using tile colors
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile_type = world_map[row][col]
                tile = TILE_TYPES[tile_type]
                pygame.draw.rect(screen, tile.color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw 'A' at the player's position
        font = pygame.font.Font(None, 50)
        text = font.render("A", True, WHITE)
        screen.blit(text, (player_x * TILE_SIZE + 15, player_y * TILE_SIZE + 5))

        # Draw enemy if present
        if enemy_present and enemy_sprite:
            text = font.render(enemy_sprite, True, WHITE)
            screen.blit(text, (enemy_x * TILE_SIZE + 15, enemy_y * TILE_SIZE + 5))

        pygame.display.update()
        redraw_needed = False  # Prevent unnecessary redraws

pygame.quit()
