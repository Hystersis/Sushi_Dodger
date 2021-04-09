# Sushi Dodger
# Created by Marcus W, 2020 - 2021
# Screen size = 256*256

# All these modules
import pygame
from pygame.freetype import * # Errors led to this line, having to be here
import ctypes
import math
import sys, os
from itertools import repeat
import random

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
class initi:
    def __init__(self,lvl = 1):
        pygame.init()
        self.screen_width = 256
        self.gm = 'Active'
        self.icon = pygame.image.load(os.path.join("Assets/","dodger_icon.png"))
        pygame.display.set_icon(self.icon)
        self.myappid = 'mycompany.myproduct.subproduct.version' # allows for taskbar icon to be changed
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_width),flags=pygame.RESIZABLE | pygame.SCALED) # This allows the screen to be bigger that it was
        pygame.display.set_caption("Sushi Dodger")
        pygame.mouse.set_visible(False) # So the cursor isn't shown
        self.score = 0
        # Level and dodger initilization
        self.lvel = self.Level(lvl)
        self.ddger = dodger(os.path.join("Assets/","dodger_1.png"))
        self.ddger_group = pygame.sprite.Group()
        self.ddger_group.add(self.ddger)
        self.pstn = self.ddger.where_am_i()
        self.offset = repeat((0,0))
        # sushi setup code
        self.sshi_group = pygame.sprite.Group()
        for a in range(self.num):
            self.sshi = sushi([random.randrange(240),random.randrange(240)],self.pstn) # Change [128,16] if starting pos of ddger is changed
            self.sshi_group.add(self.sshi)
    def Level(self,lvl):
        self.lvl = lvl
        self.n = list(map(lambda y: y*2+12, range(2,15)))
        self.n.insert(0,10)
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





class sushi(pygame.sprite.Sprite):
    def __init__(self, sop,d_xy):
        super().__init__()
        self.relation_x = round(sop[0]) - round(d_xy[0])
        self.relation_y = round(sop[1]) - round(d_xy[1])
        self.sop = [poscheck(sop[0],d_xy[0]),poscheck(sop[1],d_xy[1])]
        self.dirny = self.dirnx = 0
        self.rt = pygame.image.load(os.path.join("Assets/",'sushi_template.png'))
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = os.path.join("Assets/",self.directory + str(self.ran) + '.png')
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0,0))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.sop
        print(self.rect.topleft)
    def update(self,d_xy):
        if len(i.ddger_group) > 0:
            self.d = [0,0]
            ran = lambda : round(random.uniform(0.6,1.4),2)
            self.d[0] += (ran() if self.sop[0] <= d_xy[0] else -ran())
            self.d[1] += (ran() if self.sop[1] <= d_xy[1] else -ran())
            self.sop = tuple(map(lambda x,y:minmax(0,x+y,240),self.rect.topleft,self.d))
            self.check_hit = pygame.sprite.spritecollide(i.ddger,i.sshi_group,False)
            # self.sop_copy = deepcopy(self.sop) # WHy iS tHis LinE heRe?
            if len(self.check_hit) >= 1 and (lambda x: x[0] and x[1])(list(map(lambda sop,dxy:-16<(sop-dxy)<16,self.sop,d_xy))):
                i.offset = shake()
                i.ddger.killed() if (self.sop[1] - d_xy[1]) >= 0 else self.killed()
            self.rect.topleft = tuple(self.sop)
    def killed(self):
        print('Killed!')
        i.score += 1
        self.kill()
        print('len:',len(i.sshi_group))
        if len(i.sshi_group) == 0:
            i.gm = 'Won'
            print('Won',i.gm)

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
    clock = pygame.time.Clock()
    global i
    print('I:',i)
    while True:
        print(i.gm) if i.gm == 'Won' else None
        move_screen = i.screen.copy()
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
                i = initi(i.lvl)

        if i.gm == 'Active':
            pstn = i.ddger.where_am_i()
            # print('Score:',score)
            fps = clock.get_fps()
            # print("FPS:", fps)
            i.sshi_group.update(pstn)

        if i.gm == 'Died':
            die_screen(i.ddger.where_am_i())

        if i.gm == 'Won':
            print('Won')
            i = initi((i.lvl + 1))

        grph.data['score'] = i.num - len(i.sshi_group)

        pygame.display.flip()
        move_screen.blit(pygame.image.load(os.path.join("Assets/",'background_res2.png')),[0,0])
        move_screen.blit(grph.screenLow(move_screen),[0,0])
        i.sshi_group.draw(move_screen)
        i.ddger_group.draw(move_screen)
        i.ddger_group.update()
        move_screen.blit(grph.screenHigh(move_screen,i.gm),[0,0])
        i.screen.blit(move_screen,next(i.offset))
        # screen.current_w, screen.screen_h = screen_shake(1), screen_shake(1)

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
    te = grph.text_eight({'surf':None,'text':'yes'})
    if pygame.key.get_pressed()[pygame.K_x]:
        #Change to incorporate the movement of the helment
        i = initi(i.lvl)

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
    sr = lambda : round(random.randrange(-1,2,2),0)
    for _ in range(0, 2):
        for x in range(4, 1, -1):
            yield (equ(x)*sr(), equ(x)*sr())
    while True:
        yield (0, 0)



# class screen_shake:
#     def __init__(self):
#         self.sr_num = []
#         self.strength = ()
#     def shake(self):
#         equ = lambda t: round(math.e ** (-t // 10) * math.cos(2*math.pi*t)*random.uniform(1.1,5.2),2)
#         self.sr_num = [equ(t) for t in range(-6,4)]
#         self.strength = ((lambda x,y: (x,y))) ((equ(t) for t in range(-6,4)), (equ(t) for t in range(-6,4)))
#     def ye(self):
#         return self.strength.pop(0) if len(self.strength) > 0 else (0,0)
#
# scsh = screen_shake()


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
    i = initi()
    print(i)
    main()
