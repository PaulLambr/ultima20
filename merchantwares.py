import pygame
import random
from ui import UI, Dialog

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI


class MerchantWares:
    def __init__(self, availability, purchvalue, sellvalue, damage, protection, healpower):
        self.availability = availability
        self.purchvalue = purchvalue
        self.sellvalue = sellvalue
        self.damage = damage
        self.protection = protection
        self.healpower = healpower

    def merchantinventory():
        #reset dialog screen, display these 5 items with the purchvalue also showing. also each item needs a button to "buy". logic to limit potions to 5 in playerinventory
        return

MERCHANT_WARES = {
    "sword": MerchantWares("all", 100, 50, 10, None, None),
    "broadaxe": MerchantWares("all", 250, 125, 15, None, None),
    "leatherarmor": MerchantWares("all", 200, 100, None, 50, None),
    "chainmail": MerchantWares("all", 500, 250, None, 100, None),
    "potions": MerchantWares("all", 30, None, None, None, 25),
    
}