import pygame
import math
import os

class Enemies():
    def __init__(self):
        self.width = 64
        self.height = 64
        self.velocity = 1
        self.health = 0
        self.max_health = 0
        self.init_path = 0
        self.path = [(-10, 188), (4, 188), (290, 193), (336, 217), (355, 272), (359, 332), (359, 564), (443, 574), (554, 577), (668, 578), (958, 568), (990, 506), (964, 454), (895, 436), (711, 425), (679, 362), (670, 293), (669, 3), (669, -10)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.move_count = 0
        self.animation_count = 0
        self.image = None
        self.distance = 0
        self.move_distance = 0
        self.flipped = False
        self.images = []

    def draw(self, win):
        """
        Dibuja enemigo
        :param win: surface
        :return: None
        """
        self.image = self.images[self.animation_count]

        win.blit(self.image, (self.x - 30, self.y - 55))
        self.health_bar(win)

    def health_bar(self, win):
        """
        Dibuja la barra de salud del enemigo
        :param win: surface
        :return: None
        """
        length = 50
        move = round(length / self.max_health)
        health_bar = move * self.health

        pygame.draw.rect(win, (255,0,0), (self.x - 30, self.y - 60, length, 10), 0)
        pygame.draw.rect(win, (0,255,0), (self.x - 30, self.y - 60, health_bar, 10), 0)

    def collide(self, x, y):
        """
        Devuelve si el enemigo choca
        :param x: int
        :param y: int
        :return: Bool
        """
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def move(self):
        """
        Mover los enemigos
        :return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.images):
            self.animation_count = 0


        x1,y1 = self.path[self.init_path]
        if self.init_path +1 >= len(self.path):
            x2, y2 = (-10, 3)
        else:
            x2, y2 = self.path[self.init_path+1]

        dif = (x2-x1, y2-y1)
        length = math.sqrt((dif[0])**2 + (dif[1])**2)
        dif = (dif[0]/length, dif[1]/length)

        if dif[0] < 0 and not (self.flipped):
            self.flipped = True
            for x, img in enumerate(self.images):
                self.images[x] = pygame.transform.flip(img, True, False)


        x_move, y_move = (self.x + dif[0], self.y + dif[1])

        self.x = x_move
        self.y = y_move

        #Ir al siguiente punto
        if dif[0] >= 0: # a la derecha
            if dif[1] >= 0: #a bajo
                if self.x >= x2 and self.y >= y2:
                    self.init_path += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.init_path += 1
        else:
            if dif[1] >= 0:  # a bajo
                if self.x <= x2 and self.y >= y2:
                    self.init_path += 1
            else:
                if self.x <= x2 and self.y <= y2:
                    self.init_path += 1

                if self.x >= x2 and self.y == y2:
                    self.distance = 0
                    self.init_path += 1

    def hit(self, damage):
        """
        Resta una vida al enemigo y devuelve si muere
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False

