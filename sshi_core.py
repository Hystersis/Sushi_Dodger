# Sushi Dodger
# Created by Hystersis W, 2020
# Screen size = 256*256
# import math

import random
import pygame
from pygame.freetype import *
from copy import deepcopy
import ctypes
import sshi_graphics as grph
# import numpy as np
import dis

#                     ,,
# `7MMF'              db   mm
#   MM                     MM
#   MM  `7MMpMMMb.  `7MM mmMMmm
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
# .JMML..JMML  JMML..JMML. `Mbmo




def initi():
    pygame.init()
    global gm, screen_width, screen, ddger_group, sshi_group, lvel, ddger, score, kill_map, offset
    # Game Screen
    screen_width = 256
    gm = 'Active'
    icon = pygame.image.load("dodger_icon.png")
    pygame.display.set_icon(icon)
    myappid = 'mycompany.myproduct.subproduct.version' # allows for taskbar icon to be changed
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # flags = pygame.SCALED add in pygame.display.setmode(screen,flags!)
    screen = pygame.display.set_mode((screen_width,screen_width),flags=pygame.RESIZABLE | pygame.SCALED) # add pygame.RESIZABLE to make it resize
    display_info = pygame.display.Info()
    print("display info:",dir(display_info))
    pygame.display.set_caption("Sushi Dodger")
    pygame.mouse.set_visible(False)
    score = 0
    # Level and dodger initilization
    lvel = Level()
    ddger = dodger("dodger_1.png")
    ddger_group = pygame.sprite.Group()
    ddger_group.add(ddger)
    pstn = ddger.where_am_i()
    # sushi setup code
    sshi_group = pygame.sprite.Group()
    offset = 0
    for a in range(10):
        sshi = sushi([random.randrange(240),random.randrange(240)],pstn) # Change [128,16] if starting pos of ddger is changed
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





#                               ,,
# `7MM"""Yb.                  `7MM
#   MM    `Yb.                  MM
#   MM     `Mb  ,pW"Wq.    ,M""bMM  .P"Ybmmm .gP"Ya `7Mb,od8
#   MM      MM 6W'   `Wb ,AP    MM :MI  I8  ,M'   Yb  MM' "'
#   MM     ,MP 8M     M8 8MI    MM  WmmmP"  8M""""""  MM
#   MM    ,dP' YA.   ,A9 `Mb    MM 8M       YM.    ,  MM
# .JMMmmmdP'    `Ybmd9'   `Wbmd"MML.YMMMMMb  `Mbmmd'.JMML.
#                                  6'     dP
#                                  Ybmmmd'


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
        self.dirncy = 0
    def update(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
            else:
                self.dirnx = 0

            if keys[pygame.K_UP]:
                self.dirny = -1
            elif keys[pygame.K_DOWN]:
                self.dirny = 1
            else:
                self.dirny = 0

        self.grav = (self.dirncy if self.dirny == 0 else 0) + 0.025 # This is the expoential gravity function
        self.dirncy = self.grav if self.dirncy < 2 else self.dirncy
        self.dirny += self.grav

        self.pos[0] += self.dirnx if 0 < (self.pos[0] + self.dirnx) < 239 else 0
        self.pos[1] += self.dirny if 0 < (self.pos[1] + self.dirny) < 239 else 0
        # if 0 < self.pos[0] and self.dirnx <= 0:
        #     self.pos[0] += self.dirnx
        # elif 239 > self.pos[0] and self.dirnx >= 0:
        #     self.pos[0] += self.dirnx
        # if 0 < self.pos[1] and self.dirny <= 0:
        #     self.pos[1] += self.dirny
        # if 239 > self.pos[1] and self.dirny >= 0:
        #     self.pos[1] += self.dirny
        # # update self.position
        self.rect.topleft = (int(self.pos[0]),int(self.pos[1]))
    def where_am_i(self):
        poses = []
        poses.append(round(self.pos[0]))
        poses.append(round(self.pos[1]))
        return poses

    def killed(self):
        global gm
        gm = 'Died'
        # print(ddger_group)
        self.kill()
        # print(ddger_group)
        print('You died!, press \'X\' to start again')



#                              ,,          ,,
#  .M"""bgd                  `7MM          db
# ,MI    "Y                    MM
# `MMb.   `7MM  `7MM  ,pP"Ybd  MMpMMMb.  `7MM
#   `YMMNq. MM    MM  8I   `"  MM    MM    MM
# .     `MM MM    MM  `YMMMa.  MM    MM    MM
# Mb     dM MM    MM  L.   I8  MM    MM    MM
# P"Ybmmd"  `Mbod"YML.M9mmmP'.JMML  JMML..JMML.





class sushi(pygame.sprite.Sprite):
    def __init__(self, sop,d_xy):
        super().__init__()
        self.relation_x = round(sop[0]) - round(d_xy[0])
        self.relation_y = round(sop[1]) - round(d_xy[1])
        self.sop = [poscheck(sop[0],d_xy[0]),poscheck(sop[1],d_xy[1])]
        self.dirny = self.dirnx = 0
        self.rt = pygame.image.load('sushi_template.png')
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = self.directory + str(self.ran) + '.png'
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0,0))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.sop
        print(self.rect.topleft)
    def update(self,d_xy):
        global score
        if len(ddger_group) > 0:
            self.d = [0,0]
            ran = lambda y : round(random.uniform(0.6,1.4),2)
            self.d[0] += (ran(1) if self.sop[0] <= d_xy[0] else -ran(1))
            self.d[1] += (ran(1) if self.sop[1] <= d_xy[1] else -ran(1))
            print("d:",self.d)
            # if self.sop[0] <= d_xy[0]:
            #     self.d[0] += random.uniform(0.6,1.4)
            # if self.sop[0] > d_xy[0]:
            #     self.d[0] -= random.uniform(0.6,1.4)
            # if self.sop[1] <= d_xy[1]:
            #     self.d[1] += random.uniform(0.6,1.4)
            # if self.sop[1] > d_xy[1]:
            #     self.d[1] -= random.uniform(0.6,1.4)
            # self.sop = list(deepcopy(self.rect.topleft))
            self.sop = tuple(map(lambda x,y:minmax(0,x+y,240),self.rect.topleft,self.d))
            # self.sop[0] = minmax(0,self.sop[0] + self.d[0],240)
            # self.sop[1] = minmax(0,self.sop[1] + self.d[1],240)
            print('Sop:',self.sop,'\t',tuple(self.sop),'\t',self.rect.topleft)
            self.check_hit = pygame.sprite.spritecollide(ddger,sshi_group,False)
            self.sop_copy = deepcopy(self.sop) # WHy iS tHis LinE heRe?
            if len(self.check_hit) >= 1:
                ddger.killed() if map(lambda sop,dxy:-16<(sop-dxy)<16,self.sop,d_xy) and (self.sop[1] - d_xy[1]) > 6 else self.kill()

                # self.relation_x = round(self.sop[0]) - round(d_xy[0])
                # self.relation_y = round(self.sop[1]) - round(d_xy[1])
                # if self.relation_y > -16 and self.relation_y < 16 and self.relation_x > -16 and self.relation_x < 16:
                #     if self.relation_y > 6:
                #         self.image = pygame.image.load('True_hit.png')
                #         ddger.killed()
                #     else:
                #         self.image = self.image_copy
                #         score += 1
                #         self.kill()
                # else:
                #     self.image = self.image_copy

                # self.rect = self.image.get_rect()
            self.rect.topleft = tuple(self.sop)


def next_Lvl():
    global ddger, ddger_group, sshi_group
    sshi_group.clear()
    sshi_group = pygame.sprite.Group()
    lvel.next_lev()
    for sushi in range(lvel.get_num()):
        sshi = sushi((random.randrange(256),random.randrange(256)))
        sshi_group.add(sshi)

# class background(pygame.sprite.Sprite):
#     def __init__(self):
#
#     def state(self):


#                            ,,
# `7MMM.     ,MMF'           db
#   MMMb    dPMM
#   M YM   ,M MM   ,6"Yb.  `7MM  `7MMpMMMb.
#   M  Mb  M' MM  8)   MM    MM    MM    MM
#   M  YM.P'  MM   ,pm9MM    MM    MM    MM
#   M  `YM'   MM  8M   MM    MM    MM    MM
# .JML. `'  .JMML.`Moo9^Yo..JMML..JMML  JMML.


def main():
    global ddger_group, sshi_group, gm
    clock = pygame.time.Clock()
    while len(gm) >= 0:
        # print('Gamemode:\t',gm)
        pygame.time.delay(100)
        clock.tick(60)
        act = pygame.key.get_focused()
        if act and gm != 'Died':
            # print('Active',act,'\t',gm)
            gm = 'Active'
        elif not act and gm != 'Died':
            gm = 'Paused'

        events()

        if pygame.key.get_pressed()[pygame.K_F5]:
                initi()

        if gm == 'Active':
            pstn = ddger.where_am_i()
            sshi_group.update(pstn)
            # print('Score:',score)
            fps = clock.get_fps()
            # print("FPS:", fps)

        if gm == 'Died':
            die_screen(ddger.where_am_i())

        if gm == 'Won':
            # Add win code for each level here
            pass

        pygame.display.flip()
        screen.fill((0,0,0))
        screen.blit(grph.screenLow(screen),[0,0])
        sshi_group.draw(screen)
        ddger_group.draw(screen)
        ddger_group.update()
        screen.blit(grph.screenHigh(screen,gm),[0,0])
        # nscreen = grph.scaling(screen)
        # print("Window size:",pygame.display.get_window_size())


#                   ,,
# `7MMM.     ,MMF'  db
#   MMMb    dPMM
#   M YM   ,M MM  `7MM  ,pP"Ybd  ,p6"bo
#   M  Mb  M' MM    MM  8I   `" 6M'  OO
#   M  YM.P'  MM    MM  `YMMMa. 8M
#   M  `YM'   MM    MM  L.   I8 YM.    ,
# .JML. `'  .JMML..JMML.M9mmmP'  YMbmd'


def minmax(a,b,c):
    return (lambda x: sorted(x)[1])([a,b,c])

def poscheck(proposed,noarea):
    proposed_table = []
    for e in range(20):
        f = max(proposed - e, 0)
        g = min(proposed + e, 255)
        proposed_table.append(f), proposed_table.append(g)
    for u in proposed_table:
        if u == noarea:
            proposed = poscheck(random.randrange(0,255),noarea)
            return proposed
            break
    else:
        return proposed

def die_screen(dxy):
    if pygame.key.get_pressed()[pygame.K_x]:
        pygame.time.delay(2000) #Change to incorporate the movement of the helment
        initi()

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.key.get_pressed()[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
            print(event)

def screen_shake(screen):
    # Fix this screen shake
    fade = 0.95
    offset_x, offset_y = random.randint(-16,16), random.randint(-16,16)
    offset_x *= offset
    offset_y *= offset
    screen.scroll(offset_x,offset_y)
    offset *= fade
    offset = 0 if offset <= 0.5 else offset

#                               ,,
# `7MM"""YMM                  `7MM
#   MM    `7                    MM
#   MM   d    `7MMpMMMb.   ,M""bMM
#   MMmmMM      MM    MM ,AP    MM
#   MM   Y  ,   MM    MM 8MI    MM
#   MM     ,M   MM    MM `Mb    MM
# .JMMmmmmMMM .JMML  JMML.`Wbmd"MML.



initi()
main()
