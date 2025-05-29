import pygame
import random

pygame.init()
pygame.font.init()

# ✅ Set up the display *before* loading images
TILE_SIZE = 50
GRID_SIZE = 10  # 15x15 map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE , TILE_SIZE * GRID_SIZE  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPAWN_INTERVAL = 200  # Frames per spawn attempt

player_sprite = pygame.image.load("sprites/avatar.png")  # Load avatar
player_sprite = pygame.transform.scale(
    player_sprite, (TILE_SIZE, TILE_SIZE)
)
player_x, player_y = 5,5
farm_sprite = pygame.image.load("sprites/farm.png")  # Load avatar
farm_sprite = pygame.transform.scale(
    farm_sprite, (TILE_SIZE, TILE_SIZE)
)
player_x, player_y = 5,5

budget = 15  # in cents
placed_farms = []  # stores (x, y) tuples of placed farms
icon_farm_pos = (9, 9)
moving_farm = False

FONT = pygame.font.SysFont("Arial", 20)
income_timer = 0  # tracks time in milliseconds




# ✅ Set up the display first!
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Farmvillage")
clock = pygame.time.Clock()  # Controls frame rate

# Game loop
running = True
redraw_needed = True
frame_counter = 0



while running:
    clock.tick(60)
    # Update income every 30 seconds (30,000 ms)
    income_timer += clock.get_time()
    if income_timer >= 10000:
        farm_income = len(placed_farms) * 5
        budget += farm_income
        income_timer = 0

    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y
            if event.key == pygame.K_LEFT and player_x > 0:
                new_x -= 1
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                new_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                new_y += 1
            player_x, player_y = new_x, new_y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_col = mouse_x // TILE_SIZE
            clicked_row = mouse_y // TILE_SIZE

            if not moving_farm:
                if (clicked_col, clicked_row) == icon_farm_pos:
                    moving_farm = True
            else:
             # Only place if enough money and not placing on icon farm
                if budget >= 5 and (clicked_col, clicked_row) != icon_farm_pos:
                    placed_farms.append((clicked_col, clicked_row))
                    budget -= 5
                moving_farm = False
       


    # ✅ Clear screen and draw every frame
    screen.fill(BLACK)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(
                screen,
                BLACK,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                1  # Outline only
            )

    screen.blit(player_sprite, (player_x * TILE_SIZE, player_y * TILE_SIZE))
    
    # Always draw the farm icon
    screen.blit(farm_sprite, (icon_farm_pos[0] * TILE_SIZE, icon_farm_pos[1] * TILE_SIZE))

    # Draw all placed farms
    for fx, fy in placed_farms:
        screen.blit(farm_sprite, (fx * TILE_SIZE, fy * TILE_SIZE))
        
    # Show money in dollars
    money_text = FONT.render(f"Money: ${budget / 100:.2f}", True, WHITE)
    screen.blit(money_text, (10, 10))


    pygame.display.update()

pygame.quit()