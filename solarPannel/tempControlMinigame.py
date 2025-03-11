
#window cleaning example

#https://www.shutterstock.com/image-photo/front-view-solar-panel-isolated-on-1960798867 


from cgitb import grey
import pygame
import random



class tempControl:

    def __init__(self):

        self.temp=0
        self.upperTemp=3
        self.lowerTemp=1
    
    
        self.spongeSize=40
        self.setTime=0;

        self.needle=pygame.Rect((0,0),(20,2))
        self.bar=pygame.Rect((0,0),(20,720))
        self.indicator= pygame.Rect((0,144),(20,144))



    #draw funciton draws what ever is happening to the screen
    def draw(self,screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        
        

        pygame.draw.rect(screen,(255,0,0),self.bar)
        pygame.draw.rect(screen,(0,255,0),self.indicator)
        pygame.draw.rect(screen,(0,0,0),self.needle)

    
        #used to display to screen
        pygame.display.flip()
        
        


    #run function contains the game loop returns true on mini game being over 0 if it is ongoing
    def run(self,clock):

        dt = clock.tick(60) / 1000
        

        #adjusting temperature
        keys=pygame.key.get_pressed()
        if (True):
            if(keys[pygame.K_SPACE]):
                
                self.temp+= dt*3
                if(self.temp>100):
                    self.temp=100;
         
            else:
                self.temp-=dt*2
                if(self.temp<0):
                    self.temp=0;

        self.needle.y=self.temp*72
        

        if((self.temp>self.lowerTemp) & (self.temp<self.upperTemp)):
            self.setTime+=dt
            print("set")
        else:
            self.setTime=0

        print(self.temp)
        print(self.setTime)

        if( self.setTime>2):
            return False
        else:
            return True

