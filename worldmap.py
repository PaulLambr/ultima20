import random



def getworldmap():
    WORLD_SIZE = 100
    world_map = [["grassland"] * WORLD_SIZE for _ in range(WORLD_SIZE)]

    # Key locations
    world_map[5][5] = "britannia"
    world_map[8][4] = "trollbossspawn"

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

    return world_map


def playercamera(player_x, player_y, world_map):
    WORLD_SIZE = 100
    GRID_SIZE = 15  # Camera captures a 15x15 section

    # Calculate camera offsets so the view stays within the world bounds
    camera_x = max(0, min(player_x - GRID_SIZE // 2, WORLD_SIZE - GRID_SIZE))
    camera_y = max(0, min(player_y - GRID_SIZE // 2, WORLD_SIZE - GRID_SIZE))

    # Return the offsets along with the grid size
    return camera_x, camera_y, GRID_SIZE
