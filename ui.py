import pygame
import merchantwares  # ✅ Import the module itself, not specific items

class UI:
    def __init__(self, player):
        self.player = player
        self.WIDTH = 400  # Panel width
        self.HEIGHT = 800  # Panel height
        self.BACKGROUND_COLOR = (50, 50, 50)  # Dark gray panel
        self.TEXT_COLOR = (255, 255, 255)  # White text
        self.font = pygame.font.Font(None, 30)

        # Button properties
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.button_text_color = (255, 255, 255)
        self.buttons = {}  # ✅ Store button rects to persist between frames

    def draw(self, screen):
        """Draws the stats panel on the right side of the game window."""
        panel_x = screen.get_width() - self.WIDTH
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (panel_x, 0, self.WIDTH, self.HEIGHT))
        stat_font = pygame.font.Font(None, 30)   # Font for stats
        button_font = pygame.font.Font(None, 20) # Smaller font for buttons

        # ✅ Display Player Stats
        stats = [
            f"Level: {self.player.level}",
            f"HP: {self.player.hitpoints}",
            f"Strength: {self.player.strength}",
            f"Gold: {self.player.gold}",
            f"XP: {self.player.xp}",
            f"Weapon: {self.player.weapon}",
            f"Armor: {self.player.armor}",
            f"Salves: {self.player.potions}",
            f"Item 1: {self.player.item1}",
            f"Item 2: {self.player.item2}",
            f"Item 3: {self.player.item3}",
            f"Item 4: {self.player.item4}",
            f"Item 5: {self.player.item5}",
        ]

        y_offset = 20
        for stat in stats:
            text_surface = stat_font.render(stat, True, self.TEXT_COLOR)
            screen.blit(text_surface, (panel_x + 10, y_offset))

            # ✅ If the stat represents an item, create Equip & Drop buttons
            if "Item" in stat:
                item_slot = stat.split(":")[0].strip()  # Extract "Item 1", "Item 2", etc.

                # Equip button
                equip_rect = pygame.Rect(panel_x + 250, y_offset, 50, 25)
                self.buttons[f"Equip_{item_slot}"] = equip_rect  # ✅ Store button

                # Drop button
                drop_rect = pygame.Rect(panel_x + 320, y_offset, 50, 25)
                self.buttons[f"Drop_{item_slot}"] = drop_rect  # ✅ Store button

                # ✅ Draw buttons
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect, text in [(equip_rect, "Equip"), (drop_rect, "Drop")]:
                    color = self.button_hover_color if rect.collidepoint(mouse_x, mouse_y) else self.button_color
                    pygame.draw.rect(screen, color, rect)

                    # ✅ Use the smaller button font
                    button_text_surface = button_font.render(text, True, self.button_text_color)
                    screen.blit(button_text_surface, (rect.x + 5, rect.y + 5))

            y_offset += 40  # Move down for the next stat

        # ✅ "Use" Button for Potions
        use_rect = pygame.Rect(1000, 297, 80, 30)
        self.buttons["Use"] = use_rect  # Store button reference

        # Draw "Use" button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color = self.button_hover_color if use_rect.collidepoint(mouse_x, mouse_y) else self.button_color
        pygame.draw.rect(screen, color, use_rect)

        text_surface = button_font.render("Use", True, self.button_text_color)
        screen.blit(text_surface, (use_rect.x + 20, use_rect.y + 5))

    def handle_click(self, pos):
        """Detects if a button was clicked and returns action."""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return button_name  # ✅ Return button name like "Equip_Item 1", "Use", etc.
        return None

    def update_stats(self, player):
        """Updates the UI panel when player stats change."""
        self.player = player

    def usepotion(self, player):
        """Uses a healing potion."""
        if player.potions > 0:
            print("✅ Using healing potion")

            # ✅ Heal player but do not exceed max HP
            player.hitpoints = min(player.hitpoints + 20, player.maxhp)

            player.potions -= 1  # ✅ Reduce potion count
            self.update_stats(player)  # ✅ Update UI panel
        else:
            print("⚠️ No potions left!")

    def equip_item(self, pos, player):
        """Detects if an Equip button was clicked and equips the item."""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos) and "Equip_" in button_name:
                item_slot = button_name.replace("Equip_", "").strip()
                item_attr = item_slot.lower().replace(" ", "")
                item_name = getattr(player, item_attr, None)

                if not item_name:
                    print(f"⚠️ No item found in {item_slot}")
                    return None

                merchant_key = item_name.lower()
                if merchant_key not in merchantwares.MERCHANT_WARES:
                    print(f"⚠️ Item '{item_name}' not found in merchantwares!")
                    return None  

                item_data = merchantwares.MERCHANT_WARES[merchant_key]

                if item_data.isweapon:
                    old_weapon = player.weapon  # ✅ Store current weapon
                    player.weapon = item_name  # ✅ Equip new weapon
                    
                    print(f"✅ Equipped weapon: {item_name}")
                    
                    # ✅ Remove the equipped item from inventory
                    if player.item1 == item_name:
                        player.item1 = 0
                    elif player.item2 == item_name:
                        player.item2 = 0
                    elif player.item3 == item_name:
                        player.item3 = 0
                    elif player.item4 == item_name:
                        player.item4 = 0    
                    elif player.item5 == item_name:
                        player.item5 = 0

                    # ✅ Store the old weapon in inventory (unless it's "Fists")
                    if old_weapon and old_weapon.lower() != "fists" and old_weapon not in [
                        player.item1, player.item2, player.item3, player.item4, player.item5
                    ]:
                        if not player.item1:
                            player.item1 = old_weapon
                        elif not player.item2:
                            player.item2 = old_weapon
                        elif not player.item3:
                            player.item3 = old_weapon
                        elif not player.item4:
                            player.item4 = old_weapon
                        elif not player.item5:
                            player.item5 = old_weapon
                        else:
                            print(f"⚠️ No inventory space! {old_weapon} was dropped!")

                elif item_data.isarmor:
                    old_armor = player.armor  # ✅ Store current weapon
                    player.armor = item_name  # ✅ Equip new weapon
                    
                    print(f"✅ Equipped weapon: {item_name}")
                    
                    # ✅ Remove the equipped item from inventory
                    if player.item1 == item_name:
                        player.item1 = 0
                    elif player.item2 == item_name:
                        player.item2 = 0
                    elif player.item3 == item_name:
                        player.item3 = 0
                    elif player.item4 == item_name:
                        player.item4 = 0    
                    elif player.item5 == item_name:
                        player.item5 = 0

                    # ✅ Store the old weapon in inventory (unless it's "Fists")
                    if old_armor and old_armor.lower() != "furs" and old_armor not in [
                        player.item1, player.item2, player.item3, player.item4, player.item5
                    ]:
                        if not player.item1:
                            player.item1 = old_armor
                        elif not player.item2:
                            player.item2 = old_armor
                        elif not player.item3:
                            player.item3 = old_armor
                        elif not player.item4:
                            player.item4 = old_armor
                        elif not player.item5:
                            player.item5 = old_armor
                        else:
                            print(f"⚠️ No inventory space! {old_armor} was dropped!")

                else:
                    print(f"⚠️ {item_name} is not equippable!")

                self.update_stats(player)
                return item_name

        return None
    
    def drop_item(self, pos, player):
        """Drops an item from the inventory if the corresponding drop button is clicked."""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos) and button_name.startswith("Drop_"):
                # Extract slot info (e.g. "Drop_Item 1" → "Item 1")
                slot = button_name.replace("Drop_", "").strip()
                dropped_item = None
                if slot == "Item 1":
                    dropped_item = player.item1
                    player.item1 = 0
                elif slot == "Item 2":
                    dropped_item = player.item2
                    player.item2 = 0
                elif slot == "Item 3":
                    dropped_item = player.item3
                    player.item3 = 0
                elif slot == "Item 4":
                    dropped_item = player.item4
                    player.item4 = 0
                elif slot == "Item 5":
                    dropped_item = player.item5
                    player.item5 = 0
                if dropped_item:
                    print(f"⚠️ Dropped {dropped_item} from {slot}.")
                else:
                    print(f"⚠️ No item in {slot} to drop.")
                return dropped_item
        return None

        


class Dialog:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 200
        self.BACKGROUND_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        self.font = pygame.font.Font(None, 30)
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.button_text_color = (255, 255, 255)
        self.buttons = {}

    def draw(self, screen, dialog_text, show_buttons=True):
        panel_y = screen.get_height() - self.HEIGHT
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (0, panel_y, self.WIDTH, self.HEIGHT))
        y_offset = panel_y + 20
        for line in dialog_text:
            text_surface = self.font.render(line, True, self.TEXT_COLOR)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 40

        # Only draw the buy/sell buttons if show_buttons is True
        if show_buttons:
            self.buttons = {}  # Reset button storage
            button_x = 50
            button_y = panel_y + 120
            button_width = 100
            button_height = 40
            spacing = 20
            for option in ["Buy", "Sell"]:
                rect = pygame.Rect(button_x, button_y, button_width, button_height)
                self.buttons[option] = rect
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, self.button_hover_color, rect)
                else:
                    pygame.draw.rect(screen, self.button_color, rect)
                text_surface = self.font.render(option, True, self.button_text_color)
                screen.blit(text_surface, (button_x + 25, button_y + 10))
                button_x += button_width + spacing


    def handle_purchase_click(self, pos, player):
        """Detects if a Buy button was clicked and processes purchase."""
        for item_name, rect in self.buttons.items():
            if rect.collidepoint(pos):  # ✅ Check if the button was clicked
                key_name = item_name.lower()  # ✅ Normalize to lowercase
                if key_name in merchantwares.MERCHANT_WARES:
                     item_data = merchantwares.MERCHANT_WARES[key_name]

                else:
                    print(f"⚠️ Item '{item_name}' not found in merchantwares!")
                    return None  # ✅ Exit if the item doesn't exist

                if player.gold >= item_data.purchvalue:
                    player.gold -= item_data.purchvalue  # ✅ Deduct gold
                    print(f"✅ Purchased {item_data.item_name} for {item_data.purchvalue} gold!")

                    # ✅ Limit potions to 5 max
                    if item_data.item_name == "Healing Salve":
                        if player.potions >= 5:
                            print("⚠️ You can only carry 5 potions!")
                            player.gold += item_data.purchvalue  # Refund
                            return None
                        player.potions += 1
                    else:
                        # ✅ Check inventory slots and assign the item correctly
                        if not player.item1:  # First slot empty
                            player.item1 = item_data.item_name
                            print(f"👜 Added {item_data.item_name} to inventory slot 1")
                        elif not player.item2:  # Second slot empty
                            player.item2 = item_data.item_name
                            print(f"👜 Added {item_data.item_name} to inventory slot 2")
                        elif not player.item3:  # Second slot empty
                            player.item3 = item_data.item_name
                            print(f"👜 Added {item_data.item_name} to inventory slot 3")
                        elif not player.item4:  # Second slot empty
                            player.item4 = item_data.item_name
                            print(f"👜 Added {item_data.item_name} to inventory slot 4")
                        elif not player.item5:  # Second slot empty
                            player.item5 = item_data.item_name
                            print(f"👜 Added {item_data.item_name} to inventory slot 5")
                        else:
                            print("⚠️ Inventory full! Sell or drop an item.")
                            player.gold += item_data.purchvalue  # Refund gold
                            return None
                        print(f"Inventory: Slot 1 = {player.item1}, Slot 2 = {player.item2}")


                else:
                    print("⚠️ Not enough gold!")
                    return None

                return item_data.item_name  # ✅ Use stored name instead of key
        return None  # ✅ Return None if no item was clicked

    def handle_click(self, pos):
        """Detects if a button was clicked in the main merchant menu and returns action."""
        for option, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return option  # ✅ Return "Buy" or "Sell"
        return None  # ✅ Return None if no button was clicked

    def draw2(self, screen, dialog_text):
        """Draws the merchant wares with purchase buttons."""
        self.font = pygame.font.Font(None, 23)
        panel_y = screen.get_height() - self.HEIGHT
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (0, panel_y, self.WIDTH, self.HEIGHT))

        # Display text
        y_offset = panel_y + 15
        self.buttons = {}  # Reset buttons

        for line in dialog_text:
            text_surface = self.font.render(line, True, self.TEXT_COLOR)
            screen.blit(text_surface, (10, y_offset))

            # Ensure this line has an item to buy
            if ":" in line:
                item_name = line.split(":")[0].strip()  # ✅ Extract exact item name
                button_x = 400
                button_y = y_offset
                button_width = 80
                button_height = 30

                rect = pygame.Rect(button_x, button_y, button_width, button_height)
                self.buttons[item_name] = rect  # ✅ Store the full name (e.g., "Vorpal Blade")

                # Change color if hovering
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, self.button_hover_color, rect)
                else:
                    pygame.draw.rect(screen, self.button_color, rect)

                # Draw "Buy" text
                text_surface = self.font.render("Buy", True, self.button_text_color)
                screen.blit(text_surface, (button_x + 20, button_y + 5))

            y_offset += 31  # Move down for next item
