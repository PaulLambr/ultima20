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
