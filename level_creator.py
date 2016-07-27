import pygame
import sys
import configparser
import json
from pygame import *
from random import randint
from client_files import reswind


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
        x0, y0, x1, y1 = toField(coords)
        x0 = min(max(x0, 0), CELLS_W - 1)
        y0 = min(max(y0, 0), CELLS_H - 1)
        x1 = min(max(x1, 0), CELLS_W - 1)
        y1 = min(max(y1, 0), CELLS_H - 1)
        x0, y0, x1, y1 = toPixel([x0, y0, x1, y1])
        if x0 == x1 and y0 == y1: 
            if field: 
                tx, ty = toField([x0, y0])
                field[current_layer - 1][ty][tx] = cell_type
            if surface: drawCell(surface, cell_type, toPixel(toField((x0, y0))))
        cx, cy = x0, y0
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        while abs(cx - x1) > 1 or abs(cy - y1) > 1:
            if field: 
                tx, ty = toField([cx, cy])
                field[current_layer - 1][ty][tx] = cell_type
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
    for i in range(CELLS_H):
        for j in range(CELLS_W):
            x, y = toPixel((j, i))
            if current_layer >= 1: drawCell(surface, field[0][i][j], (x, y))   
            if current_layer >= 2: drawCell(surface, field[1][i][j], (x, y))   
            if current_layer >= 3: drawCell(surface, field[2][i][j], (x, y))   

def saveField(field, path):
    fout = open('server_files/levels/' + path, 'w')
    for layer in field:
        for line in layer:
            fout.write(''.join(line) + '\n')
    fout.close()

def loadField(path):
    floor_field = []
    walls_field = []
    ceil_field = []
    fin = open('server_files/levels/' + path)
    for i, line in enumerate(fin.readlines()):
        if i < CELLS_H:
            floor_field.append(list(line.strip())) 
        elif i < 2 * CELLS_H:
            walls_field.append(list(line.strip())) 
        else:
            ceil_field.append(list(line.strip())) 
    fin.close()
    return [floor_field, walls_field, ceil_field]

def drawCell(surface, cell_type, coords):
    if cell_type == "n": return
    if cell_type not in cells.keys(): cell_type = "v"
    x, y = toField(coords)
    x = min(max(x, 0), CELLS_W - 1)
    y = min(max(y, 0), CELLS_H - 1)
    coords = toPixel((x, y))
    surface.blit(cells[cell_type]['img'], coords)
    
def drawCursor():
    cursor_surface.fill((0, 0, 0))
    cx, cy = toField(window.getMousePos())
    cx = min(max(cx, 0), CELLS_W)
    cy = min(max(cy, 0), CELLS_H)
    cx, cy = toPixel((cx, cy))
    draw.rect(cursor_surface, (255, 0, 0), (cx - 1, cy - 1, 17, 17), 6)
    drawCell(cursor_surface, cellFromIdx(current_cell), (cx, cy))

def cellFromIdx(idx):
    return sorted(list(cells.keys()))[idx]


#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('client_files/config.ini')

WIND_W_INIT = int(config['DISPLAY SIZE']['WIND_W_INIT'])
WIND_H_INIT = int(config['DISPLAY SIZE']['WIND_H_INIT'])

MAIN_W = int(config['DISPLAY SIZE']['MAIN_W'])
MAIN_H = int(config['DISPLAY SIZE']['MAIN_H'])

CELLS_W = int(config['DISPLAY SIZE']['CELLS_W'])
CELLS_H = int(config['DISPLAY SIZE']['CELLS_H'])

cells = {}
for key in config.options('CELL TEXTURES'):
    cells[key] = json.loads(config['CELL TEXTURES'][key])
    cells[key]['img'] = image.load('client_files/' + cells[key]['texture'])
#-----#

pygame.init()
window = reswind.ResizableWindow((WIND_W_INIT, WIND_H_INIT),
                                 (MAIN_W, MAIN_H),
                                 gap_fill_type="gradient_up",
                                 smoothscale=False)

field_surface = Surface((MAIN_W, MAIN_H))

cursor_surface = Surface((MAIN_W, MAIN_H))
cursor_surface.fill((0, 0, 0))
cursor_surface.set_colorkey((0, 0, 0))
cursor_surface.set_alpha(150)
p_surface = Surface((MAIN_W, MAIN_H))
p_surface.fill((0, 0, 0))
p_surface.set_colorkey((0, 0, 0))
p_surface.set_alpha(150)

load_path = "blank.txt"
save_path = "new_level.txt"
i = 0
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg in ("-l", "--load-path"):
        i += 1
        load_path = sys.argv[i]
    if arg in ("-s", "--save-path"):
        i += 1
        save_path = sys.argv[i]
    i += 1
field = loadField(load_path)


current_cell = 0
current_layer = 1
mouse_pos = MousePos()
mouse_buttons = MouseButtons()
keyboard_buttons = KeyboardButtons()
x0, y0 = (0, 0)

clock = pygame.time.Clock()
GAME_ON = True
while GAME_ON:
    clock.tick(30)
    e = pygame.event.poll()
    if e.type == QUIT: 
        GAME_ON = False   
    if e.type == VIDEORESIZE:
        window.updateSize(e.dict['size']) 
    mouse_pos.update()
    mouse_buttons.update()
    keyboard_buttons.update()
    
    if keyboard_buttons.pressed[K_1]: current_layer = 1
    if keyboard_buttons.pressed[K_2]: current_layer = 2
    if keyboard_buttons.pressed[K_3]: current_layer = 3
    
    if mouse_buttons.pressed[1]:
        current_cell = (current_cell + 1) % len(cells.keys())
    
    if mouse_buttons.curr[0] and not (keyboard_buttons.both[K_LSHIFT] or
                                      keyboard_buttons.both[K_LCTRL]):
        Draw.line(cellFromIdx(current_cell), mouse_pos.both, field=field)
        
    if keyboard_buttons.curr[K_LSHIFT] and mouse_buttons.curr[0]:
        if not x0: x0, y0 = mouse_pos.curr
        x1, y1 = mouse_pos.curr
        p_surface.fill((0, 0, 0))
        Draw.line(cellFromIdx(current_cell), (x0, y0, x1, y1), p_surface)
    if keyboard_buttons.curr[K_LSHIFT] and mouse_buttons.released[0]:
        x1, y1 = mouse_pos.curr
        Draw.line(cellFromIdx(current_cell), (x0, y0, x1, y1), field=field)
        x0, y0 = (0, 0)
        p_surface.fill((0, 0, 0))
    
    if keyboard_buttons.curr[K_LCTRL] and mouse_buttons.curr[0]:
        if not x0: x0, y0 = mouse_pos.curr
        x1, y1 = mouse_pos.curr
        p_surface.fill((0, 0, 0))
        Draw.rect(cellFromIdx(current_cell), (x0, y0, x1, y1), p_surface)
    if keyboard_buttons.curr[K_LCTRL] and mouse_buttons.released[0]:
        x1, y1 = mouse_pos.curr
        Draw.rect(cellFromIdx(current_cell), (x0, y0, x1, y1), field=field)
        x0, y0 = (0, 0)
        p_surface.fill((0, 0, 0))    
    
    if keyboard_buttons.curr[K_LCTRL] and keyboard_buttons.curr[K_s]:
        saveField(field, save_path)
        
    
    drawField(field_surface, field)
    drawCursor()
    cursor_surface.blit(p_surface, (0, 0))
    window.updateMainSurface(field_surface)
    window.main_surface.blit(cursor_surface, (0, 0))
    window.update()
    display.update()


pygame.quit()