import pygame
import os
from .enemies import Enemies

images = []

for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    images.append(pygame.transform.scale(
        pygame.image.load(os.path.join("enemies/2", "9_enemies_1_run_0" + add_str + ".png")), (64, 64)))

class Enemy2(Enemies):
    def __init__(self):
        super().__init__()
        self.gems = 10
        self.images = images[:]
        self.max_health = 5
        self.health = self.max_health

