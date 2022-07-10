import pygame
import os
pygame.font.init()

gem = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols/gemas.png")), (25, 25))

class Button:
    """
    Botones para los menus de subir nivel
    """
    def __init__(self, menu, image, name):
        self.image = image
        self.name = name
        self.x = menu.x + 10
        self.y = menu.y + 5
        self.menu = menu
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def click(self, X, Y):
        """
        devuelve si se selecciona la torre del menu o no
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
            return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def update(self):
        self.x = self.menu.x + 10
        self.y = self.menu.y + 5

class BuyButton(Button):
    """
    Botones para menu de compra
    """
    def __init__(self,x,y, image, name, cost):
        self.image = image
        self.name = name
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.cost = cost

class PlayButton(Button):
    def __init__(self, play_image, pause_image, x, y):
        self.play = play_image
        self.pause = pause_image
        self.x = x
        self.y = y
        self.width = self.play.get_width()
        self.height = self.play.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))

class Menu:
    """
    Menu para seleccionar las torres
    """
    def __init__(self, tower, x, y, image, tower_cost):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.towers = 0
        self.buttons = []
        self.background = image
        self.upgrade = 0
        self.image_upgrade = image
        self.towers_cost = tower_cost
        self.upgrade_cost = []
        self.text_cost = pygame.font.SysFont("freesansbold", 22)
        self.object = tower

    def get_object_cost(self):
        """
        da el coste de subir de nivel la torre
        :return:
        """
        return self.towers_cost[self.object.level - 1]

    def draw(self, win):
        """
        crea el menu y botones
        :param win: surface
        :return: None
        """
        win.blit(self.background, (self.x, self.y))
        for i in self.buttons:
            i.draw(win)
            win.blit(gem, (i.x + i.width + 15, i.y + 5))
            text = self.text_cost.render(str(self.towers_cost[self.object.level - 1]), 1, (255, 255, 255))
            win.blit(text, (i.x + i.width + 8, i.y + gem.get_height() + 5))


    def add_buttons_upgrade(self, image_up, name):
        """
        añadir los botones de las torres
        :param image_up: surface
        :param name: str
        :return: None
        """
        self.upgrade += 1
        self.buttons.append(Button(self, image_up, name))

    def selected(self, X, Y):
        """
        devuelve el elemento seleccionado
        :param X: int
        :param Y: int
        :return: str
        """
        for button in self.buttons:
            if button.click(X,Y):
                return button.name
        return None

    def update(self):
        """
        carga el menu de las torres que se colocan
        :return: None
        """
        for button in self.buttons:
           button.update()

class BuyMenu(Menu):
    """
    Menu para comprar torres
    """
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.towers = 0
        self.buttons = []
        self.background = image
        self.upgrade = 0
        self.image_upgrade = image
        self.upgrade_cost = []
        self.text_cost = pygame.font.SysFont("freesansbold", 22)

    def add_buttons_towers(self, image, name, cost):
        """
        añadir los botones de las torres
        :param image: surface
        :param name: str
        :return: None
        """
        self.towers += 1
        button_y = self.y + 10 + (self.towers-1)*80
        button_x = self.x + 20
        self.buttons.append(BuyButton(button_x, button_y, image, name, cost))

    def get_tower_cost(self, name):
        """
        da el precio de la torre
        :param name: str
        :return: int
        """
        for button in self.buttons:
            if button.name == name:
                return button.cost
        return -1

    def draw(self, win):
        """
        crea el menu y botones
        :param win: surface
        :return: None
        """
        win.blit(self.background, (self.x, self.y))
        for i in self.buttons:
            i.draw(win)
            win.blit(gem, (i.x + i.width + 15, i.y + 12))
            text = self.text_cost.render(str(i.cost), 1, (255, 255, 255))
            win.blit(text, (i.x + i.width + 8, i.y + gem.get_height() + 15))
