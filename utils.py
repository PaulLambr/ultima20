from enemies.enemies import ENEMIES_LIST
from gamestate import player
from ui import UI, Dialog
import pygame
import random
from tiletypes.tiletypes import TILE_TYPES  # Import tile types
import merchantwares

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

    if 0 <= open_x < WORLD_SIZE and 0 <= open_y < WORLD_SIZE:
        
        if world_map[open_y][open_x] == "chestruby":
            chest_replacement_tiles = {}
            print("\nYou are trying to open the holy chest.")
            additem("holy ruby")
            # Store the current tile type before opening the chest
            original_tile = chest_replacement_tiles.get((open_x, open_y), "grassland")
            # Replace the chest with the original terrain
            world_map[open_y][open_x] = original_tile
            print(f"✅ Chest removed. Tile at ({open_x}, {open_y}) is now '{original_tile}'.")

            # Remove the entry from the dictionary
            if (open_x, open_y) in chest_replacement_tiles:
                del chest_replacement_tiles[(open_x, open_y)]
                
            # Force redraw and update UI
            redraw_needed = True
            ui_panel.update_stats(player)
        
        elif world_map[open_y][open_x] == "chest":
            print(f"✅ Chest detected at ({open_x}, {open_y})")

            # Store the current tile type before opening the chest
            original_tile = chest_replacement_tiles.get((open_x, open_y), "grassland")

            # If enemy_type is None (e.g. after a boss fight), default it to "trollboss"
            if enemy_type is None:
                enemy_type = "trollboss"

            # Remap if still "trollbossspawn"
            if enemy_type.lower() == "trollbossspawn":
                enemy_type = "trollboss"

            if enemy_type and enemy_type in ENEMIES_LIST:
                loot_factor = ENEMIES_LIST[enemy_type].loot * player.level
            else:
                loot_factor = 5

            loot_amount = round(random.uniform(1, 2) * loot_factor)
            player.gold += loot_amount

            # Replace the chest with the original terrain
            world_map[open_y][open_x] = original_tile
            print(f"✅ Chest removed. Tile at ({open_x}, {open_y}) is now '{original_tile}'.")

            # Remove the entry from the dictionary
            if (open_x, open_y) in chest_replacement_tiles:
                del chest_replacement_tiles[(open_x, open_y)]
                
            # Force redraw and update UI
            redraw_needed = True
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
            return True, ["Welcome, weary traveler, to my humble shoppe."], True  # ✅ Enable dialog & send text
        elif castle_map[talk_y][talk_x] == "adventurer":
            if player.item1 or player.item2 or player.item3 or player.item4 or player.item5 == "holy ruby":
                print(f"✅ Adventurer detected at ({talk_x}, {talk_y}) and you have the ruby")
                player.gold += 500
                drop("holy ruby")
                return(True), ["Say I guess you're not as big of a sissy as I thought.",
                           "Here's a little honorarium for your trouble."], False
            else:
                return True, ["Hey you. You think you're better than me...",
                          "Well you're not. See. Now I could take you in a fight.",
                          "Say have you heard about this troll nest far to the south.",
                          "They say there's a treasure of great value there. Bring me this treasure and I will reward you handsomely."], False  # ✅ Enable dialog & send text
        else:
            print("❌ No one in that direction.")

    return False, [], False  # ✅ No dialog if not a merchant

def additem(item_name):
    # Normalize the name to lowercase
    key_name = item_name.lower()
    # Look up the item in the MERCHANT_WARES dictionary
    if key_name not in merchantwares.MERCHANT_WARES:
        print(f"⚠️ Item '{item_name}' not found in merchantwares!")
        return None
    item_data = merchantwares.MERCHANT_WARES[key_name]

    # Check inventory slots and add the item
    if not player.item1:
        player.item1 = item_data.item_name
        print(f"👜 Added {item_data.item_name} to inventory slot 1")
    elif not player.item2:
        player.item2 = item_data.item_name
        print(f"👜 Added {item_data.item_name} to inventory slot 2")
    elif not player.item3:
        player.item3 = item_data.item_name
        print(f"👜 Added {item_data.item_name} to inventory slot 3")
    elif not player.item4:
        player.item4 = item_data.item_name
        print(f"👜 Added {item_data.item_name} to inventory slot 4")
    elif not player.item5:
        player.item5 = item_data.item_name
        print(f"👜 Added {item_data.item_name} to inventory slot 5")
    else:
        print("⚠️ Inventory full! Sell or drop an item.")
        return None

    return item_data.item_name

def drop(item):
    item_lower = item.lower()
    dropped = False
    if isinstance(player.item1, str) and player.item1.lower() == item_lower:
        player.item1 = 0
        print(f"⚠️ Dropped {item} from Inventory Slot 1.")
        dropped = True
    if isinstance(player.item2, str) and player.item2.lower() == item_lower:
        player.item2 = 0
        print(f"⚠️ Dropped {item} from Inventory Slot 2.")
        dropped = True
    if isinstance(player.item3, str) and player.item3.lower() == item_lower:
        player.item3 = 0
        print(f"⚠️ Dropped {item} from Inventory Slot 3.")
        dropped = True
    if isinstance(player.item4, str) and player.item4.lower() == item_lower:
        player.item4 = 0
        print(f"⚠️ Dropped {item} from Inventory Slot 4.")
        dropped = True
    if isinstance(player.item5, str) and player.item5.lower() == item_lower:
        player.item5 = 0
        print(f"⚠️ Dropped {item} from Inventory Slot 5.")
        dropped = True
    if not dropped:
        print(f"⚠️ No instance of {item} found to drop.")
