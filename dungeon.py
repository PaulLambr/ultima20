import pygame
import random

pygame.init()
pygame.font.init()

# ✅ Set up the display *before* loading images
TILE_SIZE = 50
GRID_SIZE = 15  # 15x15 map
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE , TILE_SIZE * GRID_SIZE  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)

player_x, player_y = 1,1
door_x, door_y = 1,2
orc_x, orc_y = 1, 3

enemy_present = False
enemy_text = False

def draw_door():
    if player_x == door_x and (door_y - player_y) == 1:
        # Draw a small rectangle in the middle of the screen (as if 3 tiles away)
        door_width = TILE_SIZE // 2
        door_height = TILE_SIZE 
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        rect = pygame.Rect(
            center_x - door_width // 2,
            center_y - door_height // 2,
            door_width,
            door_height
        )
        pygame.draw.rect(screen, BLACK, rect)  # Background
        pygame.draw.rect(screen, LIGHT_GREEN, rect, 2)  # Outline
        
    elif player_x == door_x and (door_y - player_y) == 0:
        # Draw a small rectangle in the middle of the screen (as if 3 tiles away)
        door_width = TILE_SIZE *2
        door_height = TILE_SIZE *4
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        rect = pygame.Rect(
            center_x - door_width // 2,
            center_y - door_height // 2,
            door_width,
            door_height
        )
        pygame.draw.rect(screen, BLACK, rect)  # Background
        pygame.draw.rect(screen, LIGHT_GREEN, rect, 2)  # Outline
        
 
def draw_enemy():
    if enemy_present:
        screen.blit(orc_sprite, (200, 200))
        return "You have penetrated my most sacred and odious lair, insolent hero type"
    return None

    
def dialog(text):
    if not text:
        return
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (10, 700))

        
# ✅ Set up the display first!
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
clock = pygame.time.Clock()  # Controls frame rate

orc_sprite = pygame.image.load("sprites/orc.png").convert_alpha()  # Load avatar
orc_sprite = pygame.transform.scale(
    orc_sprite, (350, 350)
) 

# Game loop
running = True
redraw_needed = True
frame_counter = 0


while running:
    clock.tick(60)
      
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
                new_y += 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                new_y -= 1
            player_x, player_y = new_x, new_y
        
            enemy_present = (player_x, player_y) == (orc_x, orc_y)
            

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_col = mouse_x // TILE_SIZE
            clicked_row = mouse_y // TILE_SIZE


    screen.fill(BLACK)

    # Draw tile grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(
                screen,
                BLACK,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                1
            )
            
   
    # Draw the door if conditions are met
    draw_door()
    enemy_text = draw_enemy()
    dialog(enemy_text)

    
    pygame.display.update()

pygame.quit()