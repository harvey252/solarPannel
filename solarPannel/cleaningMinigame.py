
#window cleaning example

#https://www.shutterstock.com/image-photo/front-view-solar-panel-isolated-on-1960798867 


import pygame
import random



class cleaningGame:

    def __init__(self):
     

        #this reciton loads in images
        self.spongPos = pygame.Vector2(0,0)
        self.spongeImage = pygame.image.load("sponge.png").convert_alpha()#convert_alpha required for transparrent images
        self.spongeImage = pygame.transform.scale(self.spongeImage, (100, 100))
       


        self.plannelImage = pygame.image.load("solarPannelImage.png").convert()
        
        self.plannelImage=pygame.transform.scale(self.plannelImage,(500,720))

        self.dirtImage = pygame.image.load("dirt.png").convert_alpha()
        self.dirtImage=pygame.transform.scale(self.dirtImage,(5,5))


        #generating dirt
        self.dirt=[]
        for i in range(5000):
            self.dirt.append(pygame.Vector2(random.randint(0,495),random.randint(0,715)))
    
    
        self.spongeSize=40



    #draw funciton draws what ever is happening to the screen
    def draw(self,screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        #drawing in the solar pannel
        screen.blit(self.plannelImage, (0,0))
    
        #drawing in each dirt
        for i in range(len(self.dirt)):
            screen.blit(self.dirtImage, self.dirt[i])

        #drawing in the sponge
        screen.blit(self.spongeImage, self.spongPos)
    
        #used to display to screen
        pygame.display.flip()
        
        


    #run function contains the game loop returns true on mini game being over 0 if it is ongoing
    def run(self,clock):


        #geting mouse pos
        mousePos=pygame.mouse.get_pos();
        
        #setting spong pos
        self.spongPos.x = mousePos[0]-50;
        self.spongPos.y = mousePos[1]-50;
        
        #finding dirt near enough to the spong to be removed
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
        
        #if dirt is almost gone will end the minigame
        if(len(self.dirt)<5):
            return False
        else:
            return True

