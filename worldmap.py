import random



def getworldmap():
    WORLD_SIZE = 100
    world_map = [["grassland"] * WORLD_SIZE for _ in range(WORLD_SIZE)]


    # Hills scattered across the world
    for _ in range(250):  # Random hills
        x, y = random.randint(5, 95), random.randint(5, 95)
        world_map[y][x] = "hills"

    # Mountains (rocks) scattered across the world
    for _ in range(20):  # Random mountains
        x, y = random.randint(20, 80), random.randint(20, 80)
        world_map[y][x] = "rock"

    # Borders of the world made of rocks
    for col in range(WORLD_SIZE):  # Top and bottom borders
        world_map[0][col] = "rock"
        world_map[1][col] = "hills"
        world_map[2][col] = "hills"
        world_map[3][col] = "hills"
        world_map[99][col] = "rock"

    for row in range(WORLD_SIZE):  # Left and right borders
        world_map[row][0] = "rock"
        world_map[row][99] = "rock"
        
  
    
    #Trollbarrow
    for row in range(90,98):  # Top and bottom borders
        world_map[row][2] = "rock"
    for row in range(90,99):  # Top and bottom borders
        world_map[row][1] = "hills"
    for col in range(2,10):  # Top and bottom borders
        world_map[98][col] = "hills"
    for col in range(3,9):  # Top and bottom borders
        world_map[97][col] = "rock"
    for row in range(90,99):  # Top and bottom borders
        world_map[row][10] = "rock"
    for col in range(2,10):  # Top and bottom borders
        world_map[90][col] = "rock"
    for row in range(91,98):  # Top and bottom borders
        world_map[row][9] = "hills"
    for col in range(3,9):  # Top and bottom borders
        world_map[91][col] = "hills"
    for row in range(92,97):  # Top and bottom borders
        world_map[row][3] = "hills"
    for row in range(92,96):  # Top and bottom borders
        world_map[row][4] = "rock"
    for col in range(4,8):  # Top and bottom borders
        world_map[92][col] = "rock"
    for row in range(92,97):  # Top and bottom borders
        world_map[row][8] = "rock"
    world_map[96][5] = "hills"
        
   # Key locations
    world_map[14][14] = "britannia"
    world_map[96][4] = "trollbossspawn"
    world_map[94][6] = "chestruby"
    
    return world_map


def playercamera(player_x, player_y, world_map):
    WORLD_SIZE = 100
    GRID_SIZE = 15  # Camera captures a 15x15 section

    # Calculate camera offsets so the view stays within the world bounds
    camera_x = max(0, min(player_x - GRID_SIZE // 2, WORLD_SIZE - GRID_SIZE))
    camera_y = max(0, min(player_y - GRID_SIZE // 2, WORLD_SIZE - GRID_SIZE))

    # Return the offsets along with the grid size
    return camera_x, camera_y, GRID_SIZE
