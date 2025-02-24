import pygame
import random
from enemies.enemies import ENEMIES_LIST
from tiletypes.tiletypes import TILE_TYPES
from utils import returntomap, fled
from ui import UI
from gamestate import player, ui_panel, PlayerStats
import merchantwares

# Constants for Battle Screen
BATTLE_GRID_SIZE = 15
TILE_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Flags for attack mode
attack_mode = False
pending_attack = None
player_x, player_y = 0, 0
restore_x, restore_y = player_x, player_y


def combat(player_level, tile_type, enemy_type, winning, bosstrspawnf):
    global attack_mode, pending_attack, ui_panel
    winning = False
    ...
    ui_panel = UI(player)  # ✅ Reset UI panel when entering battle
    player_sprite = pygame.image.load(
        "sprites/avatar.png"
    ).convert_alpha()  # Load avatar
    player_sprite = pygame.transform.scale(
        player_sprite, (TILE_SIZE, TILE_SIZE)
    )  # Scale to fit tiles

    pygame.init()
    WIDTH, HEIGHT = (
        TILE_SIZE * BATTLE_GRID_SIZE + ui_panel.WIDTH,
        TILE_SIZE * BATTLE_GRID_SIZE,
    )
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fight for Glory!")

    # Generate battle grid using the tile type from where battle started
    print(f"\ncombat 1 = {tile_type}")
    battle_map = [[tile_type] * BATTLE_GRID_SIZE for _ in range(BATTLE_GRID_SIZE)]

    # Player starts in the center
    player_x, player_y = 6, 10

    # Determine the number of enemies based on player level
    
    if enemy_type == "trollboss":
        num_enemies = 7
    else:

        num_enemies = min(player_level, 5)
    
    enemy_list = []

    for _ in range(num_enemies):
        while True:
            enemy_x = random.randint(0, BATTLE_GRID_SIZE - 1)
            enemy_y = random.randint(0, BATTLE_GRID_SIZE - 1)

            # Ensure enemies do not start at the player's position
            if (enemy_x, enemy_y) != (player_x, player_y) and (
                enemy_x,
                enemy_y,
            ) not in [(ex, ey) for ex, ey, _, _, _ in enemy_list]:
                enemy_sprite = ENEMIES_LIST[enemy_type]
                enemy_health = ENEMIES_LIST[enemy_type].hitpoints
                enemy_list.append(
                    [enemy_x, enemy_y, enemy_type, enemy_sprite, enemy_health]
                )
                break

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_action = ui_panel.handle_click(event.pos)  # ✅ Handle UI clicks

                if selected_action == "Use" and player.potions:
                    ui_panel.usepotion(player)  # ✅ Use potion
                    ui_panel.update_stats(player)  # ✅ Update UI panel

                elif selected_action and "Equip_" in selected_action:
                    ui_panel.equip_item(event.pos, player)  # ✅ Equip item logic triggered
                    ui_panel.update_stats(player)  # ✅ Refresh UI

                elif selected_action == "Drop":
                    print("Drop button clicked!")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Enter attack mode
                    attack_mode = True
                    pending_attack = None
                    continue

                if (
                    attack_mode
                ):  # If "A" was pressed, register the next key as attack direction
                    pending_attack = event.key
                    attack_mode = False
                    attack(player_x, player_y, pending_attack, enemy_list, bosstrspawnf)

                    # ✅ Trigger adjacency check after an attack
                    new_enemy_list = []
                    for i, (ex, ey, et, es, hp) in enumerate(enemy_list):
                        if (abs(ex - player_x) == 1 and ey == player_y) or (
                            abs(ey - player_y) == 1 and ex == player_x
                        ):
                            print(f"Enemy at ({ex}, {ey}) attacks!")
                            enemy_attack(
                                enemy_list, i, player_x, player_y
                            )  # ✅ Pass player_x and player_y
                            new_enemy_list.append(
                                [ex, ey, et, es, hp]
                            )  # Enemy stays in place
                        else:
                            # ✅ Enemy moves if not adjacent
                            new_ex, new_ey = move_enemy_battle(
                                ex,
                                ey,
                                player_x,
                                player_y,
                                battle_map,
                                TILE_TYPES,
                                enemy_list,
                            )
                            if (new_ex, new_ey) != (player_x, player_y):
                                new_enemy_list.append([new_ex, new_ey, et, es, hp])
                            else:
                                new_enemy_list.append(
                                    [ex, ey, et, es, hp]
                                )  # Stay in place if blocked

                    enemy_list = (
                        new_enemy_list  # ✅ Update enemy positions after an attack
                    )

                else:  # Player movement
                    new_x, new_y = player_x, player_y
                    if event.key == pygame.K_LEFT:
                        new_x -= 1
                    if event.key == pygame.K_RIGHT:
                        new_x += 1
                    if event.key == pygame.K_UP:
                        new_y -= 1
                    if event.key == pygame.K_DOWN:
                        new_y += 1
                        
                

                    # ✅ Prevent player from moving onto an enemy's position
                    if (new_x, new_y) not in [
                        (ex, ey) for ex, ey, _, _, _ in enemy_list
                    ]:
                        player_x, player_y = new_x, new_y  # Move player

                    # After player moves, each enemy takes its turn
                    new_enemy_list = []
                    for i, (ex, ey, et, es, hp) in enumerate(enemy_list):
                        # ✅ Check if enemy is adjacent (not diagonal)
                        if (abs(ex - player_x) == 1 and ey == player_y) or (
                            abs(ey - player_y) == 1 and ex == player_x
                        ):
                            print(f"Enemy at ({ex}, {ey}) attacks!")
                            enemy_attack(
                                enemy_list, i, player_x, player_y
                            )  # ✅ Pass player_x and player_y
                            new_enemy_list.append(
                                [ex, ey, et, es, hp]
                            )  # Enemy stays in place
                        else:
                            # ✅ Enemy moves if not adjacent
                            new_ex, new_ey = move_enemy_battle(
                                ex,
                                ey,
                                player_x,
                                player_y,
                                battle_map,
                                TILE_TYPES,
                                enemy_list,
                            )
                            if (new_ex, new_ey) != (player_x, player_y):
                                new_enemy_list.append([new_ex, new_ey, et, es, hp])
                            else:
                                new_enemy_list.append(
                                    [ex, ey, et, es, hp]
                                )  # Stay in place if blocked

                    enemy_list = new_enemy_list  # ✅ Update enemy positions

        # Draw the screen
        screen.fill(BLACK)

        #ui_panel.draw(screen)
    

        for row in range(BATTLE_GRID_SIZE):
            for col in range(BATTLE_GRID_SIZE):
                # print(f"\ncombat 2 = {tile_type}")
                tile_type = battle_map[row][col]
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

        # font = pygame.font.Font(None, 50)
        # player_text = font.render("A", True, WHITE)
        screen.blit(player_sprite, (player_x * TILE_SIZE, player_y * TILE_SIZE))

        for ex, ey, et, es, hp in enemy_list:
            enemy_obj = ENEMIES_LIST[et]  # ✅ Retrieve the Enemies object
            enemy_obj.load_sprite()  # ✅ Ensure sprite is loaded

            if enemy_obj.sprite:  # ✅ Ensure sprite is valid
                enemy_scaled = pygame.transform.scale(
                    enemy_obj.sprite, (TILE_SIZE, TILE_SIZE)
                )  # Scale to fit tiles
                screen.blit(enemy_scaled, (ex * TILE_SIZE, ey * TILE_SIZE))
            else:
                print(f"⚠️ Warning: No sprite found for enemy type '{et}'")
        ui_panel.draw(screen) 
        pygame.display.update()

        # If all enemies are dead, return to world map
        if not enemy_list:
            print("✅ All enemies defeated! Returning to world map.")
            winning = True
            pygame.time.delay(500)
            running = False  # Exit the battle loop
        
        
        elif 1 > player_x or player_x > 14 or player_y < 1 or player_y > 14:
            print("🚪 Player has escaped the battle.")
            winning = False
            pygame.time.delay(500)
            running = False
            

    return winning


def enemy_attack(enemy_list, enemy_index, player_x, player_y):
    """
    Enemy attacks the player if adjacent (not diagonal).
    """
    enemy_x, enemy_y = enemy_list[enemy_index][0], enemy_list[enemy_index][1]

    # ✅ Ensure enemy attacks if adjacent
    if (abs(enemy_x - player_x) == 1 and enemy_y == player_y) or (
        abs(enemy_y - player_y) == 1 and enemy_x == player_x
    ):
        armor_key = player.armor.lower()  # ✅ Convert to lowercase to match dictionary keys
        armor_data = merchantwares.MERCHANT_WARES.get(armor_key, None)  # ✅ Retrieve weapon object
        armorcoeff = armor_data.protection if armor_data else 1  # ✅ Default to 0 if no weapon found
        
        enemy_damage = round(
            (random.uniform(1, 2) * ENEMIES_LIST[enemy_list[enemy_index][2]].strength) * armorcoeff
        )
        player.hitpoints -= enemy_damage
        print(
            f"\nThe enemy dealt {enemy_damage:.2f} damage! Player HP: {player.hitpoints}"
        )

        # Check if player is dead
        if player.hitpoints <= 0:
            print("\nYou have been defeated! Game Over.")
            pygame.quit()
            exit()  # Exit the game


def move_enemy_battle(
    enemy_x, enemy_y, player_x, player_y, battle_map, TILE_TYPES, enemy_list
):
    """
    Moves the enemy one step toward the player in either X or Y direction (not both).
    Returns the new (enemy_x, enemy_y).
    """

    # If enemy is adjacent to the player, it does not move (attacks instead)
    if (abs(enemy_x - player_x) == 1 and enemy_y == player_y) or (
        abs(enemy_y - player_y) == 1 and enemy_x == player_x
    ):
        return enemy_x, enemy_y  # Stay in place if adjacent

    # Determine possible movement directions
    possible_moves = []
    if enemy_x < player_x:  # Move right
        possible_moves.append((enemy_x + 1, enemy_y))
    elif enemy_x > player_x:  # Move left
        possible_moves.append((enemy_x - 1, enemy_y))

    if enemy_y < player_y:  # Move down
        possible_moves.append((enemy_x, enemy_y + 1))
    elif enemy_y > player_y:  # Move up
        possible_moves.append((enemy_x, enemy_y - 1))

    random.shuffle(possible_moves)  # Shuffle movement options

    for new_x, new_y in possible_moves:
        # Check boundaries first:
        if new_x < 0 or new_x >= BATTLE_GRID_SIZE or new_y < 0 or new_y >= BATTLE_GRID_SIZE:
            continue
        if TILE_TYPES[battle_map[new_y][new_x]].passable and (new_x, new_y) not in [
            (ex, ey) for ex, ey, _, _, _ in enemy_list
        ]:
            return new_x, new_y


    return enemy_x, enemy_y  # Stay in place if blocked


def attack(player_x, player_y, direction, enemy_list, bosstrspawnf):  # ✅ Add bosstrspawnf
    """
    Processes an attack when 'A' is pressed followed by a direction key.
    """
    attack_x, attack_y = player_x, player_y

    if direction == pygame.K_LEFT:
        attack_x -= 1
    elif direction == pygame.K_RIGHT:
        attack_x += 1
    elif direction == pygame.K_UP:
        attack_y -= 1
    elif direction == pygame.K_DOWN:
        attack_y += 1

    for i, (ex, ey, et, es, hp) in enumerate(enemy_list):
        if attack_x == ex and attack_y == ey:
            bosstrspawnf = damage(i, enemy_list, bosstrspawnf)  # ✅ Pass and receive bosstrspawnf
            return bosstrspawnf  # ✅ Ensure updated value is returned

    return bosstrspawnf  # If no enemy was hit, return unchanged



def damage(enemy_index, enemy_list, bosstrspawnf):  # ✅ Add bosstrspawnf as an argument
    """
    Reduces enemy hitpoints and removes the enemy if they are defeated.
    """
    weapon_key = player.weapon.lower()
    weapon_data = merchantwares.MERCHANT_WARES.get(weapon_key, None)
    weaponcoeff = weapon_data.damage if weapon_data else 0

    enemy_damage = random.uniform(1, 2) * (player.strength + weaponcoeff)
    enemy_list[enemy_index][4] -= enemy_damage
    print(f"\n You scored {enemy_damage} points against {enemy_list[enemy_index][4]} enemy hp.")

    # If enemy health is zero or below, remove it and grant XP
    if enemy_list[enemy_index][4] <= 0:
        enemy_type = enemy_list[enemy_index][2]  # Get enemy type
        enemy_xp = ENEMIES_LIST[enemy_type].xp  # Get XP value from enemy

        player.xp += enemy_xp  # ✅ Update player's XP directly
        bosstrspawnf = player.levelup(bosstrspawnf)  # ✅ Ensure updated `bosstrspawnf` is stored

        print(f"DEBUG: bosstrspawnf after leveling up = {bosstrspawnf}")  # ✅ Debugging
        ui_panel.update_stats(player)
        del enemy_list[enemy_index]  # Remove defeated enemy
    
    return bosstrspawnf  # ✅ Return updated value
