import pygame
import sys
import configparser
from pygame import *
from random import randint
from lib import reswind


def drawField(surface, field):
    for i, line in enumerate(field):
        for j, cell in enumerate(line):
            x, y = toPixel(j, i)
            drawCell(surface, cell, x, y)

def drawCell(surface, cell_type, x, y):
    if cell_type not in cell_textures.keys(): cell_type = "v"
    cell_img = image.load(cell_textures[cell_type])
    surface.blit(cell_img, (x, y))
    
# This functions convert coordinates from field-type to pixel-type and back 
#    EXAMPLE: (2, 1) -> (32, 16)
def toPixel(x, y):
    return (x * 16, y * 16)

def toField(x, y):
    return (x // 16, y // 16)
    


#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('config.ini')

WIND_W_INIT = int(config['DISPLAY SIZE']['WIND_W_INIT'])
WIND_H_INIT = int(config['DISPLAY SIZE']['WIND_H_INIT'])

MAIN_W = int(config['DISPLAY SIZE']['MAIN_W'])
MAIN_H = int(config['DISPLAY SIZE']['MAIN_H'])

CELLS_W = int(config['DISPLAY SIZE']['CELLS_W'])
CELLS_H = int(config['DISPLAY SIZE']['CELLS_H'])

cell_textures = {}
for key in config.options('CELL TEXTURES'):
    cell_textures[key] = config['CELL TEXTURES'][key]
#-----#

pygame.init()
window = reswind.ResizableWindow((WIND_W_INIT, WIND_H_INIT),
                                 (MAIN_W, MAIN_H),
                                 gap_fill_type="gradient_up",
                                 smoothscale=False)

field_surface = Surface((MAIN_W, MAIN_H))
field = [['v' for x in range(CELLS_W)] for y in range(CELLS_H)]


clock = pygame.time.Clock()
while True:
    clock.tick(30)
    e = pygame.event.wait()
    if e.type == QUIT: 
        pygame.quit()
        sys.exit(0)      
    if e.type == VIDEORESIZE:
        window.updateSize(e.dict['size']) 
    
    if e.type == KEYDOWN:
        if e.key == K_u:
            drawField(field_surface, field)
        
    
    
    window.updateMainSurface(field_surface)
    window.update()
        
    
            
        
        
