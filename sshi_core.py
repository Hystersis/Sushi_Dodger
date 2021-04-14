# Sushi Dodger
# Created by Hystersis W, 2020 - 2021
# Screen size = 256*256

# All these modules
import pygame
# from pygame.freetype import * # Errors led to this line, having to be here
import ctypes
import math
import os
from itertools import repeat
import random
from operator import sub, add

# This importing the other modules into core
import sshi_graphics as grph
import sshi_msci as msci


#                     ,,
# `7MMF'              db   mm
#   MM                     MM
#   MM  `7MMpMMMb.  `7MM mmMMmm
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
# .JMML..JMML  JMML..JMML. `Mbmo
class Initi:
    screen = pygame.display.set_mode((256, 256), flags=pygame.RESIZABLE
                                     | pygame.SCALED)
    # This allows the screen to be bigger that it was

    def __init__(self, lvl=1):
        pygame.init()
        self.screen_width = 256
        self.gm = 'Active'
        self.icon = pygame.image.load(os.path.join("Assets",
                                                   "dodger_icon.png"))
        pygame.display.set_icon(self.icon)
        self.myappid = 'mycompany.myproduct.subproduct.version'
        # allows for taskbar icon to be changed
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                                                                self.myappid)
        pygame.display.set_caption("Sushi Dodger")
        pygame.mouse.set_visible(False)  # So the cursor isn't shown
        self.score = 0
        # Level and dodger initilization
        self.lvel = self.Level(lvl)
        self.ddger = Dodger(os.path.join("Assets", "dodger_1.png"))
        self.ddger_group = pygame.sprite.Group()
        self.ddger_group.add(self.ddger)
        self.offset = repeat((0, 0))
        # sushi setup code
        self.sshi_group = pygame.sprite.Group()
        for a in range(self.num):
            self.sshi = Sushi(self.ddger)
            # Change [128,16] if starting pos of ddger is changed
            self.sshi_group.add(self.sshi)

    def Level(self, lvl):
        self.lvl = lvl
        self.n = list(map(lambda y: y*2+12, range(2, 15)))
        self.n.insert(0, 10)

        def get_num():
            return self.n[self.lvl - 1 if self.lvl < 14 else 13]
        self.num = get_num()

    def __repr__(self):
        return 'Initialization object'







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


class Dodger(pygame.sprite.Sprite):
    pos = [128, 16]
    dirnx = 0
    dirny = 0

    def __init__(self, picture_path):
        super().__init__()
        # Sprite
        self.image = pygame.image.load(picture_path)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.dirncy = 0

    def update(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1.5
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1.5
            else:
                self.dirnx = 0

            if keys[pygame.K_UP]:
                self.dirny = -1.5
            elif keys[pygame.K_DOWN]:
                self.dirny = 1.5
            else:
                self.dirny = 0

        if i.gm == 'Active':
            self.grav = (self.dirncy if self.dirny == 0 else 0) + 0.025
            # This is the expoential gravity function
            self.dirncy = self.grav if self.dirncy < 2 else self.dirncy
            self.dirny += self.grav

        self.pos[0] += self.dirnx if 0 < (self.pos[0] + self.dirnx) < 239 else 0
        self.pos[1] += self.dirny if 0 < (self.pos[1] + self.dirny) < 239 else 0
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

    def where_am_i(self, area=False):
        if area:
            return [list(self.rect.topleft), list(self.rect.bottomright)]
        else:
            poses = []
            poses.append(round(self.pos[0]))
            poses.append(round(self.pos[1]))
            return poses

    def killed(self):
        i.gm = 'Died'
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


class Sushi(pygame.sprite.Sprite):
    def __init__(self, ddger):
        super().__init__()
        self.create_centre()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.poscheck(ddger)

    def update(self):
        self.delta = list(map(sub, i.ddger.where_am_i(), self.rect.topleft))
        # This maps each coordinate of ddger and sshi; ddger - shhi
        self.deltap = list(map(lambda z: z * random.uniform(0.8, 1.2) / abs(z)
                               if z != 0 else 0, self.delta))
        # This returns a -1, 0 or 1 (with a little bit of noise)
        # depending on the delta
        self.rect.topleft = tuple(map(minmax, [0, 0], map(add,
                                                          self.rect.topleft,
                                                          self.deltap),
                                      [255, 255]))
        # This adds the aforementioned -1, 0 or 1 to the current
        # coordinates of sshi
        self.checkhit()

    def poscheck(self, ddger):
        self.square = ddger.where_am_i(True)
        xH, xL = self.square[0][0] - 20, self.square[1][0] + 20
        yH, yL = self.square[0][1] - 20, self.square[1][1] + 20

        while True:
            x = random.randrange(0, 255)
            y = random.randrange(0, 255)
            if (x < xH or x > xL) and (y < yH or y > yL):
                # If the x,y coordinates are outside of ddger's AoE break
                # out of the loop
                break
            else:  # Else, reclaculate new x and y
                continue
        return (x, y)

    def killed(self):
        print('Killed!')
        i.score += 1
        self.kill()
        print('len:', len(i.sshi_group))
        if len(i.sshi_group) == 0:
            i.gm = 'Won'
            print('Won', i.gm)

    def create_centre(self):
        self.rt = pygame.image.load(os.path.join("Assets",
                                    'sushi_template.png'))
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = os.path.join("Assets", self.directory
                                      + str(self.ran) + '.png')
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0, 0))
        self.image_copy = self.image.copy()

    def checkhit(self):
        if len(list(filter(lambda a: -16 < a < 16, self.delta))) == 2:
            # This sees if sshi is in AoE of the ddger
            i.offset = shake()  # This shakes the screen
            i.ddger.killed() if self.delta[1] < 0 else self.killed()
            # This kills the ddger if it is bellow the sshi, and vice versa

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
    clock = pygame.time.Clock()
    global i
    print('I:', i)
    while True:
        print(i.gm) if i.gm == 'Won' else None
        move_screen = Initi.screen.copy()
        # print('Gamemode:\t',gm)
        pygame.time.delay(100)
        clock.tick(60)
        act = pygame.key.get_focused()
        if act and i.gm == 'Paused':
            i.gm = 'Active'
        elif not act and i.gm == 'Active':
            i.gm = 'Paused'

        events()

        if pygame.key.get_pressed()[pygame.K_F5]:
            i = Initi(i.lvl)

        if i.gm == 'Active':
            # print('Score:',score)
            i.sshi_group.update()

        if i.gm == 'Died':
            die_screen(i.ddger.where_am_i())

        if i.gm == 'Won':
            print('Won')
            i = Initi(i.lvl + 1)

        i.score = i.num - len(i.sshi_group)

        pygame.display.flip()
        move_screen.blit(pygame.image.load(os.path.join("Assets"
                                                        , 'background_res2.png'))
                         , [0, 0])
        move_screen.blit(GI.update('screenLow'), [0, 0])
        i.sshi_group.draw(move_screen)
        i.ddger_group.draw(move_screen)
        i.ddger_group.update()
        move_screen.blit(GI.update('screenHigh'), [0, 0])
        move_screen.blit(GI.update('all'), [0, 0])
        Initi.screen.blit(move_screen, next(i.offset))

#                   ,,
# `7MMM.     ,MMF'  db
#   MMMb    dPMM
#   M YM   ,M MM  `7MM  ,pP"Ybd  ,p6"bo
#   M  Mb  M' MM    MM  8I   `" 6M'  OO
#   M  YM.P'  MM    MM  `YMMMa. 8M
#   M  `YM'   MM    MM  L.   I8 YM.    ,
# .JML. `'  .JMML..JMML.M9mmmP'  YMbmd'


class GI(grph.add):
    # Stands for Graphics Interface, inherits from a grph function
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This directally passes all variables to grph.add.__init__

    def kill(self):
        super().kill()

    @staticmethod
    def update(flag):
        screen = grph.add.update(flag)
        return screen


def minmax(a, b, c):
    '''This function returns the middle variable between the min variable
    and the max variable.'''
    return (lambda x: sorted(x)[1])([a, b, c])


def die_screen(dxy):
    global i
    GI('all', grph.Transition, "background_res2.png", i.score)
    if pygame.key.get_pressed()[pygame.K_x]:
        # Change to incorporate the movement of the helment
        i = Initi(i.lvl)


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.key.get_pressed()[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
            print(event)


# https://stackoverflow.com/questions/23633339/pygame-shaking-window-when-loosing-lifes


def shake():
    equ = lambda t: round((math.e ** (-t // 5)) * math.cos(2*math.pi*t)*5,2)
    sr = lambda: round(random.randrange(-1, 2, 2), 0)
    for _ in range(0, 2):
        for x in range(4, 1, -1):
            yield (equ(x)*sr(), equ(x)*sr())
    while True:
        yield (0, 0)

#                               ,,
# `7MM"""YMM                  `7MM
#   MM    `7                    MM
#   MM   d    `7MMpMMMb.   ,M""bMM
#   MMmmMM      MM    MM ,AP    MM
#   MM   Y  ,   MM    MM 8MI    MM
#   MM     ,M   MM    MM `Mb    MM
# .JMMmmmmMMM .JMML  JMML.`Wbmd"MML.


if __name__ == '__main__':
    global i
    i = Initi()
    print(i)
    main()
