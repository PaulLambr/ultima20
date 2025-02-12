import pygame

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 50
GRID_SIZE = 10
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move 'A' on a 10x10 Tile Map")
clock = pygame.time.Clock()  # Controls frame rate

# Player starting position (grid-based)
player_x = 0
player_y = 0

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
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
                redraw_needed = True
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                player_x += 1
                redraw_needed = True
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
                redraw_needed = True
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                player_y += 1
                redraw_needed = True

    # Only redraw if movement occurred
    if redraw_needed:
        screen.fill(BLACK)

        # Draw the grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid lines

        # Draw 'A' at the player's position
        font = pygame.font.Font(None, 50)
        text = font.render("A", True, WHITE)
        screen.blit(text, (player_x * TILE_SIZE + 15, player_y * TILE_SIZE + 5))

        pygame.display.update()
        redraw_needed = False  # Prevent unnecessary redraws

pygame.quit()
