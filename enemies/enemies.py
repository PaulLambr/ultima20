import random

# Enemy properties
enemy_present = False
enemy_x, enemy_y = None, None
enemy_sprite = None

# Enemy class
class Enemies:
    def __init__(self, hitpoints, strength, loot, spawn, lettersprite):
        self.hitpoints = hitpoints  
        self.strength = strength
        self.loot = loot
        self.spawn = spawn
        self.lettersprite = lettersprite

# Dictionary to store enemy types
ENEMIES_LIST = {
    "orc": Enemies(25, 10, 10, "grassland", "O"),  
    "troll": Enemies(35, 20, 15, "hills", "T")  
}

# Function to spawn an enemy
def spawnenemy(world_map, GRID_SIZE):
    global enemy_present, enemy_x, enemy_y, enemy_sprite

    if enemy_present:
        return None  # Don't spawn if an enemy is already on the map

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

    enemy_sprite = ENEMIES_LIST[enemy_type].lettersprite
    enemy_present = True  # Mark that an enemy exists

    return enemy_x, enemy_y, enemy_sprite  # Return enemy info
