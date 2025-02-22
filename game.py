import pygame
import random

pygame.init()
pygame.font.init()

# ✅ Set up the display *before* loading images
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE + 400, TILE_SIZE * GRID_SIZE  # UI width = 300
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

for tile in TILE_TYPES.values():
    tile.load_sprite()
    tile.load_background()

# Sample 15x15 map using tile type keys
world_map = [["grassland"] * GRID_SIZE for _ in range(GRID_SIZE)]

# Add some rocks manually for testing (impassable areas)

world_map[7][10] = "britannia"
world_map[8][4] = "trollbossspawn"


# Two rows of hills along the other 3 sides
for col in range(15):  # Top and bottom borders
    world_map[1][col] = "hills"
    world_map[14][col] = "hills"
    world_map[2][col] = "hills"
    world_map[13][col] = "hills"

for row in range(15):  # Left and right borders
    
    world_map[row][14] = "hills"
    
    world_map[row][13] = "hills"
    
# Wall of rocks along row 1
for col in range(15):
    world_map[0][col] = "rock"

# Player starting position
player_x, player_y = 2,3
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
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                new_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
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
                if 0 <= open_x < GRID_SIZE and 0 <= open_y < GRID_SIZE:
                   
                    openchest(
                        player_x,
                        player_y,
                        pending_open,
                        world_map,
                        GRID_SIZE,
                        ENEMIES_LIST,
                        enemy_type,
                        ui_panel,
                        chest_replacement_tiles
                    )

            # Check if new position is passable
            if TILE_TYPES[world_map[new_y][new_x]].passable:
                player_x, player_y = new_x, new_y
                redraw_needed = True

                if world_map[player_y][player_x] == world_map[7][10]:
                    britannia_castle()

                # Move the enemy towards the player
                if enemy_present and enemy_x is not None and enemy_y is not None:
                    enemy_x, enemy_y = moveenemy(
                        enemy_x, enemy_y, player_x, player_y, world_map, TILE_TYPES
                    )

                    # game.py
                    if enemy_x == player_x and enemy_y == player_y:
                        restore_x, restore_y = player_x, player_y  # Save position
                        tile_type = world_map[player_y][player_x]
                        player_level = player.level
                        print(f"\n before combat is called tile_type is {tile_type}")
                        
                        
                        winning = combat(player_level, tile_type, enemy_type, winning, bosstrspawnf)  

                        # ✅ Restore position after combat
                        returned_position = returntomap(player_x, player_y, restore_x, restore_y)
                        if returned_position:
                            player_x, player_y = returned_position
                        else:
                            player_x, player_y = restore_x, restore_y

                            # ✅ If the player won, place the chest
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
                            
                        # Reinitialize UI and screen
                        redraw_needed = True
                        screen = pygame.display.set_mode(
                            (WIDTH, HEIGHT)
                        )  # Reset game window
                        pygame.display.set_caption("The Realm of Britannia")
                        ui_panel = UI(player)  # Reset UI panel
                        
                        frame_counter = 0
                        
                        enemy_present = False  # Enemy defeated, remove from overworld

    if player.level >= 4 and not bosstrspawnf:
        print("🔥 Player reached level 4! Boss should spawn.")
        bosstrspawnf = True
        
    if bosstrspawnf:
        boss_data = bosstrspawn(world_map, TILE_TYPES)  # Find the boss tile
        if boss_data:
            enemy_x, enemy_y, enemy_sprite, enemy_type = boss_data  # Place the boss
            enemy_present = True  # Ensure the boss is displayed


        
    else:
    
        # Spawn enemy every 60 frames
        frame_counter += 1
        if frame_counter >= SPAWN_INTERVAL and not enemy_present:
            spawn_result = spawnenemy(world_map, GRID_SIZE)  # Get enemy spawn data
            if spawn_result:
                enemy_x, enemy_y, enemy_sprite, enemy_type = spawn_result
                enemy_present = True  # Enemy is now on the map
            frame_counter = 0

    
    # Only redraw if necessary
    if redraw_needed:
        screen.fill(BLACK)

        # Draw the map using tile colors
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if world_map[row][col] == "chest":
                    print(f"Chest found at ({col}, {row}) in world_map")
                tile_type = world_map[row][col]
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
        screen.blit(player_sprite, (player_x * TILE_SIZE, player_y * TILE_SIZE))

        # ✅ Draw the enemy if it's present
        if enemy_present and enemy_sprite:
            enemy_scaled = pygame.transform.scale(enemy_sprite, (TILE_SIZE, TILE_SIZE))  # Scale to fit tiles
            screen.blit(enemy_scaled, (enemy_x * TILE_SIZE, enemy_y * TILE_SIZE))  # Render at the boss spawn

                

        # Draw UI Panel (Stats)
        ui_panel.draw(screen)

        pygame.display.update()
        redraw_needed = False  # Prevent unnecessary redraws

pygame.quit()
