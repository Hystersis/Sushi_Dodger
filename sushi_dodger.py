# Sushi Dodger
# Created by Hystersis W, 2020
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
    def __init__(self):
        super().__init__()
        self.rt = pygame.image.load('sushi_template.png')
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = self.directory + str(self.ran) + '.png'
        self.center = pygame.image.load(str(self.directory))
        self.center = pygame.Surface.convert_alpha(self.center)
        self.image = self.rt.copy()
        self.th = self.image.copy()
        self.image.blit(self.center, (0,0))
        self.ut = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect = [70,80]
    def update(self):
        #debugging
        global screen
        screen.blit(self.rt, (0,0))
        screen.blit(self.center, (16,0))
        screen.blit(self.image, (32,0))
        screen.blit(self.th, (48,0))
        screen.blit(self.ut, (64,0))





ddger = dodger("dodger_1.png")
ddger_group = pygame.sprite.Group()
ddger_group.add(ddger)
sshi = sushi()
sshi_group = pygame.sprite.Group()
sshi_group.add(sshi)


def main():
    clock = pygame.time.Clock()
    while flag:
        global ddger_group, sshi_group
        pygame.time.delay(300)
        clock.tick(60)
        sshi_group.update()
        pygame.display.flip()
        screen.fill((0,0,0))
        sshi_group.draw(screen)
        ddger_group.draw(screen)
        ddger_group.update()
main()
