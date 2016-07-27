import pygame
import sys
import configparser
import json
import socket
from socket import *
import time as time_
from pygame import *
from random import randint
from client_files import reswind



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

def loadField(path):
    floor_field = []
    walls_field = []
    ceil_field = []
    fin = open('client_files/levels/' + path)
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

def exchangeData(send_data):
    conn = socket(AF_INET, SOCK_STREAM)
    try:
        conn.connect(addr)   
    except ConnectionRefusedError:
        print("Connection refused")
        return
    conn.send(send_data.encode("utf-8"))
    recv_data = conn.recv(2 ** 25).decode("utf-8")
    conn.close()      
    return recv_data
    

#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('client_files/config.ini')

WIND_W_INIT = int(config['DISPLAY SIZE']['WIND_W_INIT'])
WIND_H_INIT = int(config['DISPLAY SIZE']['WIND_H_INIT'])

MAIN_W = int(config['DISPLAY SIZE']['MAIN_W'])
MAIN_H = int(config['DISPLAY SIZE']['MAIN_H'])

cells = {}
for key in config.options('CELL TEXTURES'):
    cells[key] = json.loads(config['CELL TEXTURES'][key])
    cells[key]['img'] = image.load('client_files/' + cells[key]['texture'])
#-----#
host = '192.168.1.59'#input("Server IP: ")
port = 25567#int(input("Server prot: "))
addr = (host, port)

field_surface = Surface((MAIN_W, MAIN_H))
recv_data = exchangeData('["get_field", null]')
if not recv_data: sys.exit("Couldnt connect to the server")
print(recv_data + "/n")
field = json.loads(recv_data)

pygame.init()
window = reswind.ResizableWindow((WIND_W_INIT, WIND_H_INIT),
                                 (MAIN_W, MAIN_H),
                                 gap_fill_type="gradient_up",
                                 smoothscale=False)

CELLS_W, CELLS_H = len(field[0][0]), len(field[0])

entities_surface = Surface((MAIN_W, MAIN_H))
entities_surface.fill((0, 0, 0))
entities_surface.set_colorkey((0, 0, 0))


ping = [time_.time(), time_.time()]
clock = pygame.time.Clock()
GAME_ON = True
while GAME_ON:
    clock.tick(30)
    e = pygame.event.poll()
    if e.type == QUIT: 
        GAME_ON = False   
    if e.type == VIDEORESIZE:
        window.updateSize(e.dict['size']) 
        
    entities_surface.fill((0, 0, 0))  
    
    recv_data = exchangeData('["get_field", null]')
    if not recv_data: break
    try:
        field = json.loads(recv_data)
    except Exception as e:
        print(e)
        print(recv_data)
        break
    
    drawField(field_surface, field)
    field_surface.blit(entities_surface, (0, 0))
    window.updateMainSurface(field_surface)
    window.update()
        
pygame.quit()