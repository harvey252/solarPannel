# Example file showing a circle moving on screen
import pygame
import cleaningMinigame
import tempControlMinigame

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    

    game = tempControlMinigame.tempControl()
    
    while game.run(clock):
        game.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    
    game = cleaningMinigame.cleaningGame()
    
    while game.run(clock):
        game.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()



def draw():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)
    

main()


