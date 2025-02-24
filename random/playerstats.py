import random


class PlayerStats:
    def __init__(self, level, hitpoints, strength, gold, xp, weapon, armor):
        self.level = level
        self.hitpoints = hitpoints
        self.strength = strength
        self.gold = gold
        self.xp = xp
        self.weapon = weapon
        self.armor = armor

    def levelup(self):
        if self.xp >= 100:  # Level up when XP reaches 100
            self.xp = 0  # Reset XP
            self.level += 1
            self.hitpoints += random.randint(5, 10)  # Increase HP
            self.strength += random.randint(2, 5)  # Increase Strength


# Initialize Player Stats
player = PlayerStats(
    level=5,
    hitpoints=random.randint(10, 20),
    strength=random.randint(5, 10),
    gold=500,
    xp=0,
    weapon="None",
    armor="Leather Tunic",
)
