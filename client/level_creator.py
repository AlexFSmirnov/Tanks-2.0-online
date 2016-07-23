import pygame
import sys
import configparser
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

class Draw:    
    def line(cell_type, coords, surface=None, field=None):
        x0, y0, x1, y1 = coords
        x0 = min(x0, MAIN_W - 1)
        y0 = min(y0, MAIN_H - 1)
        x1 = min(x1, MAIN_W - 1)
        y1 = min(y1, MAIN_H - 1)        
        if x0 == x1 and y0 == y1: 
            if field: field[toField([y0])[0]][toField([x0])[0]] = cell_type
            if surface: drawCell(surface, cell_type, toPixel(toField((x0, y0))))
        cx, cy = x0, y0
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        while abs(cx - x1) > 1 or abs(cy - y1) > 1:
            if field: field[toField([cy])[0]][toField([cx])[0]] = cell_type
            if surface: drawCell(surface, cell_type, toPixel(toField((cx, cy))))
            cx += (x1 - x0) / max(dx, dy)
            cy += (y1 - y0) / max(dx, dy)
    
    def rect(cell_type, coords, surface=None, field=None):
        x0, y0, x1, y1 = coords
        Draw.line(cell_type, (x0, y0, x1, y0), surface=surface, field=field)
        Draw.line(cell_type, (x1, y0, x1, y1), surface=surface, field=field)
        Draw.line(cell_type, (x1, y1, x0, y1), surface=surface, field=field)
        Draw.line(cell_type, (x0, y1, x0, y0), surface=surface, field=field)
        


# This functions convert coordinates from field-type to pixel-type and back 
#    EXAMPLE: (2, 1) -> (32, 16)
def toPixel(coords):
    return [coord * 16 for coord in coords]

def toField(coords):
    return [int(coord // 16) for coord in coords]
#

def drawField(surface, field):
    for i, line in enumerate(field):
        for j, cell in enumerate(line):
            x, y = toPixel((j, i))
            drawCell(surface, cell, (x, y))       

def drawCell(surface, cell_type, coord):
    if cell_type not in cell_textures.keys(): cell_type = "v"
    cell_img = cells[cell_type]
    surface.blit(cell_img, coord)
    
def drawCursor():
    cursor_surface.fill((0, 0, 0))
    cx, cy = toPixel(toField(window.getMousePos()))
    cx = min(max(cx, 0), MAIN_W - 17)
    cy = min(max(cy, 0), MAIN_H - 17)
    draw.rect(cursor_surface, (255, 0, 0), (cx - 1, cy - 1, 17, 17), 6)
    drawCell(cursor_surface, cell_types[current_cell], (cx, cy))


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
cell_types = []
cells = {}
for key in config.options('CELL TEXTURES'):
    cell_textures[key] = config['CELL TEXTURES'][key]
    cells[key] = image.load(cell_textures[key])
    cell_types.append(key)
#-----#

pygame.init()
window = reswind.ResizableWindow((WIND_W_INIT, WIND_H_INIT),
                                 (MAIN_W, MAIN_H),
                                 gap_fill_type="gradient_up",
                                 smoothscale=False)

field_surface = Surface((MAIN_W, MAIN_H))
field = [['v' for x in range(CELLS_W)] for y in range(CELLS_H)]

cursor_surface = Surface((MAIN_W, MAIN_H))
cursor_surface.fill((0, 0, 0))
cursor_surface.set_colorkey((0, 0, 0))

p_surface = Surface((MAIN_W, MAIN_H))
p_surface.fill((0, 0, 0))
p_surface.set_colorkey((0, 0, 0))


current_cell = 0
mouse_pos = MousePos()
mouse_buttons = MouseButtons()
keyboard_buttons = KeyboardButtons()
x0, y0 = (0, 0)

clock = pygame.time.Clock()
GAME_ON = True
while GAME_ON:
    clock.tick(30)
    e = pygame.event.wait()
    if e.type == QUIT: 
        GAME_ON = False   
    if e.type == VIDEORESIZE:
        window.updateSize(e.dict['size']) 
    mouse_pos.update()
    mouse_buttons.update()
    keyboard_buttons.update()
    
    if mouse_buttons.pressed[1]:
        current_cell = (current_cell + 1) % len(cell_types)
    
    if mouse_buttons.curr[0] and not (keyboard_buttons.both[K_LSHIFT],
                                      keyboard_buttons.both[K_LCTRL]):
        Draw.line(cell_types[current_cell], mouse_pos.both, field=field)
        
    if keyboard_buttons.curr[K_LSHIFT] and mouse_buttons.curr[0]:
        if not x0: x0, y0 = mouse_pos.curr
        x1, y1 = mouse_pos.curr
        p_surface.fill((0, 0, 0))
        Draw.line(cell_types[current_cell], (x0, y0, x1, y1), p_surface)
    if keyboard_buttons.curr[K_LSHIFT] and mouse_buttons.released[0]:
        x1, y1 = mouse_pos.curr
        Draw.line(cell_types[current_cell], (x0, y0, x1, y1), field=field)
        x0, y0 = (0, 0)
        p_surface.fill((0, 0, 0))
    
    if keyboard_buttons.curr[K_LCTRL] and mouse_buttons.curr[0]:
        if not x0: x0, y0 = mouse_pos.curr
        x1, y1 = mouse_pos.curr
        p_surface.fill((0, 0, 0))
        Draw.rect(cell_types[current_cell], (x0, y0, x1, y1), p_surface)
    if keyboard_buttons.curr[K_LCTRL] and mouse_buttons.released[0]:
        x1, y1 = mouse_pos.curr
        Draw.rect(cell_types[current_cell], (x0, y0, x1, y1), field=field)
        x0, y0 = (0, 0)
        p_surface.fill((0, 0, 0))    
        
    
    drawField(field_surface, field)
    drawCursor()
    cursor_surface.blit(p_surface, (0, 0))
    window.updateMainSurface(field_surface)
    window.main_surface.blit(cursor_surface, (0, 0))
    window.update()
    display.update()


pygame.quit()