from enemies.enemies import ENEMIES_LIST
from gamestate import player
from ui import UI, Dialog
import pygame
import random
from tiletypes.tiletypes import TILE_TYPES  # Import tile types


# utils.py
def returntomap(player_x, player_y, restore_x, restore_y):
    """
    Restores the player's position after combat.
    """
    return restore_x, restore_y  # Return new position

def fled(player_x, player_y, restore_x, restore_y):
    """
    Restores the player's position after combat.
    """
    return restore_x, restore_y  # Return new position

def openchest(
    player_x,
    player_y,
    pending_open,
    world_map,
    WORLD_SIZE,
    ENEMIES_LIST,
    enemy_type,
    ui_panel,
    chest_replacement_tiles
):
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
    if 0 <= open_x < WORLD_SIZE and 0 <= open_y < WORLD_SIZE:
        if world_map[open_y][open_x] == "chest":
            print(f"✅ Chest detected at ({open_x}, {open_y})")

            # ✅ Store the current tile type before opening the chest
            original_tile = chest_replacement_tiles.get((open_x, open_y), "grassland")

            # Determine loot amount
            if enemy_type and enemy_type in ENEMIES_LIST:
                loot_factor = ENEMIES_LIST[enemy_type].loot * player.level # Use .loot directly
            else:
                loot_factor = 5  # Default loot if no enemy
            loot_amount = round(random.uniform(1, 2) * loot_factor)
            player.gold += loot_amount

            # ✅ Replace the chest with the original terrain
            world_map[open_y][open_x] = original_tile
            print(
                f"✅ Chest removed. Tile at ({open_x}, {open_y}) is now '{original_tile}'."
            )

            # ✅ Remove the entry from the dictionary
            if (open_x, open_y) in chest_replacement_tiles:
                del chest_replacement_tiles[(open_x, open_y)]
                
            # ✅ Force redraw
            redraw_needed = True

            # ✅ Update UI panel
            ui_panel.update_stats(player)

            print(f"🎉 Chest opened! You found {loot_amount} gold.")
        else:
            print("❌ No chest in that direction.")


def talk(player_x, player_y, pending_talk, castle_map):
    talk_x, talk_y = player_x, player_y

    if pending_talk == pygame.K_LEFT:
        talk_x -= 1
    elif pending_talk == pygame.K_RIGHT:
        talk_x += 1
    elif pending_talk == pygame.K_UP:
        talk_y -= 1
    elif pending_talk == pygame.K_DOWN:
        talk_y += 1

    if 0 <= talk_x < len(castle_map) and 0 <= talk_y < len(castle_map[0]):
        if castle_map[talk_y][talk_x] == "merchant":
            print(f"✅ Merchant detected at ({talk_x}, {talk_y})")
            return True, ["Welcome, weary traveler, to my humble shoppe."]  # ✅ Enable dialog & send text
        else:
            print("❌ No merchant in that direction.")

    return False, []  # ✅ No dialog if not a merchant
