import pygame
import sys
import configparser
import json
import entities
from pygame import *
from random import randint
from lib import reswind


class MousePos:
    def __init__(self):
        self.prev = window.getMousePos()
        self.curr = window.getMousePos()
    
    def update(self):
        self.prev = self.curr
        self.curr = window.getMousePos()
        self.both = [self.prev[0], self.prev[1], self.curr[0], self.curr[1]]

class MouseButtons:
    def __init__(self):
        self.prev = mouse.get_pressed()
        self.curr = mouse.get_pressed()   
        self.both, self.pressed, self.released = None, None, None
    
    def update(self):
        self.prev = self.curr
        self.curr = mouse.get_pressed() 
        self.both = [self.prev[i] or self.curr[i] for i in range(3)]
        self.pressed = [1 if not self.prev[i] and self.curr[i] else 0 
                        for i in range(3)]
        self.released = [1 if self.prev[i] and not self.curr[i] else 0 
                         for i in range(3)]          

class KeyboardButtons:
    def __init__(self):
        self.prev = pygame.key.get_pressed()
        self.curr = pygame.key.get_pressed()        
        self.both, self.pressed, self.released = None, None, None
    
    def update(self):
        self.prev = self.curr
        self.curr = pygame.key.get_pressed()
        self.both = [self.prev[i] or self.curr[i] 
                     for i in range(len(self.prev))]
        self.pressed = [1 if not self.prev[i] and self.curr[i] else 0 
                        for i in range(len(self.prev))]
        self.released = [1 if self.prev[i] and not self.curr[i] else 0 
                         for i in range(len(self.prev))]

# This functions convert coordinates from field-type to pixel-type and back 
#    EXAMPLE: (2, 1) -> (32, 16)
def toPixel(coords):
    return [coord * 16 for coord in coords]

def toField(coords):
    return [int(coord // 16) for coord in coords]
#

def drawField(surface, field):
    for i in range(CELLS_H):
        for j in range(CELLS_W):
            x, y = toPixel((j, i))
            drawCell(surface, field[0][i][j], (x, y))   
            drawCell(surface, field[1][i][j], (x, y))   
            drawCell(surface, field[2][i][j], (x, y))   

def saveField(field, path):
    fout = open('levels/' + path, 'w')
    for layer in field:
        for line in layer:
            fout.write(''.join(line) + '\n')
    fout.close()

def loadField(path):
    floor_field = []
    walls_field = []
    ceil_field = []
    fin = open('levels/' + path)
    for i, line in enumerate(fin.readlines()):
        if i < CELLS_H:
            floor_field.append(list(line.strip())) 
        elif i < 2 * CELLS_H:
            walls_field.append(list(line.strip())) 
        else:
            ceil_field.append(list(line.strip())) 
    fin.close()
    return [floor_field, walls_field, ceil_field]

def drawCell(surface, cell_type, coord):
    if cell_type == "n": return
    if cell_type not in cells.keys(): cell_type = "v"
    surface.blit(cells[cell_type]['img'], coord)


#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('config.ini')

WIND_W_INIT = int(config['DISPLAY SIZE']['WIND_W_INIT'])
WIND_H_INIT = int(config['DISPLAY SIZE']['WIND_H_INIT'])

MAIN_W = int(config['DISPLAY SIZE']['MAIN_W'])
MAIN_H = int(config['DISPLAY SIZE']['MAIN_H'])

CELLS_W = int(config['DISPLAY SIZE']['CELLS_W'])
CELLS_H = int(config['DISPLAY SIZE']['CELLS_H'])

cells = {}
for key in config.options('CELL TEXTURES'):
    cells[key] = json.loads(config['CELL TEXTURES'][key])
    cells[key]['img'] = image.load(cells[key]['texture'])
#-----#

pygame.init()
window = reswind.ResizableWindow((WIND_W_INIT, WIND_H_INIT),
                                 (MAIN_W, MAIN_H),
                                 gap_fill_type="gradient_up",
                                 smoothscale=False)

field_surface = Surface((MAIN_W, MAIN_H))
field = loadField('test_level.txt')

mouse_pos = MousePos()
mouse_buttons = MouseButtons()
keyboard_buttons = KeyboardButtons()


entities_surface = Surface((MAIN_W, MAIN_H))
entities_surface.fill((0, 0, 0))
entities_surface.set_colorkey((0, 0, 0))

player1 = entities.Tank()

clock = pygame.time.Clock()
GAME_ON = True
while GAME_ON:
    clock.tick(30)
    e = pygame.event.poll()
    if e.type == QUIT: 
        a = (image.tostring(field_surface, "RGB"))
        GAME_ON = False   
    if e.type == VIDEORESIZE:
        window.updateSize(e.dict['size']) 
        
    entities_surface.fill((0, 0, 0))   
    player1.draw(entities_surface)
    player1.move()
    
    drawField(field_surface, field)
    field_surface.blit(entities_surface, (0, 0))
    window.updateMainSurface(field_surface)
    window.update()
        
pygame.quit()