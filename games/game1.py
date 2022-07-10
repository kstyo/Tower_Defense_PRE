import pygame
from pygame.locals import *
import os
import sys
from enemies.enemy1 import Enemy1
from enemies.enemy2 import Enemy2
from enemies.enemy3 import Enemy3
from towers.tower1 import Tower1
from towers.tower2 import Tower2
from towers.tower3 import Tower3
from menus.in_game_menu import BuyMenu, PlayButton
import time
import random

pygame.init()
lifes_image = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols", "heart-icon2.png")), (40,40))
gems_image = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols", "gemas.png")), (40,40))
background_menu = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols", "wood_menu.png")), (150, 250))
buy_tower1 = pygame.transform.scale(pygame.image.load(os.path.join("towers/1/shoot_002.png")), (70, 70))
buy_tower2 = pygame.transform.scale(pygame.image.load(os.path.join("towers/2/fire_002.png")), (70, 70))
buy_tower3 = pygame.transform.scale(pygame.image.load(os.path.join("towers/3/stone_002.png")), (70, 70))
play_button = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols/play.png")), (70, 70))
pause_button = pygame.transform.scale(pygame.image.load(os.path.join("buttons_symbols/pause.png")), (70, 70))
towers_names = ["Tower1", "Tower2", "Tower3"]
# las oleadas de enemigos se definen por numero de enemigos
waves = [[25, 0, 0], [50, 0, 0], [75, 50, 0], [100, 75, 50], [200, 100, 150]]

class Juego:
    def __init__(self):
        self.width = 1200
        self.height = 650
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemies = []
        self.towers = []
        self.lifes = 50
        self.gems = 800
        self.background = pygame.image.load(os.path.join("maps/mapa1.jpg"))
        self.menu = BuyMenu(1050, 0, background_menu)
        self.menu.add_buttons_towers(buy_tower1, "buy_tower1", 500)
        self.menu.add_buttons_towers(buy_tower2, "buy_tower2", 600)
        self.menu.add_buttons_towers(buy_tower3, "buy_tower3", 800)
        self.timer = time.time()
        self.text = pygame.font.Font("freesansbold.ttf", 32)
        self.selected_tower = None
        self.move_tower = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.play_button = PlayButton(play_button, pause_button, 10, 575)

    def generate_waves(self):
        """
        genera las oleadas de enemigos
        :return: enemy
        """
        if sum(self.current_wave) == 0:

            if len(self.enemies) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.PlayButton.paused = self.pause
        else:
            wave_enemies = [Enemy1(), Enemy2(), Enemy3()]
            for e in range(len(self.current_wave)):
                if self.current_wave[e] != 0:
                    self.enemies.append(wave_enemies[e])
                    self.current_wave[e] = self.current_wave[e] - 1
                    break
    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            if self.pause == False:
            # oleadas de enemigos
                if time.time() - self.timer >= random.randrange(1,5)/2:
                    self.timer = time.time()
                    self.generate_waves()

            pos = pygame.mouse.get_pos()

            # mover torres
            if self.move_tower:
                self.move_tower.move(pos[0], pos[1])

            # main
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # escoger y mover torres
                    if self.move_tower:
                        if self.move_tower.name in towers_names:
                            self.towers.append(self.move_tower)
                        self.move_tower.moving = False
                        self.move_tower = None
                    else: 
                        #mirar si esta en play o pausa
                        if self.play_button.click(pos[0], pos[1]):
                            self.pause = not(self.pause)
                            self.play_button.paused = self.pause

                        # mirar si se compra una torre
                        button_buy = self.menu.selected(pos[0], pos[1])
                        if button_buy:
                            cost_tower = self.menu.get_tower_cost(button_buy)
                            if self.gems >= cost_tower:
                                self.gems -= cost_tower
                                self.add_towers(button_buy)

                        # mirar si se clica una torre
                        button_clicked = None
                        if self.selected_tower:
                            button_clicked = self.selected_tower.menu.selected(pos[0], pos[1])
                            if button_clicked:
                                if button_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.gems >= cost:
                                        self.gems -= cost
                                        self.selected_tower.upgrade()
                        if not(button_clicked):
                            for tower in self.towers:
                                if tower.click(pos[0], pos[1]):
                                    tower.selected = True
                                    self.selected_tower = tower
                                else:
                                    tower.selected = False
            if not(self.pause):
                #terminar loop y eliminar enemigos y vidas
                to_del = []
                for enemy in self.enemies:
                    enemy.move()
                    if enemy.y < -15:
                        to_del.append(enemy)
                for d in to_del:
                    self.lifes -= 1
                    self.enemies.remove(d)

                #terminar loop torres
                for tower in self.towers:
                    self.gems += tower.attack(self.enemies)

                #si se pierde
                if self.lifes <= 0:
                    print("GAME OVER")
                    run = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.background, (0,0))
        #for p in self.clicks:
         #   pygame.draw.circle(self.win, (255,0,0), (p[0], p[1]), 5, 0) #se puede borrar era para crear camino enemigos

       #dibujar torres
        for tower in self.towers:
            tower.draw(self.win)

        #dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.win)

        #dibujar vidas
        life = lifes_image
        self.win.blit(life, (20, 10))
        value_life = self.text.render(str(self.lifes), 1, (255,255,255))
        self.win.blit(value_life, (65,18))

        #dibujar gemas
        gems = gems_image
        self.win.blit(gems, (120, 10))
        value_gems = self.text.render(str(self.gems), 1, (255, 255, 255))
        self.win.blit(value_gems, (170, 18))

        #dibujar torre moviendose
        if self.move_tower:
            self.move_tower.draw(self.win)

        #dibujar menu
        self.menu.draw(self.win)

        # dibujar boton jugar
        self.play_button.draw(self.win)

        pygame.display.update()

    def add_towers(self, name):
        x,y = pygame.mouse.get_pos()
        list_names = ["buy_tower1", "buy_tower2", "buy_tower3"]
        list_towers = [Tower1(x,y), Tower2(x,y), Tower3(x,y)]

        try:
            twr = list_towers[list_names.index(name)]
            self.move_tower = twr
            twr.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID")


#j = Juego()
#j.run()
