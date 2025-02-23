import pygame
import random

pygame.init()
pygame.font.init()

# ✅ Set up the display *before* loading images
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map (camera view)
WORLD_SIZE = 100  # Expanded world map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE + 400, TILE_SIZE * GRID_SIZE  # UI width = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPAWN_INTERVAL = 200  # Frames per spawn attempt

# ✅ Set up the display first!
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Realm of Britannia")
clock = pygame.time.Clock()  # Controls frame rate

from tiletypes.tiletypes import TILE_TYPES  # Import tile types
from enemies.enemies import spawnenemy, moveenemy, bosstrspawn
from battle import combat  # Import combat system
from ui import UI
from utils import returntomap, openchest, fled
from gamestate import player, ui_panel, PlayerStats
from enemies.enemies import ENEMIES_LIST
from britannia import britannia_castle

# Load all tile sprites
for tile in TILE_TYPES.values():
    tile.load_sprite()
    tile.load_background()


# ✅ Generate the full 100x100 world map
def getworldmap():
    world_map = [["grassland"] * WORLD_SIZE for _ in range(WORLD_SIZE)]


    # Hills scattered across the world
    for _ in range(250):  # Random hills
        x, y = random.randint(5, 95), random.randint(5, 95)
        world_map[y][x] = "hills"

    # Mountains (rocks) scattered across the world
    for _ in range(100):  # Random mountains
        x, y = random.randint(20, 80), random.randint(20, 80)
        world_map[y][x] = "rock"

    # Borders of the world made of rocks
    for col in range(WORLD_SIZE):  # Top and bottom borders
        world_map[0][col] = "rock"
        world_map[99][col] = "rock"

    for row in range(WORLD_SIZE):  # Left and right borders
        world_map[row][0] = "rock"
        world_map[row][99] = "rock"
        
    # Key locations
    world_map[7][25] = "britannia"
    world_map[8][4] = "trollbossspawn"

    return world_map


def playercamera(player_x, player_y, world_map):
    CAMERA_SIZE = 15  # Camera captures 15x15 section

    # Keep camera within world boundaries
    camera_x = max(0, min(player_x - CAMERA_SIZE // 2, WORLD_SIZE - CAMERA_SIZE))
    camera_y = max(0, min(player_y - CAMERA_SIZE // 2, WORLD_SIZE - CAMERA_SIZE))

    # Extract 15x15 view centered on the player
    camera_view = [
        row[camera_x:camera_x + CAMERA_SIZE] for row in world_map[camera_y:camera_y + CAMERA_SIZE]
    ]

    return camera_view, camera_x, camera_y  # Return the camera view + offset


# Load the expanded world map
world_map = getworldmap()

# Player starting position
player_x, player_y = 50, 50  # Start in the center of the world
player_level = 1
restore_x, restore_y = player_x, player_y  # Ensure it's initialized
player_sprite = pygame.image.load("sprites/avatar.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (TILE_SIZE, TILE_SIZE))

# Enemy tracking variables
enemy_present = False
enemy_x, enemy_y, enemy_sprite = None, None, None
enemy_type = None
winning = False
bosstrspawnf = False

# Game loop
running = True
redraw_needed = True
frame_counter = 0
open_mode = False
pending_open = None

while running:
    clock.tick(60)  # Limit FPS to 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_action = ui_panel.handle_click(event.pos)

            if selected_action == "Use" and player.potions:
                redraw_needed = True
                ui_panel.usepotion(player)

            elif selected_action and "Equip_" in selected_action:
                redraw_needed = True
                ui_panel.equip_item(event.pos, player)
                ui_panel.update_stats(player)

        if event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y

            if event.key == pygame.K_LEFT and player_x > 0:
                new_x -= 1
            if event.key == pygame.K_RIGHT and player_x < WORLD_SIZE - 1:
                new_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_DOWN and player_y < WORLD_SIZE - 1:
                new_y += 1

            if TILE_TYPES[world_map[new_y][new_x]].passable:
                player_x, player_y = new_x, new_y
                redraw_needed = True

                if world_map[player_y][player_x] == "britannia":
                    britannia_castle()

                if enemy_present:
                    enemy_x, enemy_y = moveenemy(
                        enemy_x, enemy_y, player_x, player_y, world_map, TILE_TYPES
                    )

                    if enemy_x == player_x and enemy_y == player_y:
                        restore_x, restore_y = player_x, player_y
                        tile_type = world_map[player_y][player_x]
                        player_level = player.level
                        winning = combat(player_level, tile_type, enemy_type, winning, bosstrspawnf)

                        returned_position = returntomap(player_x, player_y, restore_x, restore_y)
                        player_x, player_y = returned_position if returned_position else (restore_x, restore_y)

                        if winning:
                            if world_map[restore_y][restore_x] != "britannia":
                                world_map[restore_y][restore_x] = "chest"

                        redraw_needed = True
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        ui_panel = UI(player)
                        enemy_present = False

    if player.level >= 4 and not bosstrspawnf:
        bosstrspawnf = True

    if bosstrspawnf:
        boss_data = bosstrspawn(world_map, TILE_TYPES)
        if boss_data:
            enemy_x, enemy_y, enemy_sprite, enemy_type = boss_data
            enemy_present = True

    else:
        frame_counter += 1
        if frame_counter >= SPAWN_INTERVAL and not enemy_present:
            spawn_result = spawnenemy(world_map, WORLD_SIZE)
            if spawn_result:
                enemy_x, enemy_y, enemy_sprite, enemy_type = spawn_result
                enemy_present = True
            frame_counter = 0

    if redraw_needed:
        screen.fill(BLACK)
        camera_view, camera_x, camera_y = playercamera(player_x, player_y, world_map)

        for row in range(15):
            for col in range(15):
                tile_type = camera_view[row][col]
                tile = TILE_TYPES[tile_type]
                if tile.background2:
                    screen.blit(pygame.transform.scale(tile.background2, (TILE_SIZE, TILE_SIZE)), (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    pygame.draw.rect(screen, tile.color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        screen.blit(player_sprite, (7 * TILE_SIZE, 7 * TILE_SIZE))
        print(f"\nPlayer at {player_x, player_y}")
        if enemy_present and enemy_sprite:
            screen.blit(pygame.transform.scale(enemy_sprite, (TILE_SIZE, TILE_SIZE)), (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE))

        ui_panel.draw(screen)
        pygame.display.update()
        redraw_needed = False

pygame.quit()
