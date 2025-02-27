
#window cleaning example



import pygame

spongPos = pygame.Vector2(0,0)
imp=pygame.image

def init():
    print("init")
    spongPos = pygame.Vector2(0,0)
    
    #print(imp.get_width())
    



#draw funciton draws what ever is happening to the screen
def draw(screen):
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    imp = pygame.image.load("sponge.png").convert()
    imp = pygame.transform.scale(imp, (100, 100))
    
    screen.blit(imp, spongPos)
    
    #used to display to screen
    pygame.display.flip()


#run function contains the game loop returns true on mini game being over 0 if it is ongoing
def run(clock):


    #geting keys pressed
    
    
    spongPos.x = pygame.mouse.get_pos()[0]-50;
    spongPos.y = pygame.mouse.get_pos()[1]-50;
  
    

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
        


    return True;

