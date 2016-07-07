import pygame
from pygame import *


grad = Surface((100, 100))
cur_col = 0
for i in range(100):
    for j in range(100):
        grad.set_at((i, j), (cur_col, cur_col, cur_col))
    cur_col += 1

image.save(grad, "grad.png")