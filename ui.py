import pygame

class UI:
    def __init__(self, player):
        self.player = player
        self.WIDTH = 250  # Panel width
        self.HEIGHT = 800  # Panel height
        self.BACKGROUND_COLOR = (50, 50, 50)  # Dark gray panel
        self.TEXT_COLOR = (255, 255, 255)  # White text
        self.font = pygame.font.Font(None, 30)

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
        ]

        y_offset = 20
        for stat in stats:
            text_surface = self.font.render(stat, True, self.TEXT_COLOR)
            screen.blit(text_surface, (panel_x + 10, y_offset))
            y_offset += 40

    def update_stats(self, player):
        """Updates the UI panel when player stats change."""
        self.player = player


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

    def handle_click(self, pos):
        """Detects if a button was clicked and returns action."""
        for option, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return option  # Return "Buy" or "Sell"
        return None
