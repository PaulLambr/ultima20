import pygame
import random
from enemies.enemies import ENEMIES_LIST, moveenemy  # Use existing enemy logic
from tiletypes.tiletypes import TILE_TYPES

# Constants for Battle Screen
BATTLE_GRID_SIZE = 12  # Smaller battle map
TILE_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def combat(player_level):
    """
    Initializes a battle screen where the number of enemies depends on the player's level.
    """
    # Initialize Pygame battle screen
    pygame.init()
    WIDTH, HEIGHT = TILE_SIZE * BATTLE_GRID_SIZE, TILE_SIZE * BATTLE_GRID_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Mode")

    # Generate a blank battle grid (All 'grassland' tiles)
    battle_map = [["grassland"] * BATTLE_GRID_SIZE for _ in range(BATTLE_GRID_SIZE)]

    # Player starts in the center
    player_x, player_y = 6,10

    # Determine the number of enemies based on player level
    num_enemies = min(player_level, 5)  # Limit max enemies to 5 for balance
    enemy_list = []

    # Spawn enemies in random valid positions
    for _ in range(num_enemies):
        while True:
            enemy_x = random.randint(0, BATTLE_GRID_SIZE - 1)
            enemy_y = random.randint(0, BATTLE_GRID_SIZE - 1)

            # Ensure enemy doesn't spawn on the player or another enemy
            if (enemy_x, enemy_y) != (player_x, player_y) and (enemy_x, enemy_y) not in enemy_list:
                enemy_type = random.choice(list(ENEMIES_LIST.keys()))  # Random enemy type
                enemy_sprite = ENEMIES_LIST[enemy_type].lettersprite
                enemy_list.append((enemy_x, enemy_y, enemy_sprite))
                break

    # Battle loop
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)  # Limit FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement
            if event.type == pygame.KEYDOWN:
                new_x, new_y = player_x, player_y
                if event.key == pygame.K_LEFT and player_x > 0:
                    new_x -= 1
                if event.key == pygame.K_RIGHT and player_x < BATTLE_GRID_SIZE - 1:
                    new_x += 1
                if event.key == pygame.K_UP and player_y > 0:
                    new_y -= 1
                if event.key == pygame.K_DOWN and player_y < BATTLE_GRID_SIZE - 1:
                    new_y += 1

                # Move player and update enemy positions
                player_x, player_y = new_x, new_y
                new_enemy_list = []
                for ex, ey, es in enemy_list:
                    new_ex, new_ey = moveenemy(ex, ey, player_x, player_y, battle_map, TILE_TYPES)
                    new_enemy_list.append((new_ex, new_ey, es))
                enemy_list = new_enemy_list

        # Draw battle screen
        screen.fill(BLACK)

        # Draw the map using tile colors
        for row in range(BATTLE_GRID_SIZE):
            for col in range(BATTLE_GRID_SIZE):
                tile_type = battle_map[row][col]
                tile = TILE_TYPES[tile_type]
                pygame.draw.rect(screen, tile.color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw player
        font = pygame.font.Font(None, 50)
        player_text = font.render("A", True, WHITE)
        screen.blit(player_text, (player_x * TILE_SIZE + 15, player_y * TILE_SIZE + 5))

        # Draw enemies
        for ex, ey, es in enemy_list:
            enemy_text = font.render(es, True, WHITE)
            screen.blit(enemy_text, (ex * TILE_SIZE + 15, ey * TILE_SIZE + 5))

        pygame.display.update()

    pygame.quit()
