import pygame
import os
from .towers import Towers

images = []

for im in range(8):
    add_str = "0" + str(im)
    images.append(
        pygame.transform.scale(pygame.image.load(os.path.join("towers/3", "stone_0" + add_str + ".png")),
                               (100, 100)))

class Tower3(Towers):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.images = images[:]
        self.range = 150
        self.damage = 3
        self.name = "Tower3"



