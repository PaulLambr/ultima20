import pygame

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI


class MerchantWares:
    def __init__(
        self, availability, purchvalue, sellvalue, damage, protection, healpower, item_name, isweapon, isarmor
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

    @staticmethod
    def showwares():
        """Returns a list of available merchant wares with prices for display."""
        print("\nDisplaying merchant wares...")  # Debugging step
        dialog_text = ["What would you like to purchase?"]

        for item, details in MERCHANT_WARES.items():
            dialog_text.append(f"{details.item_name}: {details.purchvalue} gold")  # ✅ Always show the correct item name


        return dialog_text  # ✅ Return the list to update the dialog panel


# ✅ Define `MERCHANT_WARES` as a global dictionary
MERCHANT_WARES = {
    "vorpal blade": MerchantWares("all", 100, 50, 5, None, None, "Vorpal Blade", True, False),
    "morningstar": MerchantWares("all", 250, 125, 8, None, None, "Morningstar", True, False),
    "leather armor": MerchantWares("all", 1000, 100, None, 3, None, "Leather Armor", False, True),
    "hauberk": MerchantWares("all", 1000, 250, None, 8, None, "Hauberk", False, True),
    "healing salve": MerchantWares("all", 30, None, None, None, 25, "Healing Salve", False, False),
}
