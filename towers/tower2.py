import pygame
import os
from .towers import Towers

images = []

for im in range(7):
    add_str = "0" + str(im)
    images.append(
        pygame.transform.scale(pygame.image.load(os.path.join("towers/2", "fire_0" + add_str + ".png")),
                               (100, 100)))

class Tower2(Towers):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.images = images[:]
        self.range = 200
        self.damage = 2
        self.name = "Tower2"



