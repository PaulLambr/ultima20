import pygame

# ✅ Ensure pygame is initialized first
pygame.init()  # 🔥 This must run before creating fonts in UI


class MerchantWares:
    def __init__(
        self, availability, purchvalue, sellvalue, damage, protection, healpower, item_name
    ):
        self.availability = availability
        self.purchvalue = purchvalue
        self.sellvalue = sellvalue
        self.damage = damage
        self.protection = protection
        self.healpower = healpower
        self.item_name = item_name

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
    "vorpal blade": MerchantWares("all", 100, 50, 10, None, None, "Vorpal Blade"),
    "morningstar": MerchantWares("all", 250, 125, 15, None, None, "Morningstar"),
    "leather armor": MerchantWares("all", 200, 100, None, 50, None, "Leather Armor"),
    "hauberk": MerchantWares("all", 500, 250, None, 100, None, "Hauberk"),
    "healing salve": MerchantWares("all", 30, None, None, None, 25, "Healing Salve"),
}
