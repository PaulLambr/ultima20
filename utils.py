from enemies.enemies import ENEMIES_LIST
from gamestate import player
from ui import UI
import pygame
import random
from tiletypes.tiletypes import TILE_TYPES  # Import tile types


# utils.py
def returntomap(player_x, player_y, restore_x, restore_y):
    """
    Restores the player's position after combat.
    """
    return restore_x, restore_y  # Return new position

import pygame
import random

import pygame
import random

import pygame
import random

def openchest(player_x, player_y, pending_open, world_map, GRID_SIZE, ENEMIES_LIST, enemy_type, ui_panel, current_tile):
    """Handles opening chests adjacent to the player and granting rewards."""
    global redraw_needed  

    open_x, open_y = player_x, player_y  

    # Determine chest location based on direction key
    if pending_open == pygame.K_LEFT:
        open_x -= 1
    elif pending_open == pygame.K_RIGHT:
        open_x += 1
    elif pending_open == pygame.K_UP:
        open_y -= 1
    elif pending_open == pygame.K_DOWN:
        open_y += 1

    # Ensure within bounds
    if 0 <= open_x < GRID_SIZE and 0 <= open_y < GRID_SIZE:
        if world_map[open_y][open_x] == "chest":
            print(f"✅ Chest detected at ({open_x}, {open_y})")

            # ✅ Store the current tile type before opening the chest
            original_tile = current_tile  # Passed from game.py

            # Determine loot amount
            if enemy_type and enemy_type in ENEMIES_LIST:
                loot_factor = ENEMIES_LIST[enemy_type].loot  # Use .loot directly
            else:
                loot_factor = 5  # Default loot if no enemy
            loot_amount = random.randint(1, 2) * loot_factor  
            player.gold += loot_amount

            # ✅ Replace the chest with the original terrain
            world_map[open_y][open_x] = original_tile
            print(f"✅ Chest removed. Tile at ({open_x}, {open_y}) is now '{original_tile}'.")

            # ✅ Force redraw
            redraw_needed = True  

            # ✅ Update UI panel
            ui_panel.update_stats(player)

            print(f"🎉 Chest opened! You found {loot_amount} gold.")
        else:
            print("❌ No chest in that direction.")
