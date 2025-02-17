import pygame
import random
from ui import UI, Dialog

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI
level1done=False
level2done=False
level3done=False

class PlayerStats:
    def __init__(self, level, hitpoints, strength, gold, xp, weapon, armor, potions, item1, item2):
        self.level = level
        self.hitpoints = hitpoints  
        self.strength = strength
        self.gold = gold
        self.xp = xp
        self.weapon = weapon
        self.armor = armor
        self.potions = potions
        self.item1 = item1
        self.item2 = item2

    def levelup(self):
        global level1done, level2done, level3done
        if self.xp >= 150 and level1done==False:  # Level up when XP reaches 100
            self.level += 1
            self.hitpoints += random.randint(5, 10)  # Increase HP
            self.strength += random.randint(1, 2)  # Increase Strength
            ui_panel.update_stats(player)
            level1done=True
        elif self.xp >= 300 and level1done==True and level2done==False:  # Level up when XP reaches 100
            self.level += 1
            self.hitpoints += random.randint(10, 20)  # Increase HP
            self.strength += random.randint(1, 2)  # Increase Strength
            ui_panel.update_stats(player)  
            level2done=True
        elif self.xp >= 1000 and level1done and level2done and not level3done:  # Level up when XP reaches 100
            self.level += 1
            self.hitpoints += random.randint(15, 30)  # Increase HP
            self.strength += random.randint(1, 2)  # Increase Strength
            ui_panel.update_stats(player)    
            level3done=True
    

# Initialize Player Stats
player = PlayerStats(
    level=1,
    hitpoints=random.randint(80, 90),
    strength=random.randint(5, 10),
    gold=0,
    xp=0,
    weapon="Dagger",
    armor="Cloth",
    potions=3,
    item1="Sword",
    item2=0
)

# Initialize UI Panel
ui_panel = UI(player)  # ✅ Now pygame is initialized before UI is created
dialog_panel = Dialog()
