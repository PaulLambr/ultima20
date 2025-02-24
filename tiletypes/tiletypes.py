import pygame
import os
import random


class Tile:
    def __init__(self, sprite_path, background, color, passable):
        self.passable = passable
        self.color = color
        self.sprite_path = sprite_path  # Store path but don't load immediately
        self.sprite = None  # Delay sprite loading
        self.background = background
        self.background2 = None

    def load_background(self):
        """Loads the sprite only after Pygame display is initialized"""
        if self.background and not self.background2:
            if os.path.exists(self.background):
                try:
                    self.background2 = pygame.image.load(
                        self.background
                    ).convert_alpha()
                    # print(f"Loaded sprite: {self.background}")
                except pygame.error as e:
                    print(f"Error loading {self.background}: {e}")
            else:
                print(f"Sprite file not found: {self.background}")

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

    def getbg(self, current_tile2):
        if current_tile2 == "hills":
            self.background = "sprites/hills.png"
        elif current_tile2 == "grassland":
            self.background = "sprites/grassland.png"

        self.background2 = None  # Reset the loaded background
        self.load_background()  # Force the update


# ✅ Dictionary to store tile types, but sprites are not loaded yet
TILE_TYPES = {
    "grassland": Tile(None, "sprites/grassland.png", (34, 139, 34), True),
    "rock": Tile("sprites/mountain.png", "sprites/grassland.png", (128, 128, 128), False),
    "hills": Tile(None, "sprites/hills.png", (34, 139, 34), True),
    "chest": Tile("sprites/chest_trans.png", None, (139, 69, 19), True),
    "avatar": Tile("sprites/avatar.png", None, (128, 128, 128), False),
    "britannia": Tile("sprites/castle.png", None, (128, 128, 128), True),
    "merchant": Tile("sprites/merchant.png", None, (165, 42, 42), False),
    "bricks": Tile(None, "sprites/bricks.png", (128, 128, 128), True),
    "weaponshoppe": Tile("sprites/weaponshoppe.png", "sprites/bricks.png", (165, 42, 42), False),
    "arch": Tile("sprites/arch.png", "sprites/bricks.png", (165, 42, 42), True),
    "castle_stone": Tile(None, "sprites/castle_stone.png", (128, 128, 128), False),
    "trollbossspawn": Tile("sprites/troll.png", "sprites/hills.png", (128, 128, 128), True),
    "chestruby": Tile("sprites/chest_trans.png", "sprites/grassland.png", (139, 69, 19), True),
    "adventurer": Tile("sprites/merchant.png", None, (165, 42, 42), False)
    
}

def is_tile_passable(tile_type):
    """
    Returns True if the tile is passable.
    For hills, there's a 70% chance of being passable.
    """
    if tile_type == "hills":
        # Using random.random() gives a float between 0.0 and 1.0.
        # Passable if the value is less than 0.7 (70% chance)
        return random.random() < 0.7
    # For other tiles, rely on the tile property
    return True
