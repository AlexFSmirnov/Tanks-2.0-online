import pygame 
from pygame import *


class Tank:
    def __init__(self,
                 init_pos=[0, 0],
                 color="red"):
        self.pos = init_pos
        self.color = color
        self.angle = 0
        self.image = image.load("img/tanks/tank_{}.png".format(color))
        
    def draw(self, surface):
        im = transform.rotate(self.image, self.angle)
        surface.blit(im, self.pos)
    
    def move(self):
        keyboard_buttons = key.get_pressed()
        if keyboard_buttons[K_a]:
            self.angle = (self.angle + 10) % 360
        if keyboard_buttons[K_d]:
            self.angle = (self.angle - 10) % 360
        