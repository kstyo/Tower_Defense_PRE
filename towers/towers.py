import pygame
import os
import math
from menus.in_game_menu import Menu

upgrade_menu = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols/upgrade_menu.png")), (125, 60))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols/upgrade_btn.png")), (50, 50))


class Towers():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0,0,0]
        self.price = [0,0,0]
        self.level = 1
        self.max_level = 3
        self.selected = False
        self.menu = Menu(self, self.x - 63, self.y + 45, upgrade_menu, [1000, 3000, "MAX"])
        self.menu.add_buttons_upgrade(upgrade_button, "Upgrade")
        self.image = None
        self.images = []
        self.animation_count = 0
        self.inRange = False
        self.range = 0
        self.damage = 0
        self.moving = False


    def click(self,x,y):
        """
        devuelve si la torre se clica y se selecciona
        :param x: int
        :param y: int
        :return: bool
        """
        if x - 50 <= self.x + self.width and x >= self.x:
            if y - 50 <= self.y + self.height and y >= self.y:
                return True
        return False

    def range(self, r):
        """
        cambia el rango de disparo de la torre
        :param r: int
        :return: None
        """
        self.range = r

    def draw(self, win):
        if self.inRange and not self.moving:
            self.animation_count += 1
            if self.animation_count >= len(self.images) * 5:
                self.animation_count = 0
        else:
            self.animation_count = 0

        tower = self.images[self.animation_count // 5]
        win.blit(tower, (self.x - 50, self.y - 50))

        #dibujar menu
        if self.selected:
            self.menu.draw(win)

        # dibuja el rango de la torre cuando se esta colocando en el mapa o se clica
        if self.selected:
            sf = pygame.Surface((self.range*4, self.range*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(sf, (255, 0, 0, 100), (self.range, self.range), self.range, 0)
            win.blit(sf, (self.x-self.range, self.y-self.range))


    def attack(self, enemies):
        """
        ataca el enemigo de la lista de enemigos
        :param enemies: lista de enemigos
        :return: None
        """
        gems = 0
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            distance = math.sqrt((self.x-x)**2 + (self.y-y)**2)
            if distance < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            first_en = enemy_closest[0]
            if self.animation_count == 25:
                if first_en.hit(self.damage) == True:
                    gems = first_en.gems
                    enemies.remove(first_en)
        return gems

    def sell(self):
        """
        vender la torre, devuelve el precio
        :return: int
        """
        return self.sell_price[self.level - 1]

    def upgrade(self):
        """
        subir de nivel la torre
        :return: None
        """
        if self.level < self.max_level:
            self.level += 1
            self.damage += 1
            self.range += 50

    def get_upgrade_cost(self):
        """
        devuelve el precio de subir de nivek, 0 si no se puede subir más de nivel
        :return: int
        """
        return self.menu.get_object_cost()

    def move(self, x, y):
        """
        mueve las torres
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()
