import pygame
import random

pygame.init()
pygame.font.init()

# ✅ Set up the display *before* loading images
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map
WORLD_SIZE = 100
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE + 400, TILE_SIZE * GRID_SIZE  # UI width = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPAWN_INTERVAL = 200  # Frames per spawn attempt

# ✅ Set up the display first!
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Realm of Britannia")
clock = pygame.time.Clock()  # Controls frame rate

from tiletypes.tiletypes import TILE_TYPES, is_tile_passable  # Import tile types
from enemies.enemies import spawnenemy, moveenemy, bosstrspawn
from battle import combat  # Import combat system
from ui import UI
from utils import returntomap, openchest, fled, additem
from gamestate import player, ui_panel, PlayerStats
from enemies.enemies import ENEMIES_LIST
from britannia import britannia_castle
from worldmap import getworldmap, playercamera

for tile in TILE_TYPES.values():
    tile.load_sprite()
    tile.load_background()

world_map = getworldmap()
camera_x, camera_y = 0,0

# Player starting position
player_x, player_y = 7,15
player_level = 1
restore_x, restore_y = player_x, player_y  # Ensure it's initialized
player_sprite = pygame.image.load("sprites/avatar.png").convert_alpha()  # Load avatar
player_sprite = pygame.transform.scale(
    player_sprite, (TILE_SIZE, TILE_SIZE)
)  # Scale to fit tiles


# Enemy tracking variables (initialized as None)
enemy_present = False
enemy_x, enemy_y, enemy_sprite = None, None, None
enemy_type = None  # Ensure it's always defined
winning = False
bosstrspawnf = False
chest_replacement_tiles = {}



# Game loop
running = True
redraw_needed = True
frame_counter = 0
open_mode = False  # Ensure 'open_mode' is defined
pending_open = None  # Ensure 'pending_open' is also defined
previouscolor = None

while running:
    clock.tick(60)  # Limit FPS to 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect single key press event (not continuous holding)
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_action = ui_panel.handle_click(event.pos)  # Get action

            if selected_action == "Use" and player.potions:
                redraw_needed = True
                ui_panel.usepotion(player)  # ✅ Correct
                
            elif selected_action and "Equip_" in selected_action:
                redraw_needed = True
                ui_panel.equip_item(event.pos, player)  # ✅ Equip item logic triggered
                ui_panel.update_stats(player)  # ✅ Refresh UI

            elif selected_action == "Drop":
                print("Drop button clicked!")

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

            if event.key == pygame.K_o:  # Enter open chest mode
                open_mode = True
                pending_open = None
                print("🔓 Open mode activated. Press a direction key.")
                continue

            if (
                open_mode
            ):  # If "O" was pressed, register the next key as chest direction
                pending_open = event.key
                open_mode = False

                # Determine chest location
                open_x, open_y = player_x, player_y
                if pending_open == pygame.K_LEFT:
                    open_x -= 1
                elif pending_open == pygame.K_RIGHT:
                    open_x += 1
                elif pending_open == pygame.K_UP:
                    open_y -= 1
                elif pending_open == pygame.K_DOWN:
                    open_y += 1

                # Ensure within bounds and process chest
                if 0 <= open_x < WORLD_SIZE and 0 <= open_y < WORLD_SIZE:
                   
                    openchest(
                        player_x,
                        player_y,
                        pending_open,
                        world_map,
                        WORLD_SIZE,
                        ENEMIES_LIST,
                        enemy_type,
                        ui_panel,
                        chest_replacement_tiles
                    )
            
                    
            new_tile_type = world_map[new_y][new_x]
            # Process player input and attempt to move
            if TILE_TYPES[new_tile_type].passable and is_tile_passable(new_tile_type):
                player_x, player_y = new_x, new_y
                print(f"Player at{player_x, player_y} in world_map")
                camera_x, camera_y, grid_size = playercamera(player_x, player_y, world_map)
                redraw_needed = True

                if new_tile_type == "britannia":
                    britannia_castle()
            else:
                print("Movement blocked on hills this turn.")

            # Move the enemy towards the player regardless of player's move success
            if enemy_present and enemy_x is not None and enemy_y is not None:
                enemy_x, enemy_y = moveenemy(
            enemy_x, enemy_y, player_x, player_y, world_map, TILE_TYPES, redraw_needed
            )
            redraw_needed = True

            if enemy_x == player_x and enemy_y == player_y:
                restore_x, restore_y = player_x, player_y  # Save position
                tile_type = world_map[player_y][player_x]
                player_level = player.level
                print(f"\nBefore combat, tile_type is {tile_type}")

                winning = combat(player_level, tile_type, enemy_type, winning, bosstrspawnf)

                returned_position = returntomap(player_x, player_y, restore_x, restore_y)
                if returned_position:
                    player_x, player_y = returned_position
                else:
                    player_x, player_y = restore_x, restore_y
                
                if winning and enemy_type == "trollboss":
                # Replace the boss spawn tile with a normal tile (e.g., "grassland")
                    for row in range(len(world_map)):
                        for col in range(len(world_map[0])):
                            if world_map[row][col] == "trollbossspawn":
                                world_map[row][col] = "hills"
                                break


                if winning:
                    chest_replacement_tiles = {}
                    if world_map[restore_y][restore_x] != "britannia":
                        print(f"📦 Placing chest at ({restore_x}, {restore_y})")
                        chest_replacement_tiles[(restore_x, restore_y)] = world_map[restore_y][restore_x]
                        world_map[restore_y][restore_x] = "chest"
                        TILE_TYPES["chest"].background = TILE_TYPES[
                            tile_type
                        ].background
                        TILE_TYPES["chest"].background2 = (
                            None  # Reset previous background
                        )
                        TILE_TYPES[
                            "chest"
                        ].load_background()  # Reload with new background

                
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("The Realm of Britannia")
                ui_panel = UI(player)
                frame_counter = 0
                # Reset enemy variables to fully remove the enemy from the world map
                enemy_present = False
                enemy_x, enemy_y, enemy_sprite, enemy_type = None, None, None, None
                redraw_needed = True

    # logic for spawning the troll boss       
    if (player_x, player_y) == (3,94) and not bosstrspawnf:
        print("🔥 Player triggered the trap! Boss should spawn.")
        bosstrspawnf = True
        
    if bosstrspawnf:
        boss_data = bosstrspawn(world_map, TILE_TYPES)  # Find the boss tile
        if boss_data:
            enemy_x, enemy_y, enemy_sprite, enemy_type = boss_data  # Place the boss
            enemy_present = True  # Ensure the boss is displayed


        
    else:
    
        # Get current camera view offsets and grid_size
        camera_x, camera_y, grid_size = playercamera(player_x, player_y, world_map)

        # Spawn enemy every SPAWN_INTERVAL frames
        frame_counter += 1
    if frame_counter >= SPAWN_INTERVAL and not enemy_present:
        spawn_result = spawnenemy(world_map, grid_size, camera_x, camera_y)  # Now using dynamic camera view
        if spawn_result:
            enemy_x, enemy_y, enemy_sprite, enemy_type = spawn_result
            enemy_present = True
        frame_counter = 0
    elif frame_counter >= 750 and enemy_present:
        enemy_present = False
        frame_counter = 0
        redraw_needed = True
        spawn_result = spawnenemy(world_map, grid_size, camera_x, camera_y)
        if spawn_result:
            enemy_x, enemy_y, enemy_sprite, enemy_type = spawn_result
            enemy_present = True
        frame_counter = 0


    
    # Only redraw if necessary
    if redraw_needed:
        screen.fill(BLACK)

        # Draw the map using tile colors
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if world_map[row][col] == "chest":
                    print(f"Chest found at ({col}, {row}) in world_map")
                tile_type = world_map[row + camera_y][col + camera_x]
                # print(f"\ntile type is {tile_type} when drawing map")
                tile = TILE_TYPES[tile_type]
                if tile.background2:
                    background_scaled = pygame.transform.scale(
                        tile.background2, (TILE_SIZE, TILE_SIZE)
                    )  # Ensure correct size
                    screen.blit(background_scaled, (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    pygame.draw.rect(
                        screen,
                        tile.color,
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )

                # ✅ Then layer the sprite on top if it exists
                if tile.sprite:
                    tile.background = TILE_TYPES[tile_type].background

                    if tile.background2:
                        background_scaled = pygame.transform.scale(
                            tile.background2, (TILE_SIZE, TILE_SIZE)
                        )  # Ensure correct size
                        screen.blit(
                            background_scaled, (col * TILE_SIZE, row * TILE_SIZE)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            tile.color,
                            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        )
                    sprite_scaled = pygame.transform.scale(
                        tile.sprite, (TILE_SIZE, TILE_SIZE)
                    )  # Ensure correct size
                    screen.blit(sprite_scaled, (col * TILE_SIZE, row * TILE_SIZE))

        # Draw player sprite at the player's position
        screen.blit(player_sprite,((player_x - camera_x) * TILE_SIZE, (player_y - camera_y) * TILE_SIZE))

        if enemy_present and enemy_sprite:
            enemy_scaled = pygame.transform.scale(enemy_sprite, (TILE_SIZE, TILE_SIZE))
            screen.blit(enemy_scaled,((enemy_x - camera_x) * TILE_SIZE, (enemy_y - camera_y) * TILE_SIZE))
                

        # Draw UI Panel (Stats)
        ui_panel.draw(screen)

        pygame.display.update()
        redraw_needed = False  # Prevent unnecessary redraws

pygame.quit()
