# Example file showing a circle moving on screen
import pygame
import cleaningMinigame
import tempControlMinigame

import recycleMinigame

from powerTheCityMinigame import powerTheCityGame

import disassemably

import building

#funciton to render a slide and then move on when space is pressed
def slide(slideName,screen):
    #loading in image for slide
    slideImage = spongeImage = pygame.image.load(slideName).convert()
    slideImage=pygame.transform.scale(slideImage,(1280,720))
    
    

    #drawing image
    
    screen.blit(slideImage,(0,0))
    
    pygame.display.flip()
    
   
        
    #ending slide when space is pressed
    running = True
    
    #for the game to update space must not have been space in the prevous frame (this allows two slides in a row)
    spaceNotPressedLastFrame=False;
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #letting the rest of the game know the window has been closed
                return False;
    
        #checking if space was pressed and seeing if it was not pressed last frame
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if(spaceNotPressedLastFrame):
                return True;
        else:
            spaceNotPressedLastFrame=True
    
    return

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    

    #all slides and mini games must check for running before they start
    
    
    
    #first two slides
    if(running):
        running = slide("images/startSlide.png",screen)
    if(running):
        running = slide("images/processingSilconeSlide.png",screen)
    
    

    #temp control minigame
    if(running):
        game = tempControlMinigame.tempControl()
    
        while game.run(clock) and running:
            game.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    

    #assembey slide
    if(running):
        running = slide("images/componentsSlides.png",screen)
    #assembly game
    if(running):
        building.run(screen)
                    
    #power the city slide
    if(running):
        running = slide("images/powerTheCitySlide.png",screen)
    #power the city game
    if(running):
        game = powerTheCityGame()
        while game.run(clock):
            game.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False

    #solar panel cleaning slide
    if(running):
        running = slide("images/cleaningSolarpannels.png",screen)
    
    #solar panel cleaning minigame
    if(running):
        game = cleaningMinigame.cleaningGame()
    
        while game.run(clock) and running:
            game.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


    #dissassembly slide
    if(running):
        running = slide("images/dissasemblySlide.png",screen)
    #disassembly game
    if(running):                
        disassemably.run(screen)

    #recycling slide
    if(running):
        running = slide("images/recyclingSlide.png",screen)
    #recycling game
    if(running):                
        recycleMinigame.run(screen)
    

    #recycling silcon slide
    if(running):
        running = slide("images/recyclingSilconeSlide.png",screen)


    #final slide 
    if(running):
        running = slide("images/finalSlide.png",screen)    
    
    
    pygame.quit()

    



main()


