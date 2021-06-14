# Sushi Dodger
# Created by Marcus W, 2020 - 2021
# Screen size = 256*256

# All these modules
import pygame
# from pygame.freetype import * # Errors led to this line, having to be here
import math
import os
from itertools import repeat, cycle, count
import random
from operator import sub, add
from copy import deepcopy
import time

# This importing the other modules into core
import sshi_graphics as grph
from sshi_msci import Apj
import sshi_score as sce
import sshi_special as spe


#                     ,,
# `7MMF'              db   mm
#   MM                     MM
#   MM  `7MMpMMMb.  `7MM mmMMmm
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
# .JMML..JMML  JMML..JMML. `Mbmo
class Initi:
    screen = None

    def __init__(self, lvl=1, screen=None):
        if screen != None: Initi.screen = screen
        pygame.init()
        self.screen_width = 256
        self.gm = 'Active'
        pygame.mouse.set_visible(False)  # So the cursor isn't shown
        self.score = 0
        # Level and dodger initilization
        self.lvel = self.Level(lvl)
        self.ddger = Dodger(os.path.join("Assets", "dodger_1.png"))
        self.offset = repeat((0, 0))
        # sushi setup code
        self.sshi_group = pygame.sprite.Group()
        for a in range(self.num):
            self.sshi = Sushi(self.ddger)
            # Change [128,16] if starting pos of ddger is changed
            self.sshi_group.add(self.sshi)
        self.layers = pygame.sprite.LayeredUpdates()
        for num_of_layer in range(6):
            '''Background = 0
            screenLow = 1
            sprites = 2
            screenEffects = 3
            screenHigh = 4
            all = 5'''
            self.layers.add(Placeholder(), layer=num_of_layer)
        self.board = sce.scoreboard()
        self.layers.add(self.ddger, self.sshi_group, layer=2)
        self.background = Background('background_res2.png')
        self.layers.add(self.background, layer=0)
        self.p = DifficultlyStats()
        self.missile = spe.missile((0, 0), 1)
        self.layers.add(self.missile, layer=2)

    def Level(self, lvl):
        self.lvl = lvl
        self.n = list(map(lambda y: y*2+12, range(2, 15)))
        self.n.insert(0, 10)

        def get_num():
            return self.n[self.lvl - 1 if self.lvl < 14 else 13]
        self.num = get_num()

    def __repr__(self):
        return 'Initialization object'


class Placeholder(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class DifficultlyStats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dodger = {
            'movevalue': 1.6,
        }
        self.sshi = {
            'intelligence': 0,
        }

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
        global i
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -(i.p.dodger['movevalue'])
            elif keys[pygame.K_RIGHT]:
                self.dirnx = i.p.dodger['movevalue']
            else:
                self.dirnx = 0

            if keys[pygame.K_UP]:
                self.dirny = -(i.p.dodger['movevalue'])
            elif keys[pygame.K_DOWN]:
                self.dirny = i.p.dodger['movevalue']
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
        return [list(self.rect.topleft), list(self.rect.bottomright)]

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
        global i
        self.ddger_pos = [i.ddger.rect.midtop[0], i.ddger.rect.midtop[1]
                          + i.p.sshi['intelligence']]
        self.delta = list(map(sub, self.ddger_pos, self.rect.midtop))
        # This maps each coordinate of ddger and sshi; ddger - sshi
        # Intelligence is the factor for the sushi to aim for the bottom of
        # the ddger, can lead to avoiding ddger
        self.deltap = list(map(lambda z: z * random.uniform(0.8, 1.2) / abs(z)
                               if z != 0 else 0, self.delta))
        # This returns a -1, 0 or 1 (with a little bit of noise)
        # depending on the delta
        self.deltan = list(map(sub, i.ddger.rect.center, self.rect.center))
        if not self.avoid():
            self.rect.topleft = tuple(map(minmax, [0, 0],
                                          map(add,
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
        # i.ddger.killed()
        if len(list(filter(lambda a: -16 < a < 16, self.deltan))) == 2:
            # This sees if sshi is in AoE of the ddger
            i.offset = shake()  # This shakes the screen
            i.ddger.killed() if self.deltan[1] < 0 else self.killed()
            # This kills the ddger if it is bellow the sshi, and vice versa

    def avoid(self):
        if len(list(filter(lambda a: -48 < a < 48, self.deltan))) == 2:
            if -20 < self.deltan[0] < 20 and 24 > self.deltan[1] > 8:
                self.rect.topleft = closer(-48, self.rect.topleft[0],
                                           48,
                                           i.p.sshi['intelligence'] / 16),\
                                    self.rect.topleft[1]\
                                    - i.p.sshi['intelligence'] / 16
                return True
        return False


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
    track_previous_gm = 'Active'
    while True:
        move_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        # print('Gamemode:\t',gm)
        clock.tick(10)
        act = pygame.key.get_focused()
        if act and i.gm == 'Paused':
            i.gm = 'Active'
        elif not act and i.gm == 'Active':
            i.gm = 'Paused'

        if i.gm != 'Died':
            events()  # As die screen has its own event system

        if pygame.key.get_pressed()[pygame.K_F5]:
            i = Initi(i.lvl)

        if i.gm == 'Active':
            # print('Score:',score)
            i.sshi_group.update()

        if i.gm == 'Died' and track_previous_gm != 'Died':
            d = die_screen()
        elif i.gm == 'Died':
            d()
        elif i.gm != 'Died' and track_previous_gm == 'Died':
            d.kill()

        if i.gm == 'Won' and track_previous_gm != 'Won':
            print('Won')
            i = Initi(i.lvl + 1)
        elif i.gm == 'Won':
            pass  # Add code here later

        i.score = i.num - len(i.sshi_group)

        pygame.display.flip()
        move_screen.fill((0, 0, 0)), Initi.screen.fill((0, 0, 0))
        i.background.draw(Initi.screen)
        i.layers.draw(move_screen)
        i.ddger.update()
        Initi.screen.blit(move_screen, next(i.offset))
        track_previous_gm = i.gm
        i.missile.update(i.ddger)

#                   ,,
# `7MMM.     ,MMF'  db
#   MMMb    dPMM
#   M YM   ,M MM  `7MM  ,pP"Ybd  ,p6"bo
#   M  Mb  M' MM    MM  8I   `" 6M'  OO
#   M  YM.P'  MM    MM  `YMMMa. 8M
#   M  `YM'   MM    MM  L.   I8 YM.    ,
# .JML. `'  .JMML..JMML.M9mmmP'  YMbmd'


def minmax(a, b, c):
    '''This function returns the middle variable between the min variable
    and the max variable.'''
    return (lambda x: sorted(x)[1])([a, b, c])


def closer(a, b, c, by=1):
    '''This function returns what the effect of by will be on +/- it
    to b, this returns which operation should be performed to get the closetest
    to a or c'''
    smaller = min(a, c)
    larger = max(a, c)
    minus = [(b - by) - smaller, b - by]
    addition = [larger - (b + by), b + by]
    if min(minus[0], addition[0]) == minus[0]:
        return minus[1]
    else:
        return addition[1]


#  .M"""bgd
# ,MI    "Y
# `MMb.      ,p6"bo `7Mb,od8 .gP"Ya   .gP"Ya `7MMpMMMb.  ,pP"Ybd
#   `YMMNq. 6M'  OO   MM' "',M'   Yb ,M'   Yb  MM    MM  8I   `"
# .     `MM 8M        MM    8M"""""" 8M""""""  MM    MM  `YMMMa.
# Mb     dM YM.    ,  MM    YM.    , YM.    ,  MM    MM  L.   I8
# P"Ybmmd"   YMbmd' .JMML.   `Mbmmd'  `Mbmmd'.JMML  JMML.M9mmmP'


class die_screen():
    states = {'Score': 'defeat_screenV3-3.png',
              'Board': 'score_screen1.png',
              'Fade': 'fade_out.bmp'}
    def __init__(self):
        global i
        self.YPpos = [add(x, i.ddger.pos[1]) for x in [0, 1, 2, 3, 4,
                                                                3, 2, 1]]
        self.Ppos = cycle(zip(repeat(i.ddger.pos[0]),
                              self.YPpos))
        # The expression above zips together the x coordinate of ddger
        # This x coordinate is repeated, so it just keeps on
        # yelling the same value,  while the Y pos is from the
        # addition mapping above that takes in the y pos, and maps 0,1,2 ...
        # To it.
        self.group = pygame.sprite.Group()
        Background.change_i('defeat_screenV2.png')
        self.ripple = grph.ripple()
        self.group.add(self.ripple)
        i.layers.add(self.ripple, layer=1)
        self.time = time.time()
        i.layers.remove_sprites_of_layer(2)
        print(i.sshi_group)
        self.fade = count(0, 5)
        self.menu_screen = Background('blank.png')
        self.menu_screen.set_alpha(0)
        i.layers.add(self.menu_screen, layer=2)
        self.state = 'Score'
        self.screen_state = 'blank.png'
        self.scoreboard = sce.scoreboard()
        self.mask = pygame.mask.Mask(size=(256, 256))
        self.mask.draw(pygame.mask.Mask(size=(134, 130), fill=True), (61, 94))

    def __call__(self):
        global i
        self.temp_screen = pygame.image.load(
                                             os.path.join("Assets",
                                                          self.screen_state))
        if self.state == 'Changing':
            self.next = next(self.count_for_fade)
            if -11 < self.next < 11:
                self.screen_out = pygame.image.load(
                                             os.path.join("Assets",
                                                          die_screen.states[self.screen_out_state]))
                self.screen_in = pygame.image.load(
                                             os.path.join("Assets",
                                                          die_screen.states[self.screen_in_state]))

                self.screen_out.set_alpha(((10 -abs(self.next)) / 9) * 255)
                self.screen_in.set_alpha((abs(self.next) / 9) * 255)
                if self.screen_in_state == 'Board':
                    self.temp_screen.blit(self.screen_out, [0 - self.next, 0])
                    self.temp_screen.blit(self.screen_in, [0 + (10 - self.next), 0])
                elif self.screen_in_state == 'Score':
                    self.temp_screen.blit(self.screen_out, [0 - self.next, 0])
                    self.temp_screen.blit(self.screen_in, [0 + (-10 - self.next), 0])
                else:
                    self.temp_screen.blit(self.screen_out, [0, 0])
                    self.temp_screen.blit(self.screen_in, [0, 0], special_flags=pygame.BLEND_SUB)
                    if self.next <= 0:
                        i = Initi(i.lvl)
                        self.kill()
                        return

                self.menu_screen.change_i(self.temp_screen, 2)
            else:
                self.state = self.screen_in_state
        if (time.time() - self.time) >= 2.5 and self.state == 'Score':
            self.temp_screen.blit(pygame.image.load(os.path.join("Assets", die_screen.states[self.state])), [0, 0])
            new_xy = grph.word_wrap(self.temp_screen,
                                    str(i.score),
                                    pygame.freetype.Font(os.path.join("Assets", '8-bit Arcade In.ttf'), 96), 
                                    xy=['center', 128],
                                    colour=(46, 34, 47))
            grph.word_wrap(self.temp_screen,
                           str(i.score),
                           pygame.freetype.Font(os.path.join("Assets", '8-bit Arcade Out.ttf'), 96),
                           xy=new_xy, colour=(255, 130, 77))
            self.menu_screen.change_i(self.temp_screen, 2)
        if (time.time() - self.time) >= 2.5 and self.state == 'Board':
            if self.last_state != 'Board':
                self.iter_for_board_scroll = cycle(list(repeat(0, 10))
                                                   + [x for x in range(0, 74)]
                                                   + list(repeat(74, 10))
                                                   + [y for y in range(74, 0, -1)])
            self.temp_screen.blit(pygame.image.load(os.path.join("Assets", die_screen.states[self.state])), [0, 0])
            self.score_screen = pygame.Surface((256, 512), flags=pygame.SRCALPHA)
            for num, name_score in enumerate(self.scoreboard.get()):
                name, score = name_score
                name_score_string = f'{name}  {score}'
                grph.word_wrap(self.score_screen,
                               name_score_string,
                               pygame.freetype.Font(os.path.join("Assets", 'manaspace.regular.ttf'), 24),
                               xy = (61, 101 + 20*num), colour=(49, 54, 56))
            self.mask_copy = self.mask.copy()
            self.next_a = -next(self.iter_for_board_scroll)
            self.score_screen.scroll(dy=self.next_a)
            self.score_screen = self.mask_copy.to_surface(self.score_screen,
                                                          setsurface=self.score_screen,
                                                          unsetcolor=(0, 0, 0, 0))
            self.temp_screen.blit(self.score_screen, (0, 0))
            self.menu_screen.change_i(self.temp_screen, 2)


        self.ripple.update()
        self.last_state = deepcopy(self.state)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    # Change to incorporate the movement of the helmet
                    self.fade_out()
                elif event.key == pygame.K_RIGHT and self.state == 'Score':
                    self.change_fade()
                elif event.key == pygame.K_LEFT and self.state == 'Board':
                    self.change_fade()
            events_seperated(event)

    def kill(self):
        for sprite in self.group:
            sprite.kill()

    def change_fade(self):
        if self.state == 'Score':
            self.screen_in_state = 'Board'
            self.screen_out_state = 'Score'
            self.count_for_fade = count(0)
        elif (time.time() - self.time) >= 2.5:
            self.screen_out_state = 'Board'
            self.screen_in_state = 'Score'
            self.count_for_fade = count(0, -1)
        self.state = 'Changing'

    def fade_out(self):
        self.screen_out_state = 'Fade'
        self.screen_in_state = 'Fade'
        self.state = 'Changing'
        self.screen_state = 'blank8.png'
        self.count_for_fade = count(10, -1)

    def remind(self, screen):
        pass


class Background(pygame.sprite.Sprite):
    def __init__(self, image, alpha=255):
        super().__init__()
        if type(image) is str:
            self.image = pygame.image.load(os.path.join('Assets', image))

        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self, surface, alpha=255):
       surface.blit(self.image, (0, 0))

    def blit(self, surface):
        self.image.blit(surface, (0, 0))

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)
        print(alpha)

    @classmethod
    def change_i(cls, image, layer=0, a=255):
        i.layers.remove(i.background)
        i.background = cls(image, a)
        i.layers.add(i.background, layer=layer)


# class win_screen():
#     def __inti__(self):
#

def events():
    for event in pygame.event.get():
        events_seperated(event)


def events_seperated(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()
        print(event)

# https://stackoverflow.com/questions/23633339/pygame-shaking-window-when-loosing-lifes


def shake():
    for _ in range(0, 2):
        for x in range(4, 1, -1):
            yield (equ(x)*sr(), equ(x)*sr())
    while True:
        yield (0, 0)


def equ(x):
    '''This function is a dampered osilation based off:
    https://deutsch.physics.ucsc.edu/6A/book/harmonic/node18.html'''
    return round((math.e ** (-x//5)) * math.cos(2*math.pi*x)*5, 2)


def sr():
    '''This randomly returns a positive or negative 1'''
    return random.randrange(-1, 2, 2)



#                               ,,
# `7MM"""YMM                  `7MM
#   MM    `7                    MM
#   MM   d    `7MMpMMMb.   ,M""bMM
#   MMmmMM      MM    MM ,AP    MM
#   MM   Y  ,   MM    MM 8MI    MM
#   MM     ,M   MM    MM `Mb    MM
# .JMMmmmmMMM .JMML  JMML.`Wbmd"MML.


def start(screen=None):
    global i
    i = Initi(screen=screen)
    main()


if __name__ == '__main__':
    icon = pygame.image.load(os.path.join("Assets", "dodger_icon.png"))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Sushi Dodger")
    screen = pygame.display.set_mode((256, 256), flags=pygame.RESIZABLE
                                     | pygame.SCALED)
    start(screen)
