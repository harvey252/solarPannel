
import pygame
import sys
import random
def run(screen):
    # Initialize Pygame

    # Screen dimensions
    WIDTH, HEIGHT = 1200, 900

    pygame.display.set_caption("Solar Panel Disassembly")

    # Colors
    WHITE, GREEN, RED, GRAY, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (200, 200, 200), (0, 0, 0)

    # Font
    font = pygame.font.SysFont('Arial', 24)

    # Load images
    background = pygame.transform.scale(pygame.image.load("images/gameBackground.png"), (1280, 720))

    # Function to add border to an image
    def add_border(image, border_size=5):
        bordered_surface = pygame.Surface((image.get_width() + 2 * border_size, image.get_height() + 2 * border_size), pygame.SRCALPHA)
        bordered_surface.fill(WHITE)
        bordered_surface.blit(image, (border_size, border_size))
        return bordered_surface

    # Scale and load components
    scale_factor = WIDTH * 0.05 / pygame.image.load("images/frame.png").get_width()
    components = [
        {"name": "Frame", "img": "images/frame.png", "order": 1},
        {"name": "Glass", "img": "images/glass.png", "order": 2},
        {"name": "Silicon", "img": "images/silicon.png", "order": 3},
        {"name": "Backsheet", "img": "images/backsheet.png", "order": 4}
    ]

    # Preprocess images and add borders
    for component in components:
        img = pygame.image.load(component["img"])
        component["surface"] = add_border(pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))))

    # Shuffle only the frame component
    random.shuffle(components)

    # Set vertical gap and starting positions
    max_height = HEIGHT - 200
    total_height = sum(comp["surface"].get_height() for comp in components)
    vertical_gap = max(20, (max_height - total_height) // (len(components) - 1)-100)
    start_y = 100

    # Assign positions
    for i, comp in enumerate(components):
        comp["pos"] = [100, start_y]
        comp["target"] = pygame.Rect(WIDTH - 250, start_y, comp["surface"].get_width(), comp["surface"].get_height())
        comp["assembled"] = True
        start_y += comp["surface"].get_height() + vertical_gap

    # Game state
    dragging, current_order = None, len(components)

    def draw_scene():
        screen.blit(background, (0, 0))
        for comp in components:
            if comp["assembled"]:
                screen.blit(comp["surface"], comp["pos"])
                screen.blit(font.render(comp["name"], True, RED), (comp["pos"][0], comp["pos"][1] - 25))
                pygame.draw.rect(screen, GRAY, comp["target"], 2)
                if comp["order"] == current_order:
                    pygame.draw.rect(screen, GREEN, comp["target"], 2)

    def reset_component_position(comp):
        comp["pos"] = [100, 100 + components.index(comp) * (comp["surface"].get_height() + vertical_gap)]

    # Main game loop
    running = True
    while running:
        screen.fill(BLACK)
    
        draw_scene()

        if all(not c["assembled"] for c in components):
            return
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for comp in components:
                    if pygame.Rect(comp["pos"], comp["surface"].get_size()).collidepoint(event.pos) and comp["assembled"]:
                        dragging = comp
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                if dragging["target"].collidepoint(event.pos) and dragging["order"] == current_order:
                    dragging["pos"] = dragging["target"].topleft
                    dragging["assembled"] = False
                    current_order -= 1
                else:
                    reset_component_position(dragging)
                dragging = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                dragging["pos"][0] += event.rel[0]
                dragging["pos"][1] += event.rel[1]

        pygame.display.flip()

 