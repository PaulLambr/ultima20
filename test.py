import pygame
import os

# ✅ Mac Fix: Force SDL2 to use software rendering
os.environ["SDL_VIDEO_METAL"] = "1"
os.environ["SDL_RENDER_DRIVER"] = "software"

# ✅ Initialize pygame
pygame.init()
pygame.key.set_repeat(150, 50)  # Prevents input lag on Mac

# ✅ Constants
TILE_SIZE = 50
GRID_SIZE = 15
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ✅ Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Optimized Pygame on macOS")
clock = pygame.time.Clock()

# ✅ Tile types
class Tile:
    def __init__(self, color, passable):
        self.color = color
        self.passable = passable

TILE_TYPES = {
    "grassland": Tile((34, 139, 34), True),
    "rock": Tile((128, 128, 128), False),
}

# ✅ Create an off-screen surface for performance boost
buffer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# ✅ Sample 15x15 map
world_map = [["grassland"] * GRID_SIZE for _ in range(GRID_SIZE)]
world_map[3][3] = "rock"
world_map[5][6] = "rock"
world_map[7][7] = "rock"
world_map[10][10] = "rock"

# ✅ Player starting position
player_x, player_y = 0, 0

# ✅ Draw the entire map **once** on the buffer to avoid redrawing every frame
def render_map():
    buffer.fill(BLACK)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = TILE_TYPES[world_map[row][col]]
            pygame.draw.rect(buffer, tile.color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

render_map()  # Draw the static background

# ✅ Game loop
running = True

while running:
    clock.tick(60)  # ✅ Maintain 60 FPS without CPU overload

    # ✅ Process events **only if they are needed**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y

            if event.key == pygame.K_LEFT and player_x > 0:
                new_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                new_x += 1
            elif event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            elif event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                new_y += 1

            if TILE_TYPES[world_map[new_y][new_x]].passable:
                player_x, player_y = new_x, new_y

    # ✅ Render only the player on top of the static buffer
    screen.blit(buffer, (0, 0))  # Reuse pre-rendered background
    font = pygame.font.Font(None, 50)
    text = font.render("A", True, WHITE)
    screen.blit(text, (player_x * TILE_SIZE + 15, player_y * TILE_SIZE + 5))

    pygame.display.flip()  # ✅ Fastest possible update method

pygame.quit()
