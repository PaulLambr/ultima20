import pygame
import merchantwares  # ✅ Import the module itself, not specific items


class UI:
    def __init__(self, player):
        self.player = player
        self.WIDTH = 250  # Panel width
        self.HEIGHT = 800  # Panel height
        self.BACKGROUND_COLOR = (50, 50, 50)  # Dark gray panel
        self.TEXT_COLOR = (255, 255, 255)  # White text
        self.font = pygame.font.Font(None, 30)

        # Button properties
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.button_text_color = (255, 255, 255)
        self.buttons = {}  # Store button rects

    def draw(self, screen):
        """Draws the stats panel on the right side of the game window."""
        panel_x = screen.get_width() - self.WIDTH
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (panel_x, 0, self.WIDTH, self.HEIGHT))

        # Display Player Stats
        stats = [
            f"Level: {self.player.level}",
            f"HP: {self.player.hitpoints}",
            f"Strength: {self.player.strength}",
            f"Gold: {self.player.gold}",
            f"XP: {self.player.xp}",
            f"Weapon: {self.player.weapon}",
            f"Armor: {self.player.armor}",
            f"Potions: {self.player.potions}",
            f"Item 1: {self.player.item1}",
            f"Item 3: {self.player.item2}",
        ]

        y_offset = 20
        for stat in stats:
            self.font = pygame.font.Font(None, 30)
            text_surface = self.font.render(stat, True, self.TEXT_COLOR)
            screen.blit(text_surface, (panel_x + 10, y_offset))
            y_offset += 40

        # Draw buttons (Equip, Drop)
        self.buttons = {}  # Reset button storage
        self.font = pygame.font.Font(None, 15)
        button_x = 910
        button_y = 355 # Position buttons at the bottom of the panel
        button_width = 35
        button_height = 20
        spacing = 10

        for option in ["Equip", "Drop"]:
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons[option] = rect  # Store button rect

            # Change color if hovering
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, self.button_hover_color, rect)
            else:
                pygame.draw.rect(screen, self.button_color, rect)

            # Draw text
            text_surface = self.font.render(option, True, self.button_text_color)
            screen.blit(text_surface, (button_x + 5, button_y + 5))

            button_x += button_width + spacing  # Move to the right for next button

        for option in ["Use"]:
            button_x = 910
            button_y = 300
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons[option] = rect  # Store button rect

            # Change color if hovering
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, self.button_hover_color, rect)
            else:
                pygame.draw.rect(screen, self.button_color, rect)

            # Draw text
            text_surface = self.font.render(option, True, self.button_text_color)
            screen.blit(text_surface, (button_x + 5, button_y + 5))

            #button_x += button_width + spacing  # Move to the right for next button


    def handle_click(self, pos):
        """Detects if a button was clicked and returns action."""
        for option, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return option  # Return "Buy" or "Sell"
        return None

    def update_stats(self, player):
        """Updates the UI panel when player stats change."""
        self.player = player

    def usepotion(self, player):
        if player.potions > 0:
            print("Using healing potion")  
            player.hitpoints += 20
            player.potions -= 1
            self.update_stats(player)  # ✅ Update stats
            

class Dialog:
    def __init__(self):
        self.WIDTH = 800  
        self.HEIGHT = 200  
        self.BACKGROUND_COLOR = (50, 50, 50)  
        self.TEXT_COLOR = (255, 255, 255)  
        self.font = pygame.font.Font(None, 30)

        # Button properties
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)
        self.button_text_color = (255, 255, 255)
        self.buttons = {}  # Store button rects

    def draw(self, screen, dialog_text):
        """Draws the dialog panel at the bottom of the screen."""
        panel_y = screen.get_height() - self.HEIGHT  
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (0, panel_y, self.WIDTH, self.HEIGHT))

        # Display text
        y_offset = panel_y + 20
        for line in dialog_text:
            text_surface = self.font.render(line, True, self.TEXT_COLOR)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 40

        # Draw buttons (Buy, Sell)
        self.buttons = {}  # Reset button storage

        button_x = 50
        button_y = panel_y + 120  # Position buttons at the bottom of the panel
        button_width = 100
        button_height = 40
        spacing = 20

        for option in ["Buy", "Sell"]:
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.buttons[option] = rect  # Store button rect

            # Change color if hovering
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, self.button_hover_color, rect)
            else:
                pygame.draw.rect(screen, self.button_color, rect)

            # Draw text
            text_surface = self.font.render(option, True, self.button_text_color)
            screen.blit(text_surface, (button_x + 25, button_y + 10))

            button_x += button_width + spacing  # Move to the right for next button

    def handle_click(self, pos, player):
        """Detects if a Buy button was clicked and processes purchase."""
        for item_name, rect in self.buttons.items():
            if rect.collidepoint(pos):  # Check if the button was clicked
                item_key = item_name.lower()

                if item_key in merchantwares.MERCHANT_WARES:  # ✅ Reference via module
                    item_data = merchantwares.MERCHANT_WARES[item_key]

                    # Check if player has enough gold
                    if player.gold >= item_data.purchvalue:
                        player.gold -= item_data.purchvalue
                        print(f"✅ Purchased {item_name} for {item_data.purchvalue} gold!")

                    # Limit potions to 5 max
                    if item_key == "potions":
                        if player.potions >= 5:
                            print("⚠️ You can only carry 5 potions!")
                            player.gold += item_data.purchvalue  # Refund
                            return None
                        player.potions += 1
                    else:
                        # Assign to an inventory slot
                        if player.item1 is None:
                            player.item1 = item_key
                        elif player.item2 is None:
                            player.item2 = item_key
                        else:
                            print("⚠️ Inventory full! Sell or drop an item.")
                            player.gold += item_data.purchvalue  # Refund gold
                            return None
                else:
                    print("⚠️ Not enough gold!")
                return item_name
        return None

    
    def draw2(self, screen, dialog_text):
        
        """Draws the merchant wares with purchase buttons."""
        panel_y = screen.get_height() - self.HEIGHT  
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, (0, panel_y, self.WIDTH, self.HEIGHT))

        # Display text
        y_offset = panel_y + 20
        self.buttons = {}  # Reset buttons

        for line in dialog_text:
            text_surface = self.font.render(line, True, self.TEXT_COLOR)
            screen.blit(text_surface, (10, y_offset))

            # Draw Buy Button (for actual items)
            if ":" in line:  # Ensures this line has an item to buy
                item_name = line.split(":")[0].strip()
                button_x = 600  
                button_y = y_offset  
                button_width = 80  
                button_height = 30  

                rect = pygame.Rect(button_x, button_y, button_width, button_height)
                self.buttons[item_name] = rect  # Store button rect

                # Change color if hovering
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, self.button_hover_color, rect)
                else:
                    pygame.draw.rect(screen, self.button_color, rect)

                # Draw "Buy" text
                text_surface = self.font.render("Buy", True, self.button_text_color)
                screen.blit(text_surface, (button_x + 20, button_y + 5))

            y_offset += 40  # Move down for next item
