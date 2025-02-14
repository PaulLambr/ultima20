import pygame
import random
from enemies.enemies import ENEMIES_LIST, moveenemy  
from tiletypes.tiletypes import TILE_TYPES
from game import returntomap  # Import function to return to map

# Constants for Battle Screen
BATTLE_GRID_SIZE = 12  
TILE_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Flags for attack mode
attack_mode = False
pending_attack = None  

def combat(player_level):
    global attack_mode, pending_attack
    
    pygame.init()
    WIDTH, HEIGHT = TILE_SIZE * BATTLE_GRID_SIZE, TILE_SIZE * BATTLE_GRID_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Mode")

    # Generate blank battle grid (All 'grassland' tiles)
    battle_map = [["grassland"] * BATTLE_GRID_SIZE for _ in range(BATTLE_GRID_SIZE)]

    # Player starts in the center
    player_x, player_y = 6, 10

    # Determine the number of enemies based on player level
    num_enemies = min(player_level, 5)  
    enemy_list = []

    for _ in range(num_enemies):
        while True:
            enemy_x = random.randint(0, BATTLE_GRID_SIZE - 1)
            enemy_y = random.randint(0, BATTLE_GRID_SIZE - 1)

            if (enemy_x, enemy_y) != (player_x, player_y) and (enemy_x, enemy_y) not in [(ex, ey) for ex, ey, _, _, _ in enemy_list]:
                enemy_type = random.choice(list(ENEMIES_LIST.keys()))  
                enemy_sprite = ENEMIES_LIST[enemy_type].lettersprite
                enemy_health = ENEMIES_LIST[enemy_type].hitpoints  # Store unique health per enemy
                enemy_list.append([enemy_x, enemy_y, enemy_type, enemy_sprite, enemy_health])
                break

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Enter attack mode
                    attack_mode = True  
                    pending_attack = None  
                    continue  

                if attack_mode:  # If "A" was pressed, register the next key as attack direction
                    pending_attack = event.key  
                    attack_mode = False  
                    attack(player_x, player_y, pending_attack, enemy_list)
                
                else:  # Player movement
                    new_x, new_y = player_x, player_y
                    if event.key == pygame.K_LEFT and player_x > 0:
                        new_x -= 1
                    if event.key == pygame.K_RIGHT and player_x < BATTLE_GRID_SIZE - 1:
                        new_x += 1
                    if event.key == pygame.K_UP and player_y > 0:
                        new_y -= 1
                    if event.key == pygame.K_DOWN and player_y < BATTLE_GRID_SIZE - 1:
                        new_y += 1

                    player_x, player_y = new_x, new_y  

                    # Move enemies
                    new_enemy_list = []
                    for ex, ey, et, es, hp in enemy_list:
                        new_ex, new_ey = moveenemy(ex, ey, player_x, player_y, battle_map, TILE_TYPES)
                        new_enemy_list.append([new_ex, new_ey, et, es, hp])
                    enemy_list = new_enemy_list  

        # Draw the screen
        screen.fill(BLACK)

        for row in range(BATTLE_GRID_SIZE):
            for col in range(BATTLE_GRID_SIZE):
                tile_type = battle_map[row][col]
                tile = TILE_TYPES[tile_type]
                pygame.draw.rect(screen, tile.color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        font = pygame.font.Font(None, 50)
        player_text = font.render("A", True, WHITE)
        screen.blit(player_text, (player_x * TILE_SIZE + 15, player_y * TILE_SIZE + 5))

        for ex, ey, et, es, hp in enemy_list:
            enemy_text = font.render(es, True, WHITE)
            screen.blit(enemy_text, (ex * TILE_SIZE + 15, ey * TILE_SIZE + 5))

        pygame.display.update()

        # If all enemies are dead, return to world map
        if not enemy_list:
            pygame.time.delay(500)  # Small delay before returning
            returntomap()
            break  # Exit the battle

    pygame.quit()

def attack(player_x, player_y, direction, enemy_list):
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
            damage(i, enemy_list)
            return  

def damage(enemy_index, enemy_list):
    """
    Reduces enemy hitpoints and removes the enemy if they are defeated.
    """
    enemy_list[enemy_index][4] -= 10  # Reduce enemy's health by 10

    # If enemy health is zero or below, remove it
    if enemy_list[enemy_index][4] <= 0:
        del enemy_list[enemy_index]  

    # If all enemies are defeated, return to world map
    if not enemy_list:
        pygame.time.delay(500)  # Small delay before returning
        returntomap()
