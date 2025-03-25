import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Panel Disassembly")

# Colors
WHITE, GREEN, RED, GRAY, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (200, 200, 200), (0, 0, 0)

# Font
font = pygame.font.SysFont('Arial', 24)

# Load images
background = pygame.transform.scale(pygame.image.load("images/background.png"), (WIDTH, HEIGHT))
info_slide_image = pygame.transform.scale(pygame.image.load("images/infopage.png"), (WIDTH, HEIGHT))
panel_image = pygame.transform.scale(pygame.image.load("images/panel.png"), (WIDTH, HEIGHT))  # Solar panel image

# Function to add border to an image
def add_border(image, border_size=5):
    bordered_surface = pygame.Surface((image.get_width() + 2 * border_size, image.get_height() + 2 * border_size), pygame.SRCALPHA)
    bordered_surface.fill(WHITE)
    bordered_surface.blit(image, (border_size, border_size))
    return bordered_surface

# Scale and load components
scale_factor = WIDTH * 0.15 / pygame.image.load("images/frame.png").get_width()
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
vertical_gap = max(20, (max_height - total_height) // (len(components) - 1))
start_y = 100

# Assign positions
for i, comp in enumerate(components):
    comp["pos"] = [100, start_y]
    comp["target"] = pygame.Rect(WIDTH - 250, start_y, comp["surface"].get_width(), comp["surface"].get_height())
    comp["assembled"] = True
    start_y += comp["surface"].get_height() + vertical_gap

# Game state
dragging, current_order, game_started, info_slide_shown, panel_shown, start_page_shown = None, len(components), False, False, False, False

def draw_start_screen():
    screen.blit(background, (0, 0))
    title = font.render("Solar Panel Disassembly", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    start_button = pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100))
    screen.blit(font.render("Press SPACE to Start", True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    return start_button

def draw_information_slide():
    screen.blit(info_slide_image, (0, 0))
    note_text = font.render("Press the space bar to continue to the game.", True, WHITE)
    screen.blit(note_text, (WIDTH // 2 - note_text.get_width() // 2, HEIGHT - 50))

def draw_panel_image():
    screen.blit(panel_image, (0, 0))
    instruction_text = font.render("Press SPACE to start the game.", True, WHITE)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

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
    
    if not game_started:
        if not start_page_shown:
            # Show the start page first
            start_button = draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                    start_page_shown = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    start_page_shown = True
        elif not info_slide_shown:
            # Show the info page after the start page
            draw_information_slide()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    info_slide_shown = True
        elif not panel_shown:
            # Show the solar panel image after the info slide
            draw_panel_image()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    panel_shown = True
        else:
            # Once everything is shown, start the game
            game_started = True
    else:
        draw_scene()
        if all(not c["assembled"] for c in components) and not well_done_message_shown:
            well_done_message_shown = True
            screen.blit(font.render("Well Done!", True, GREEN), (WIDTH // 2 - 80, 150))
        
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

pygame.quit()
sys.exit()
