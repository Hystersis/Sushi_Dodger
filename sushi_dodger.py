# Sushi Dodger
# Created by Hystersis W, 2020
# Screen size = 256*256
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


pygame.init()

def initi():
    global flag, screen_width, screen, ddger_group, sshi_group, lvel, ddger
    flag = True
    # Game Screen
    screen_width = 256
    screen = pygame.display.set_mode((screen_width,screen_width))
    pygame.display.set_caption("Sushi Dodger")
    pygame.mouse.set_visible(False)
    # Level and dodger initilization
    lvel = Level()
    ddger = dodger("dodger_1.png")
    ddger_group = pygame.sprite.Group()
    ddger_group.add(ddger)
    # sushi setup code
    sshi_group = pygame.sprite.Group()
    for a in range(10):
        sshi = sushi([random.randrange(256),random.randrange(256)])
        sshi_group.add(sshi)


class Level:
    lev = 1
    def __init__(self):
        lev_num = self.lev
    def get_num(self, num_sshi = 0):
        if num_sshi >= 40:
            num_sshi = 40
        else:
            num_sshi = self.lev * 2 + 14
        return int(num_sshi)
    def get_lev(self):
        return int(self.lev)
    def next_lev(self, is_endless = False):
        if self.lev < 5 or is_endless:
            self.lev += 1
            next_Lvl()





class dodger(pygame.sprite.Sprite):
    pos = [128,16]
    dirnx = 0
    dirny = 0
    def __init__(self, picture_path):
        super().__init__()
        # Sprite
        self.image = pygame.image.load(picture_path)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    print('Going left',self.dirnx,self.dirny)
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    print('Going right',self.dirnx,self.dirny)
                else:
                    self.dirnx = 0

                if keys[pygame.K_UP]:
                    self.dirny = -1
                    print('Going up',self.dirnx,self.dirny)
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    print('Going down',self.dirnx,self.dirny)
                else:
                    self.dirny = 0

        self.dirny += 0.025
        if 0 < self.pos[0] and self.dirnx <= 0:
            self.pos[0] += self.dirnx
        elif 240 > self.pos[0] and self.dirnx >= 0:
            self.pos[0] += self.dirnx
        if 0 < self.pos[1] and self.dirny <= 0:
            self.pos[1] += self.dirny
        if 240 > self.pos[1] and self.dirny >= 0:
            self.pos[1] += self.dirny
        # update self.position
        self.rect.topleft = self.pos
    def where_am_i(self):
        poses = []
        poses.append(self.pos[0])
        poses.append(self.pos[1])
        return poses



class sushi(pygame.sprite.Sprite):
    def __init__(self, sop):
        super().__init__()
        self.sop = [0,0]
        self.sop[0] = sop[0]
        self.sop[1] = sop[1]
        self.dirny = self.dirnx = 0
        print(self.sop)
        self.rt = pygame.image.load('sushi_template.png')
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = self.directory + str(self.ran) + '.png'
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.sop
    def update(self,d_x,d_y):
        if self.sop[0] < d_x and self.sop[0] <= 0:
            self.dirnx = random.randrange(2) - random.uniform(0.6,1.2)
        elif self.sop[0] > d_x and self.sop[0] >= 240:
            self.dirnx = random.randrange(2) - random.uniform(0.8,1.4)
        if self.sop[1] < d_y and self.sop[1] <= 0:
            self.dirny = random.randrange(2) - random.uniform(0.6,1.2)
        elif self.sop[1] > d_y and self.sop[1] >= 240:
            self.dirny = random.randrange(2) - random.uniform(0.8,1.4)
        self.sop[0] += self.dirnx
        self.sop[1] += self.dirny
        self.rect.topleft = self.sop




def next_Lvl():
    global ddger, ddger_group, sshi_group
    sshi_group.clear()
    sshi_group = pygame.sprite.Group()
    lvel.next_lev()
    for sushi in range(lvel.get_num()):
        sshi = sushi((random.randrange(256),random.randrange(256)))
        sshi_group.add(sshi)



def main():
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(60)
        clock.tick(60)
        pygame.display.flip()
        screen.fill((0,0,0))
        sshi_group.draw(screen)
        ddger_group.draw(screen)
        ddger_group.update()
        pstn = ddger.where_am_i()
        sshi_group.update(pstn[0],pstn[1])
initi()
main()
