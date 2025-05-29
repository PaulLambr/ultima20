import pygame

# Initialize
pygame.init()
GRID_SIZE = 10
TILE_SIZE = 40
WIDTH = HEIGHT = GRID_SIZE * TILE_SIZE

# Colors
COLOR_DEFAULT = (220, 230, 255)
COLOR_TOGGLED = (140, 240, 200)
COLOR_BORDER = (150, 150, 150)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Grid Example")

# Create grid state
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            grid[grid_y][grid_x] = (grid[grid_y][grid_x] + 1) % 2

    # Draw grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = COLOR_TOGGLED if grid[y][x] == 1 else COLOR_DEFAULT
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_BORDER, rect, 1)

    pygame.display.flip()

pygame.quit()


# git add .
# git commit -m "Updated some files"
# git push
# git pull origin main

# player_level = 2

# git branch
# git checkout Potions
# git pull origin Potions

# git fetch origin
# git checkout -b Potions origin/Potions

