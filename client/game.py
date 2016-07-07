import pygame
from pygame import *
import sys
import configparser


def updateDisplaySurface():
    global display_surface
    (disp_w, disp_h) = display_surface.get_size()    
    
    # If this condition is true, the field width will be sized 
    # to the display width, and the gaps between the field and
    # the window will be above and below the field.
    #
    # If it is not, the field will be sized to the display 
    # height, and the gaps will appear on the both sides 
    # of the display.
    if disp_h / (disp_w / 16) >= 9:
        size = (disp_w, round(disp_w / 16 * 9))
        coords = (0, round((disp_h - size[1]) / 2))
    else:
        size = (round(disp_h / 9 * 16), disp_h)
        coords = (round((disp_w - size[0]) / 2), 0) 
    
    display_surface.blit(background_surface, (0, 0))   
    display_surface.blit(transform.scale(field_surface, size), coords)

def newBackground():
    new_background = Surface(display_surface.get_size())
    (disp_w, disp_h) = display_surface.get_size() 
    
    # We need to add a gradient into the gaps, in order to 
    # make them look more pretty.
    grad = image.load("img/gui/grad.png")
    if disp_h / (disp_w / 16) >= 9:  # If the gaps are above and below the field
        grad_size = (disp_w, round((disp_h - disp_w / 16 * 9) / 2))
        grad_top = transform.scale(transform.rotate(grad, 90), grad_size)
        grad_bottom = transform.scale(transform.rotate(grad, -90), grad_size)
        
        new_background.blit(grad_top, (0, 0))
        new_background.blit(grad_bottom, (0, disp_h - grad_size[1]))
        
        # -1 here - sort of a duct tape. It works, and idk why :P
        draw.line(new_background, (100, 100, 100),
                  (0, grad_size[1] - 1), (disp_w, grad_size[1] - 1), 6)
        draw.line(new_background, (100, 100, 100),
                          (0, disp_h - grad_size[1] - 1), 
                          (disp_w, disp_h - grad_size[1] - 1), 6) 
    else:  # And if they are on the sides
        grad_size = (round((disp_w - disp_h / 9 * 16) / 2), disp_h)
        grad_left = transform.scale(transform.rotate(grad, 180), grad_size)
        grad_right = transform.scale(grad, grad_size)
        
        new_background.blit(grad_left, (0, 0))
        new_background.blit(grad_right, (disp_w - grad_size[0], 0))
        
        # -1 here - just the same duct tape.
        draw.line(new_background, (100, 100, 100),
                  (grad_size[0] - 1, 0), (grad_size[0] - 1, disp_h), 6)
        draw.line(new_background, (100, 100, 100),
                  (disp_w - grad_size[0] - 1, 0), 
                  (disp_w - grad_size[0] - 1, disp_h), 6)
    
    return new_background
        
    


#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('config.ini')

WIND_W_INIT = int(config['DISPLAY SIZE']['WIND_W_INIT'])
WIND_H_INIT = int(config['DISPLAY SIZE']['WIND_H_INIT'])

FIELD_W = int(config['DISPLAY SIZE']['FIELD_W'])
FIELD_H = int(config['DISPLAY SIZE']['FIELD_H'])

CELLS_W = int(config['DISPLAY SIZE']['CELLS_W'])
CELLS_H = int(config['DISPLAY SIZE']['CELLS_H'])
#-----#

pygame.init()
screen = display.set_mode((WIND_W_INIT, WIND_H_INIT),
                                 HWSURFACE|DOUBLEBUF|RESIZABLE)
display_surface    = Surface((WIND_W_INIT, WIND_H_INIT))
background_surface = Surface((WIND_W_INIT, WIND_H_INIT))
field_surface      = Surface((FIELD_W, FIELD_H))



pic = pygame.image.load("a.png")
field_surface.blit(transform.scale(pic, (FIELD_W, FIELD_H)), (0, 0))
#pygame.display.flip()
while True:
    for e in pygame.event.get():
        if e.type == QUIT: 
            pygame.quit()
            sys.exit(0)      
        elif e.type == VIDEORESIZE:
            screen = display.set_mode(e.dict['size'],
                                             HWSURFACE|DOUBLEBUF|RESIZABLE)
            display_surface = transform.scale(display_surface, e.dict['size'])
            background_surface = newBackground()
            
        if e.type == KEYDOWN:
            if e.key == K_q:
                print("aa")
                
        
        
        updateDisplaySurface()
        screen.blit(transform.scale(display_surface,
                                    (screen.get_width(), screen.get_height())),
                                    (0, 0))
        pygame.display.update()
