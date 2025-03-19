
#window cleaning example

#https://www.shutterstock.com/image-photo/front-view-solar-panel-isolated-on-1960798867 


from cgitb import grey
import pygame
import random



class tempControl:

    def __init__(self):
        self.background = pygame.image.load("heatingBackground.jpg").convert()
        
        self.background=pygame.transform.scale(self.background,(1280,720))
        #setting inital values
        self.temp=0
        self.upperTemp=4
        self.lowerTemp=2
        self.setTime=0;

        #creating rectangles for meter
        self.needle=pygame.Rect((605,0),(75,2))
        self.bar=pygame.Rect((605,0),(75,720))
        self.indicator= pygame.Rect((605,144),(75,144))

        #generating font
        self.titlefont=pygame.font.SysFont('comicsans',  50)



    #draw funciton draws what ever is happening to the screen
    def draw(self,screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        screen.blit(self.background, (0,0))

        renderTemp=round(3-self.setTime,1)
        #rending font
        letter2=self.titlefont.render(str(renderTemp), False, (0,0,0), (255,255,255))
        screen.blit(letter2, (827,230))
        
        #drawing meter
        pygame.draw.rect(screen,(255,0,0),self.bar)
        pygame.draw.rect(screen,(0,255,0),self.indicator)
        pygame.draw.rect(screen,(0,0,0),self.needle)

    
        #used to display to screen
        pygame.display.flip()
        
        


    #run function contains the game loop returns true on mini game being over 0 if it is ongoing
    def run(self,clock):
        #getting time passed
        dt = clock.tick(60) / 1000
        

        #adjusting temperature on if space pressed
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_SPACE]):
            #increasing temp
            self.temp-= dt*10
            if(self.temp>10):
                 self.temp=10;
        else:
            #lowing temp
            self.temp+=dt*2
            if(self.temp<0):
                self.temp=0;

        #setting nedel pos relative to temperature
        self.needle.y=self.temp*72
        
        #chekcing if the range for temperture calls inside of optimal region, if so updates the timper
        if((self.temp>self.lowerTemp) & (self.temp<self.upperTemp)):
            self.setTime+=dt
        else:
            self.setTime=0


        #end mini game if the meter has been inside correct region for long enough
        if( self.setTime>3):
            return False
        else:
            return True

