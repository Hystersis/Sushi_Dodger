# Sushi Dodger
# Created by Marcus W, 2020
# Screen size = 256*256
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


pygame.init()
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
global sshi_group
sshi_group = pygame.sprite.Group()
for sus in range(11):
    sshi = sushi((random.randrange(256),random.randrange(256)))
    sshi_group.add(sshi)


class Level():
    lev = 1
    def __init__(self):
        lev_num = Level.lev
    def get_num(self, num_sshi = 0):
        if num_sshi >= 40:
            num_sshi = 40
        else:
            num_sshi = Level.lev * 2 + 14
        return int(num_sshi)
    def get_lev(self):
        return int(Level.lev)
    def next_lev(self, is_endless = False):
        if Level.lev < 5 or is_endless:
            Level.lev += 1
            next_Lvl()





class dodger(pygame.sprite.Sprite):
    def __init__(self,picture_path):
        global pos, dirnx, dirny
        super().__init__()
        # Sprite
        pos = [128,16]
        dirnx = 0
        dirny = 0
        self.image = pygame.image.load(picture_path)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        global pos, dirnx, dirny
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    dirnx = -1
                    print('Going left',dirnx,dirny)
                elif keys[pygame.K_RIGHT]:
                    dirnx = 1
                    print('Going right',dirnx,dirny)
                else:
                    dirnx = 0

                if keys[pygame.K_UP]:
                    dirny = -1
                    print('Going up',dirnx,dirny)
                elif keys[pygame.K_DOWN]:
                    dirny = 1
                    print('Going down',dirnx,dirny)
                else:
                    dirny = 0

        dirny += 0.025
        if 0 < pos[0] and dirnx <= 0:
            pos[0] += dirnx
        elif 240 > pos[0] and dirnx >= 0:
            pos[0] += dirnx
        if 0 < pos[1] and dirny <= 0:
            pos[1] += dirny
        if 240 > pos[1] and dirny >= 0:
            pos[1] += dirny
        # update position
        self.rect.topleft = pos



class sushi(pygame.sprite.Sprite):
    def __init__(self, sop):
        super().__init__()
        self.rt = pygame.image.load('sushi_template.png')
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = self.directory + str(self.ran) + '.png'
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0,0))
        self.rect = self.image.get_rect()
        self.rect = sop



def next_Lvl():
    global ddger, ddger_group, sshi_group
    sshi_group.clear()
    sshi_group = pygame.sprite.Group()
    for sushi in range(level.get_num()):
        sshi = sushi((random.randrange(256),random.randrange(256)))
        sshi_group.add(sshi)


def main():
    clock = pygame.time.Clock()
    while flag:
        global ddger_group, sshi_group
        pygame.time.delay(300)
        clock.tick(60)
        pygame.display.flip()
        screen.fill((0,0,0))
        sshi_group.draw(screen)
        ddger_group.draw(screen)
        ddger_group.update()
main()
