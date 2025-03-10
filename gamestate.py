import pygame
import random
from ui import UI, Dialog

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI
level1done = False
level2done = False
level3done = False
level4done = False
level5done = False


class PlayerStats:
    def __init__(
        self, level, hitpoints, maxhp, strength, gold, xp, weapon, armor, potions, item1, item2, item3, item4, item5
    ):
        self.level = level
        self.hitpoints = hitpoints
        self.maxhp = maxhp
        self.strength = strength
        self.gold = gold
        self.xp = xp
        self.weapon = weapon
        self.armor = armor
        self.potions = potions
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        self.item4 = item4
        self.item5 = item5
        

    def levelup(self, bosstrspawnf):
        pygame.mixer.init()
        global level1done, level2done, level3done, level4done, level5done
        if self.xp >= 100 and level1done == False:  # Level up when XP reaches 100
            pygame.mixer.music.load("music/levelup.mp3")
            pygame.mixer.music.play()  
            self.level += 1
            self.maxhp += random.randint(5, 10)  # Increase HP
            self.hitpoints = self.maxhp
            self.strength += random.randint(1, 3)  # Increase Strength
            ui_panel.update_stats(player)
            level1done = True
        elif (
            self.xp >= 350 and level1done == True and level2done == False
        ):  # Level up when XP reaches 100
            pygame.mixer.music.load("music/levelup.mp3")
            pygame.mixer.music.play()  
            self.level += 1
            self.maxhp += random.randint(10, 20)  # Increase HP
            self.hitpoints = self.maxhp
            self.strength += random.randint(2, 4)  # Increase Strength
            ui_panel.update_stats(player)
            level2done = True
        elif (
            self.xp >= 800 and level1done and level2done and not level3done
        ):  # Level up when XP reaches 100
            pygame.mixer.music.load("music/levelup.mp3")
            pygame.mixer.music.play()  
            self.level += 1
            self.maxhp += random.randint(20, 30)  # Increase HP
            self.hitpoints = self.maxhp
            self.strength += random.randint(3, 4)  # Increase Strength
            ui_panel.update_stats(player)
            level3done = True
            
        elif (
            self.xp >= 1500 and level1done and level2done and level3done and not level4done
        ):  # Level up when XP reaches 100
            pygame.mixer.music.load("music/levelup.mp3")
            pygame.mixer.music.play()  
            self.level += 1
            self.maxhp += random.randint(25, 35)  # Increase HP
            self.hitpoints = self.maxhp
            self.strength += random.randint(3, 5)  # Increase Strength
            ui_panel.update_stats(player)
            level4done = True
          
        elif (    
            self.xp >= 2500 and level1done and level2done and level3done and level4done and not level5done
        ):  # Level up when XP reaches 100
            pygame.mixer.music.load("music/levelup.mp3")
            pygame.mixer.music.play()  
            self.level += 1
            self.maxhp += random.randint(35, 50)  # Increase HP
            self.hitpoints = self.maxhp
            self.strength += random.randint(4, 6)  # Increase Strength
            ui_panel.update_stats(player)
            level5done = True
        return bosstrspawnf

# Initialize Player Stats
initial_hp=random.randint(30, 40)

player = PlayerStats(
    level=1,
    hitpoints=initial_hp,
    maxhp=initial_hp,
    strength=random.randint(5, 10),
    gold=0,
    xp=0,
    weapon="Fists",
    armor="Furs",
    potions=1,
    item1=0,
    item2=0,
    item3=0,
    item4=0,
    item5=0
)

# Initialize UI Panel
ui_panel = UI(player)  # ✅ Now pygame is initialized before UI is created
dialog_panel = Dialog()
