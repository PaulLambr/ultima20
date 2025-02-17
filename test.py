import pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FPS Test")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
