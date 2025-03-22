
#window cleaning example

#https://www.shutterstock.com/image-photo/front-view-solar-panel-isolated-on-1960798867 


import pygame
import random



class cleaningGame:

    def __init__(self):
        print("init")
        self.spongPos = pygame.Vector2(0,0)
        self.spongeImage = pygame.image.load("sponge.png").convert()
        self.spongeImage = pygame.transform.scale(self.spongeImage, (100, 100))
        
        self.plannelImage = pygame.image.load("solarPannelImage.png").convert()
        
        self.plannelImage=pygame.transform.scale(self.plannelImage,(500,720))

        self.dirtImage = pygame.image.load("dirt.png").convert()
        self.dirtImage=pygame.transform.scale(self.dirtImage,(5,5))

        self.dirt=[]
        for i in range(5000):
            self.dirt.append(pygame.Vector2(random.randint(0,495),random.randint(0,715)))
    
    
        self.spongeSize=40



    #draw funciton draws what ever is happening to the screen
    def draw(self,screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(self.plannelImage, (0,0))
    
        for i in range(len(self.dirt)):
            screen.blit(self.dirtImage, self.dirt[i])

        screen.blit(self.spongeImage, self.spongPos)
    
        #used to display to screen
        pygame.display.flip()
        
        


    #run function contains the game loop returns true on mini game being over 0 if it is ongoing
    def run(self,clock):


        #geting keys pressed
    
        mousePos=pygame.mouse.get_pos();
        self.spongPos.x = mousePos[0]-50;
        self.spongPos.y = mousePos[1]-50;
        
        tempDirt=[]
        
        for i in range(len(self.dirt)):
           if(not ((mousePos[0]-self.spongeSize<self.dirt[i].x) & (mousePos[0]+self.spongeSize>self.dirt[i].x) & 
              (mousePos[1]-self.spongeSize<self.dirt[i].y) & (mousePos[1]+self.spongeSize>self.dirt[i].y))):
                tempDirt.append(self.dirt[i])
        
        self.dirt = tempDirt
        

    

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        
        if(len(self.dirt)<5):
            return False
        else:
            return True

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 720))
    clock = pygame.time.Clock()

    game = cleaningGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        running = game.run(clock)
        game.draw(screen)

    pygame.quit()

