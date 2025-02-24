import pygame

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI


class MerchantWares:
    def __init__(
        self, availability, purchvalue, sellvalue, damage, protection, healpower, item_name, isweapon, isarmor, cansell
    ):
        self.availability = availability
        self.purchvalue = purchvalue
        self.sellvalue = sellvalue
        self.damage = damage
        self.protection = protection
        self.healpower = healpower
        self.item_name = item_name
        self.isweapon = isweapon
        self.isarmor = isarmor
        self.cansell = cansell

    @staticmethod
    def showwares():
        dialog_text = ["What would you like to purchase?"]
        for key, details in MERCHANT_WARES.items():
            if details.availability == "all":
                dialog_text.append(f"{details.item_name}: {details.purchvalue} gold")
        return dialog_text



# ✅ Define `MERCHANT_WARES` as a global dictionary
MERCHANT_WARES = {
    "vorpal blade": MerchantWares("all", 100, 50, 5, None, None, "Vorpal Blade", True, False, True),
    "morningstar": MerchantWares("all", 250, 125, 8, None, None, "Morningstar", True, False, True),
    "leather armor": MerchantWares("all", 200, 100, None, .8, None, "Leather Armor", False, True, True),
    "hauberk": MerchantWares("all", 500, 250, None, .6, None, "Hauberk", False, True, True),
    "healing salve": MerchantWares("all", 30, None, None, None, 25, "Healing Salve", False, False, False),
    "holy ruby": MerchantWares(None, 30, None, None, None, None, "Holy Ruby", False, False, False),
}
