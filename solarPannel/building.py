import pygame
import sys

def run(screen):
    # Initialize Pygame
    pygame.init()
    WIDTH, HEIGHT = 1280,720

    background_image = pygame.image.load('images/gameBackground.png')  
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Screen dimensions
    screen 
    pygame.display.set_caption("Solar Panel Assembly")

    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GRAY = (200, 200, 200)

    # Load component images
    frame = pygame.image.load('images/frame.png')
    frame = pygame.transform.scale(frame, (140, 80))
    glass = pygame.image.load('images/glass.png')
    glass = pygame.transform.scale(glass, (120, 60))
    silicon = pygame.image.load('images/silicon.png')
    silicon = pygame.transform.scale(silicon, (100, 50))
    backsheet = pygame.image.load('images/backsheet.png')
    backsheet = pygame.transform.scale(backsheet, (100, 60))

    # Components and their target positions
    components = [
        {"name": "frame", "surface": frame, "pos": [50, 500], "target": pygame.Rect(150, 400, 140, 80), "assembled": False, "order": 1},
        {"name": "glass", "surface": glass, "pos": [200, 500], "target": pygame.Rect(150, 300, 120, 60), "assembled": False, "order": 2},
        {"name": "silicon", "surface": silicon, "pos": [350, 500], "target": pygame.Rect(150, 200, 100, 50), "assembled": False, "order": 3},
        {"name": "backsheet", "surface": backsheet, "pos": [500, 500], "target": pygame.Rect(150, 100, 100, 60), "assembled": False, "order": 4}
    ]

    dragging = None
    panel_assembled = False
    current_order = 1

    # Font for displaying text
    font = pygame.font.SysFont('Arial', 24)

    # Function to draw the components and their labels
    def draw_components():
        for component in components:
            if not component["assembled"]:
                # Draw the component surface
                screen.blit(component["surface"], component["pos"])

                # Label each component
                label = font.render(component["name"], True, (0, 0, 0))
                screen.blit(label, (component["pos"][0], component["pos"][1] - 25))


    # Game state
    game_state = "playing"

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)

        if game_state == "intro":
            screen.blit(intro_image, (0, 0))
            message = font.render("Press SPACE to continue", True, (0, 0, 0))
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 50))

        elif game_state == "playing":
            screen.blit(background_image, (0, 0))

            # Draw target areas
            for component in components:
                pygame.draw.rect(screen, GRAY, component["target"], 2)
                if component["assembled"]:
                    pygame.draw.rect(screen, GREEN, component["target"], 2)

            # Draw components
            draw_components()

            # Show current order
            order_message = font.render(f"Current Order: {current_order}", True, (0, 0, 0))
            screen.blit(order_message, (WIDTH - 200, HEIGHT - 40))

            # Check if panel is fully assembled
            if all(component["assembled"] for component in components):
                panel_assembled = True

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == "intro" and event.key == pygame.K_SPACE:
                    game_state = "playing"
                elif game_state == "playing" and panel_assembled:
                    running = False  # Close the game when SPACE is pressed after assembly

            if game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for component in components:
                        if pygame.Rect(component["pos"], component["surface"].get_size()).collidepoint(event.pos):
                            dragging = component

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        if dragging["target"].collidepoint(event.pos) and dragging["order"] == current_order:
                            dragging["pos"] = dragging["target"].topleft
                            dragging["assembled"] = True
                            current_order += 1
                        dragging = None

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        dragging["pos"][0] += event.rel[0]
                        dragging["pos"][1] += event.rel[1]

        # Update the screen
        pygame.display.flip()

