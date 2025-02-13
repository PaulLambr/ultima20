import pygame
from tiletypes.tiletypes import TILE_TYPES  # Import tile types

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move 'A' on a 15x15 Tile Map")
clock = pygame.time.Clock()  # Controls frame rate

# Sample 15x15 map using tile type keys
world_map = [
    ["grassland"] * GRID_SIZE for _ in range(GRID_SIZE)
]

# Add some rocks manually for testing (impassable areas)
world_map[3][3] = "rock"
world_map[5][6] = "rock"
world_map[7][7] = "rock"
world_map[10][10] = "rock"

# Player starting position (grid-based)
player_x, player_y = 0, 0

# Game loop
running = True
redraw_needed = True  # Only redraw when necessary

while running:
    clock.tick(60)  # Limit FPS to 60 (prevents CPU overuse)

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

    # Only redraw if movement occurred
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

        pygame.display.update()
        redraw_needed = False  # Prevent unnecessary redraws

pygame.quit()