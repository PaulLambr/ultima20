# tiletypes.py - Defines the tile types for the game

class Tile:
    def __init__(self, color, passable):
        self.color = color  # RGB color for rendering
        self.passable = passable  # Determines if the player can move onto this tile

# Dictionary to store tile types
TILE_TYPES = {
    "grassland": Tile((34, 139, 34), True),  # Forest Green, passable
    "rock": Tile((128, 128, 128), False)  # Grey, impassable
}
