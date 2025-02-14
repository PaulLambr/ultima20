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
            print(f"🎉 Level up! You are now level {self.level}!")
            print(f"New Stats: HP={self.hitpoints}, Strength={self.strength}")

# Initialize Player Stats
player = PlayerStats(
    level=1,
    hitpoints=random.randint(10, 20),
    strength=random.randint(5, 10),
    gold=0,
    xp=0,
    weapon="None",
    armor="None"
)

# Example usage
print(f"Player HP: {player.hitpoints}, Strength: {player.strength}")

# Simulate gaining XP and leveling up
player.xp += 100
player.levelup()
