import pygame
from pygame.locals import *
import sys
import lib/textlib.py


pygame.init()
screen=pygame.display.set_mode((500,500),HWSURFACE|DOUBLEBUF|RESIZABLE)
pic=pygame.image.load("a.png") #You need an example picture in the same folder as this file!
screen.blit(pygame.transform.scale(pic,(500,500)),(0,0))
#pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type==QUIT: 
            pygame.quit()
            sys.exit(0)      
        elif event.type==VIDEORESIZE:
            screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
            pygame.display.update()
            
        if event.type == KEYDOWN:
            if event.key == K_q:
                print("aa")

