import pygame
import cleaningMinigame
import tempControlMinigame
from powerTheCityMinigame import powerTheCityGame

def show_menu(screen):
    pygame.font.init()
    font = pygame.font.SysFont("arial", 32)
    title_font = pygame.font.SysFont("arial", 36, bold=True)

    # Menu text
    title_text = "Hey, we think it's pretty cool that you want to learn about solar panels!"
    subtitle_text = "We'll make it fun for you :)"
    subtitle2_text = "Choose which game you want to play."

    options = [
        "Clean the Panel",
        "Temperature Control",
        "Power the City",
        "Quit Game"
    ]

    # Pre-render text
    title = title_font.render(title_text, True, (255, 255, 255))
    subtitle = font.render(subtitle_text, True, (255, 255, 255))
    subtitle2 = font.render(subtitle2_text, True, (255, 255, 255))
    rendered_options = [font.render(opt, True, (255, 255, 0)) for opt in options]

    # Create clickable rects
    option_rects = []
    spacing = 50
    start_y = 300

    for i, opt in enumerate(rendered_options):
        rect = opt.get_rect(center=(640, start_y + i * spacing))
        option_rects.append(rect)

    while True:
        screen.fill((0, 0, 50))
        screen.blit(title, title.get_rect(center=(640, 80)))
        screen.blit(subtitle, subtitle.get_rect(center=(640, 130)))
        screen.blit(subtitle2, subtitle2.get_rect(center=(640, 170)))

        for i, opt in enumerate(rendered_options):
            screen.blit(opt, option_rects[i])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "clean"
                elif event.key == pygame.K_2:
                    return "temp"
                elif event.key == pygame.K_3:
                    return "city"
                elif event.key == pygame.K_4:
                    return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        return ["clean", "temp", "city", "quit"][i]



def main():
    print("Main function started")  # debug print

    # Pygame setup
    pygame.init()
    pygame.display.set_caption("Solar Minigames")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    while True:
        print("Showing menu...")  # debug print
        selected = show_menu(screen)

        if selected == "quit" or selected is None:
            break

        elif selected == "temp":
            game = tempControlMinigame.tempControl()
            while game.run(clock):
                game.draw(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

        elif selected == "clean":
            game = cleaningMinigame.cleaningGame()
            while game.run(clock):
                game.draw(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

        elif selected == "city":
            print("Launching Power the City")
            try:
                game = powerTheCityGame()
                screen = pygame.display.set_mode((game.window_width, game.window_height))
                while game.run(clock):
                    game.draw(screen)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                screen = pygame.display.set_mode((1280, 720))
            except Exception as e:
                print("Error running Power the City:", e)

    pygame.quit()


if __name__ == "__main__":
    main()


#def draw():
    # fill the screen with a color to wipe away anything from last frame
   # screen.fill("purple")
    #pygame.draw.circle(screen, "red", player_pos, 40)

#main()
