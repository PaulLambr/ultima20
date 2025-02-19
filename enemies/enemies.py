import random
import pygame
import os


# Enemy class
class Enemies:
    def __init__(self, sprite_path, hitpoints, strength, loot, spawn, lettersprite, xp):
        self.sprite_path = sprite_path
        self.sprite = None
        self.hitpoints = hitpoints
        self.strength = strength
        self.loot = loot
        self.spawn = spawn
        self.lettersprite = lettersprite
        self.xp = xp

    def load_sprite(self):
        """Loads the sprite only after Pygame display is initialized"""
        if self.sprite_path and not self.sprite:
            if os.path.exists(self.sprite_path):
                try:
                    self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
                    print(f"Loaded sprite: {self.sprite_path}")
                except pygame.error as e:
                    print(f"Error loading {self.sprite_path}: {e}")
            else:
                print(f"Sprite file not found: {self.sprite_path}")


# Dictionary to store enemy types
ENEMIES_LIST = {
    "orc": Enemies("sprites/orc.png", 12, 5, 10, "grassland", "O", 20),
    "troll": Enemies(None, 20, 10, 15, "hills", "T", 30),
}


# Function to spawn an enemy
def spawnenemy(world_map, GRID_SIZE):
    spawnable_tiles = []  # List to store potential spawn locations

    # Find all grassland and hill tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_type = world_map[row][col]
            if tile_type in ["grassland", "hills"]:  # Check valid enemy spawn tiles
                spawnable_tiles.append((row, col, tile_type))

    if not spawnable_tiles:
        return None  # No valid spawn locations

    # Choose a random spawn location
    enemy_y, enemy_x, tile_type = random.choice(spawnable_tiles)

    # Determine which enemy to spawn
    if tile_type == "grassland":
        enemy_type = "orc"
    elif tile_type == "hills":
        enemy_type = "troll"

    enemy = ENEMIES_LIST[enemy_type]  # Get enemy object

    # ✅ Load and return the enemy sprite instead of a letter
    enemy.load_sprite()  # Ensure sprite is loaded before use
    return enemy_x, enemy_y, enemy.sprite, enemy_type


# Function to move enemy toward player
def moveenemy(enemy_x, enemy_y, player_x, player_y, world_map, TILE_TYPES):
    """
    Moves the enemy one step toward the player, but only in one direction (X or Y).
    Returns the new (enemy_x, enemy_y).
    """

    # Calculate possible movement directions
    move_x = 0
    move_y = 0

    if enemy_x < player_x:  # Move right
        move_x = 1
    elif enemy_x > player_x:  # Move left
        move_x = -1

    if enemy_y < player_y:  # Move down
        move_y = 1
    elif enemy_y > player_y:  # Move up
        move_y = -1

    # Randomly decide whether to move in X or Y direction (not both)
    if random.choice([True, False]):  # 50% chance to prioritize horizontal movement
        new_x = enemy_x + move_x
        new_y = enemy_y  # Keep Y the same
    else:  # 50% chance to prioritize vertical movement
        new_x = enemy_x
        new_y = enemy_y + move_y  # Keep X the same

    # Check if new position is passable
    if TILE_TYPES[world_map[new_y][new_x]].passable:
        return new_x, new_y  # Move enemy to new position

    return enemy_x, enemy_y  # Stay in place if blocked
