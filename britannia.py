import pygame
from ui import UI, Dialog
from gamestate import player, ui_panel, PlayerStats, dialog_panel
from tiletypes.tiletypes import TILE_TYPES
from utils import talk
from merchantwares import MerchantWares  # Import it properly


# Constants for Battle Screen
CASTLE_GRID_SIZE = 13
TILE_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def britannia_castle():
    pygame.init()
    talk_mode = False
    show_dialog = False  # ✅ Track whether the dialog panel is visible
    show_dialog2 = False
    dialog_text = []  # ✅ Store the current dialog text
    selected_action = None
    selected_item = None

    player_sprite = pygame.image.load("sprites/avatar.png").convert_alpha()
    player_sprite = pygame.transform.scale(player_sprite, (TILE_SIZE, TILE_SIZE))

    WIDTH, HEIGHT = (
        TILE_SIZE * CASTLE_GRID_SIZE + ui_panel.WIDTH,
        TILE_SIZE * CASTLE_GRID_SIZE + dialog_panel.HEIGHT,
    )
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome to Britannia Castle!")

    # Generate castle grid
    castle_map = [["grassland"] * CASTLE_GRID_SIZE for _ in range(CASTLE_GRID_SIZE)]
    castle_map[7][7] = "hills"
    castle_map[2][3] = "merchant"

    # Player starts in the center
    player_x, player_y = 7, 7
    merchant_mode = False

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ✅ Handle Keyboard Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    talk_mode = True
                    pending_talk = None
                    print("Talk mode activated. Press a direction key.")
                    continue

                if talk_mode:
                    pending_talk = event.key
                    talk_mode = False

                    # Determine conversation location
                    talk_x, talk_y = player_x, player_y
                    if pending_talk == pygame.K_LEFT:
                        talk_x -= 1
                    elif pending_talk == pygame.K_RIGHT:
                        talk_x += 1
                    elif pending_talk == pygame.K_UP:
                        talk_y -= 1
                    elif pending_talk == pygame.K_DOWN:
                        talk_y += 1

                    # Ensure within bounds
                    if (
                        0 <= talk_x < CASTLE_GRID_SIZE
                        and 0 <= talk_y < CASTLE_GRID_SIZE
                    ):
                        show_dialog, dialog_text = talk(
                            player_x, player_y, pending_talk, castle_map
                        )  # ✅ Get dialog data

                # ✅ Allow closing dialog with ESC
                if event.key == pygame.K_ESCAPE:
                    show_dialog = False  # Close dialog

                # ✅ Move the player ONLY IF the dialog is NOT open
                if not show_dialog:
                    new_x, new_y = player_x, player_y

                    if event.key == pygame.K_LEFT and player_x > 0:
                        new_x -= 1
                    if event.key == pygame.K_RIGHT and player_x < CASTLE_GRID_SIZE - 1:
                        new_x += 1
                    if event.key == pygame.K_UP and player_y > 0:
                        new_y -= 1
                    if event.key == pygame.K_DOWN and player_y < CASTLE_GRID_SIZE - 1:
                        new_y += 1

                    if TILE_TYPES[castle_map[new_y][new_x]].passable:
                        player_x, player_y = new_x, new_y

                    if new_x == 7 and new_y == 7:
                        print("Returning to the overworld...")
                        return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_dialog:
                    selected_action = dialog_panel.handle_click(
                        event.pos
                    )  # ✅ Get "Buy" or "Sell"

                    if selected_action == "Buy":
                        print("🛒 Entering merchant's inventory...")
                        dialog_text = (
                            MerchantWares.showwares()
                        )  # ✅ Capture updated dialog
                        show_dialog = False  # Hide the first dialog
                        show_dialog2 = True  # ✅ Show the merchant inventory

                    elif selected_action == "Sell":
                        print("💰 Opening player inventory for selling...")
                        # TODO: Add selling logic here

                elif (
                    show_dialog2
                ):  # ✅ Handle purchasing when merchant inventory is shown
                    selected_item = dialog_panel.handle_purchase_click(
                        event.pos, player
                    )

                    if selected_item:  # ✅ Ensure the player actually clicked an item
                        print(
                            f"\nYou purchased {selected_item}"
                        )  # ✅ Print correct item

        # Draw the screen
        screen.fill(BLACK)
        ui_panel.draw(screen)

        for row in range(CASTLE_GRID_SIZE):
            for col in range(CASTLE_GRID_SIZE):
                tile_type = castle_map[row][col]
                tile = TILE_TYPES[tile_type]

                if tile.background2:
                    background_scaled = pygame.transform.scale(
                        tile.background2, (TILE_SIZE, TILE_SIZE)
                    )
                    screen.blit(background_scaled, (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    pygame.draw.rect(
                        screen,
                        tile.color,
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )

                if tile.sprite:
                    current_tile2 = castle_map[player_y][player_x]
                    tile.getbg(current_tile2)
                    redraw_needed = True

                    if tile.background2:
                        background_scaled = pygame.transform.scale(
                            tile.background2, (TILE_SIZE, TILE_SIZE)
                        )  # Ensure correct size
                        screen.blit(
                            background_scaled, (col * TILE_SIZE, row * TILE_SIZE)
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            tile.color,
                            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        )
                    sprite_scaled = pygame.transform.scale(
                        tile.sprite, (TILE_SIZE, TILE_SIZE)
                    )  # Ensure correct size
                    screen.blit(sprite_scaled, (col * TILE_SIZE, row * TILE_SIZE))

        screen.blit(player_sprite, (player_x * TILE_SIZE, player_y * TILE_SIZE))

        if show_dialog:  # ✅ Only draw dialog if active
            dialog_panel.draw(screen, dialog_text)

        if show_dialog2:
            dialog_panel.draw2(screen, dialog_text)

        pygame.display.update()

    return
