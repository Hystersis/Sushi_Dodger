# Sushi Dodger
# Created by Hystersis W, 2020 - 2021
# Screen size = 256*256

# All these modules
import pygame
# from pygame.freetype import * # Errors led to this line, having to be here
import math
import os
import string
from itertools import repeat, cycle, count
import random
from operator import sub, add, mul
from copy import deepcopy
import time
from collections import Counter
from abc import ABC, abstractmethod

# This importing the other modules into core
import sshi_graphics as grph
from sshi_msci import Apj
import sshi_json as jsn
import sshi_special as spe
import tkinter
from tkinter import messagebox


#                     ,,
# `7MMF'              db   mm
#   MM                     MM
#   MM  `7MMpMMMb.  `7MM mmMMmm
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
#   MM    MM    MM    MM   MM
# .JMML..JMML  JMML..JMML. `Mbmo
class Initi:
    """A class that manages initalisation variables and flow

    Attributes
    ----------
    screen : pygame.Surface
        This is the main screen of the game - it is a low-level variable so,
        the screen doesn't flash when restarting as it isn't recreated
    """    
    screen = None

    def __init__(self, lvl=1, screen=None):
        """Initalisation of the game

        Parameters
        ----------
        lvl : int, optional
            This is the starting level of the game, by default 1
        screen : pygame.Surface, optional
            This is the passed through screen from sshi_base
            this is so the experience is one constant screen, by default None

        Attributes
        ----------
        screen : pygame.Surface
            Main screen of the game
        screen_width : int
            CONSTANT, width of the screen
        gm : str
            Current game mode either:
                Active - the game is being played
                Won - the player has passed a level
                Died - the player is deceased
                Paused - the player doesn't have the game currently in focus
        score : int
            The player's score
        lvel : int
            The current level of the game
            See Also
            --------
            Initi.Level:
                Is a sudo-class for holding the current level and how
                many enemies should be on the screen
        ddger : int
            The player's score
        """
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
        self.unayers = pygame.sprite.LayeredUpdates()
        # Shorthand for UNAffected laYERS
        for num_of_layer in range(2):
            '''Two layers: 0, 1'''
            self.unayers.add(Placeholder(), layer=num_of_layer)
        self.board = jsn.scoreboard()
        self.layers.add(self.ddger, self.sshi_group, layer=2)
        self.background = Background('background_res2.png')
        self.layers.add(self.background, layer=0)
        global c
        self.layers.add(c.items, layer=0)
        self.event_sys = events_sync()
        self.event_sys.listen('Active', pygame.KEYDOWN, self.ddger.killed, pygame.K_F2)
        self.laser = spe.laser_enemy((0, 0))
        self.missile = spe.missile((0, 0))

        self.layers.add(self.missile, layer=2)
        self.layers.add(self.laser, layer=2)
        if c._health == 0:
            print('health added')
            c.items += item(iV=self, **{"name": "health",
                                        "sprite": jsn.items().item_val(
                                            'health', 'sprite')})
            c._health += 1

    def Level(self, lvl):
        """Creates a list of amount of sushi that should be in each
        level, it then receives the level num and recalls the amount
        of sushi that should be in the level

        Parameters
        ----------
        lvl : int
            The level to be recalled
        Returns
        -------
        int
            The amount of sushi that should be in the level
        """        
        self.lvl = lvl
        self.n = list(map(lambda y: y*2+12, range(2, 15)))
        self.n.insert(0, 10)

        def get_num():
            """Gets the amount of sushi from the list using the lvl parameter

            Returns
            -------
            int
                The amount of sushi to be in the level
            """            
            return self.n[self.lvl - 1 if self.lvl < 14 else 13]
        self.num = get_num()

    def __repr__(self):
        return 'Initialization object'


class Placeholder(pygame.sprite.Sprite):
    """A placeholder for certain situation where something needs to
    be kept open
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class DifficultlyStats:
    """
    These are the stats that allow for
    granular control over parts of the game
    therefore allowing for the difficulty to
    be changed
    """    
    def __init__(self):
        """
        Resets all items to their original state and
        it also creates the item manager
        """        
        self.reset()
        self.items = item_manager()

    def reset(self):
        """Resets all values to their original state
        """        
        self.fps = 10
        self.overall_speed = 1
        # Allows for all entities to be speed up by one control
        self._dspeed = 1.6
        self.intelligence = 0  # The higher the number more 'intelligent', max: 16
        self._sspeed = 1  # The higher the number the faster
        self.sensitivity = 0.2  # The higher the number the less sensitive
        self.luck = 0.2  # This has to be a decimal or 1, aka drop_rate
        self._health = 0
        self._score = 0

    @property
    def dspeed(self):
        """The speed of the ddger

        Returns
        -------
        float
            The dodger speed effected by the overall speed
        """        
        return self._dspeed * self.overall_speed

    @dspeed.setter
    def dspeed(self, value):
        """Allows for the setting of the internal
        ddger speed value

        Parameters
        ----------
        value : float
            The value wished for dspeed to be
        """        
        self._dspeed = value

    @property
    def sspeed(self):
        return self._sspeed * self.overall_speed

    @sspeed.setter
    def sspeed(self, value):
        self._sspeed = value

    def load_from_json(self):
        jsn.config.get(self)

    @property
    def health(self):
        # self.reset_item("health", self._health, [0, 0])
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.reset_item("health", self._health, [0, 0])

    @property
    def score(self):
        self.reset_item("score", self._score, [0, 0])
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.reset_item("score", self._score, [0, 0])
        # !This must be changed to demonstrate the score's sprite sheet

    def reset_item(self, item: str, val: int, sprite: list):
        num_items = c.items.len(item)
        if num_items > val:
            for _ in range(num_items - val):
                del c.items[item]
        elif num_items < val:
            for _ in range(num_items - val):
                c.items += item(**{"name": item, "sprite": sprite})


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
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.dirncy = 0
        self.lives = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global i, c
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -(c.dspeed)
            elif keys[pygame.K_RIGHT]:
                self.dirnx = c.dspeed
            else:
                self.dirnx = 0

            if keys[pygame.K_UP]:
                self.dirny = -(c.dspeed)
            elif keys[pygame.K_DOWN]:
                self.dirny = c.dspeed
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
        # i.gm = 'Died'
        # self.kill()
        # print('You died!, press \'X\' to start again', i.gm)
        pass



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
        self.move = sshi_classic_movement()
        self.hit = sshi_classic_hit()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global i, c
        if type(self.move) is sshi_classic_movement:
            self.movement = tuple(map(add, map(mul, self.move(self, i.ddger), repeat(1 - c.intelligence / 16)), map(mul, sshi_avoid_movement()(self, i.ddger), repeat(c.intelligence / 16))))
            self.rect.topleft = tuple(map(minmax, (0, 0), self.movement, (239, 239)))
        self.hit(self, i.ddger)

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

    def killed(self, do_drop=True):
        # Do drop exists when a sshi dies due to the ddger having another life
        # the sshi doesn't just drop another one
        global score
        score += 1
        self.kill()
        if len(i.sshi_group) == 0:
            i.gm = 'Won'
        if random.random() <= c.luck and do_drop:
            c.items += jsn.items().return_item(item, start_pos = self.rect.topleft)

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


class sshi_movement(ABC):
    @abstractmethod
    def __call__(self, sshi, ddger):
        pass


class sshi_hit(ABC):
    @abstractmethod
    def __call__(self, sshi, ddger):
        pass


class sshi_classic_movement(sshi_movement):
    def __call__(self, sshi: Sushi, ddger: Dodger):
        global i, c
        self.ddger_pos = [ddger.rect.midtop[0], ddger.rect.midtop[1]
                          + c.intelligence]
        # This maps each coordinate of ddger and sshi; ddger - sshi
        # Intelligence is the factor for the sushi to aim for the bottom of
        # the ddger, can lead to avoiding ddger
        self.delta = list(map(sub, self.ddger_pos, sshi.rect.midtop))
        # This returns a -1, 0 or 1 (with a little bit of noise)
        # depending on the delta
        self.deltap = list(map(lambda z: spe.sign(z) * random.uniform(
            1 - c.sensitivity,
            1 + c.sensitivity),
                self.delta))
        self.deltan = tuple(map(sub, ddger.rect.center, sshi.rect.center))
        # This adds the aforementioned -1, 0 or 1 to the current
        # coordinates of sshi
        return tuple(map(add, sshi.rect.topleft, self.deltap))


class sshi_avoid_movement(sshi_movement):
    def __call__(self, sshi: Sushi, ddger: Dodger) -> tuple:
        global i, closer
        self.sense = c.intelligence * 3
        self.sH = c.intelligence * 2
        self.deltan = list(map(sub, ddger.rect.center, sshi.rect.center))
        by = c.intelligence / 16 + c.sspeed
        if len(list(filter(lambda a: -self.sense < a < self.sense, self.deltan))) == 2\
                and c.intelligence >= 8:
            if self.sH > self.deltan[1] > 8:
                self.closer = tuple(map(closer, repeat(-self.sense),
                                        self.deltan, repeat(self.sense),
                                        repeat(by)))
                self.NEW_pos = map(sub, map(sub, i.ddger.rect.center, self.closer), (8, 8))
                return self.NEW_pos
            elif 8 >= self.deltan[1] >= -8:
                self.xmovement = closer(-self.sense, self.deltan[0], self.sense, by)
                self.xmovement = -by if self.xmovement < self.deltan[0] else by
                self.ymovement = -by
                self.NEW_pos = tuple(map(add, sshi.rect.topleft, (self.xmovement, self.ymovement)))
                return self.NEW_pos
            elif -self.sH < self.deltan[1] < -8:
                self.deltam = list(map(sub, ddger.rect.midbottom, sshi.rect.midbottom))
                self.xmovement = math.copysign(by, -self.deltam[0])
                self.ymovement = spe.sign(math.sin(abs(self.deltam[0])/(self.sense/math.pi))*(self.sense-8), by)
                # The sin function = sin(abs(xpos/(max_x_value/pi)))*max_height
                self.NEW_pos = tuple(map(sub, sshi.rect.topleft, (self.xmovement, self.ymovement)))
                return self.NEW_pos
        return sshi_classic_movement()(sshi, ddger)


class sshi_classic_hit(sshi_hit):
    def __call__(self, sshi: Sushi, ddger: Dodger):
        self.deltan = list(map(sub, ddger.rect.center, sshi.rect.center))
        if len(list(filter(lambda a: -16 < a < 16, self.deltan))) == 2:
            # This sees if sshi is in AoE of the ddger
            i.offset = shake()  # This shakes the screen
            if self.deltan[1] < 0:
                c.health -= 1
                if c.health >= 1:
                    sshi.killed(False)
                    c.items.minus_of(jsn.items().item_val('health', 'sprite'),
                                     self.rect.topleft)
                else:
                    i.ddger.killed()
            else:
                pygame.mixer.Sound(os.path.join("Assets","Sounds","Sword-swish.wav")).play().set_volume(0.07)
                sshi.killed()



#                            ,,
# `7MMM.     ,MMF'           db
#   MMMb    dPMM
#   M YM   ,M MM   ,6"Yb.  `7MM  `7MMpMMMb.
#   M  Mb  M' MM  8)   MM    MM    MM    MM
#   M  YM.P'  MM   ,pm9MM    MM    MM    MM
#   M  `YM'   MM  8M   MM    MM    MM    MM
# .JML. `'  .JMML.`Moo9^Yo..JMML..JMML  JMML.

def main():
    """This the main loop of the program
    Notes
    -----
    This function will be the only while loop in the program and
    will continually run until interupted
    """    
    clock = pygame.time.Clock()
    global i, c
    track_previous_gm = 'Active'
    while True:
        # try:
        move_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        clock.tick(c.fps)
        act = pygame.key.get_focused()
        if act and i.gm == 'Paused':
            i.gm = 'Active'
        elif not act and i.gm == 'Active':
            i.gm = 'Paused'

        i.event_sys()

        if i.gm == 'Active':
            i.sshi_group.update()
            c.items.update()

        if i.gm == 'Died' and track_previous_gm != 'Died':
            d = die_screen()
        elif i.gm == 'Died':
            d()
        elif i.gm != 'Died' and track_previous_gm == 'Died':
            d.kill()

        if i.gm == 'Won' and track_previous_gm != 'Won':
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
        i.unayers.draw(Initi.screen)
        track_previous_gm = i.gm
        i.missile.update(i.ddger, i.sshi_group)
        i.laser.update(i.ddger, i.sshi_group)
        # except Exception as the_error:
        #     # This makes sure the tkinter screen isn't visable
        #     TK_screen = tkinter.Tk()
        #     TK_screen.withdraw()
        #     # This displays the error
        #     messagebox.showerror(title='Error', message=f"A fatal error has occured: {the_error}")
        #     pygame.quit()
        #     quit()


#                   ,,
# `7MMM.     ,MMF'  db
#   MMMb    dPMM
#   M YM   ,M MM  `7MM  ,pP"Ybd  ,p6"bo
#   M  Mb  M' MM    MM  8I   `" 6M'  OO
#   M  YM.P'  MM    MM  `YMMMa. 8M
#   M  `YM'   MM    MM  L.   I8 YM.    ,
# .JML. `'  .JMML..JMML.M9mmmP'  YMbmd'


def minmax(a, b, c):
    """This returns the middle parameter

    Parameters
    ----------
    a : int | float
        Any number
    b : int | float
        Any number
    c : int | float
        Any number

    Returns
    -------
    int | float
        Returns the middle parameter between the max and min variables
    """
    return (lambda x: sorted(x)[1])([a, b, c])


def closer(a, b, c, by=1, maximise=False):
    '''This function returns what the effect of by will be on +/- it
    to b, this returns which operation should be performed to get the closetest
    to a or c'''
    smaller = min(a, c)
    larger = max(a, c)
    minus = [(b - by) - smaller, b - by]
    addition = [larger - (b + by), b + by]
    if min(minus[0], addition[0]) == minus[0]\
            or maximise and min(minus[0], addition[0]) == addition[0]:
        return minus[1]
    else:
        return addition[1]


# From https://realpython.com/python-rounding/#a-menagerie-of-methods
def round5(num, d=0):
    multiplier = 10 ** d
    rounded_abs = math.floor(abs(num)*multiplier + 0.5) / multiplier
    return math.copysign(rounded_abs, num)


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
        i.layers.remove(c.items)
        c.items.empty()
        self.fade = count(0, 5)
        self.menu_screen = Background('blank.png')
        self.menu_screen.set_alpha(0)
        i.layers.add(self.menu_screen, layer=2)
        self.state = 'Score'
        self.screen_state = 'blank.png'
        self.scoreboard = jsn.scoreboard()
        self.mask = pygame.mask.Mask(size=(256, 256))
        self.mask.draw(pygame.mask.Mask(size=(134, 130), fill=True), (61, 94))
        self.message = grph.message_box('Press the key x to restart, press the key z to enter text input mode for scoreboard', (106, 23, 45, 100), [256, 16], xy=[0, 240])
        i.unayers.add(self.message, layer=0)
        self.text_input = input_box(20, 92, 3, UpperLowerSentence='U', length=3, disallowed_words=['ASS', 'SEX', 'JDH'])
        self.show_text_input = False
        i.event_sys.listen('Died', pygame.KEYDOWN, self.fade_out, pygame.K_x)
        i.event_sys.listen('Died', pygame.KEYDOWN, self.ask_for_input, pygame.K_z)
        i.event_sys.listen('Died', pygame.KEYDOWN, self.change_fade, pygame.K_RIGHT, 'Right')
        i.event_sys.listen('Died', pygame.KEYDOWN, self.change_fade, pygame.K_LEFT, 'Left')

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
            self.message.kill()
            self.message = grph.message_box('Press the key x to restart', (106, 23, 45, 100), [256, 16], xy=[0, 240])
            i.unayers.add(self.message, layer=0)
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
                self.message.kill()
                self.message = grph.message_box('Press the key x to restart, press the key z to enter text input mode for scoreboard', (106, 23, 45, 100), [256, 16], xy=[0, 240])
                i.unayers.add(self.message, layer=0)
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
            if self.show_text_input:
                x = self.text_input.handle_events()
                self.text_input.draw(self.temp_screen)
                if type(x) is list and x[0] == 'Entered':
                    print('Written')
                    self.show_text_input = None
                    self.scoreboard.write(x[1], x[2])
                    self.iter_for_board_scroll = cycle(list(repeat(0, 10))
                                                   + [x for x in range(0, 74)]
                                                   + list(repeat(74, 10))
                                                   + [y for y in range(74, 0, -1)])
                    # Reset scroll so they can *hopefully see their name at the top of the list
            self.menu_screen.change_i(self.temp_screen, 2)

        if (time.time() - self.time) >= 7.5 and self.screen_state != 'blank8.png':
            self.message.update()
        elif self.screen_state == 'blank8.png':
            self.message.kill()
        self.ripple.update()
        if (time.time() - self.time) < 2.5 and self.state != 'Board' or\
                (time.time() - self.time) >= 2.5:
            self.last_state = deepcopy(self.state)

    def kill(self):
        for sprite in self.group:
            sprite.kill()

    def change_fade(self, direction):
        if self.state == 'Score' and direction == 'Right':
            self.screen_in_state = 'Board'
            self.screen_out_state = 'Score'
            self.count_for_fade = count(0)
        elif (time.time() - self.time) >= 2.5 and self.state == 'Board'\
                and direction == 'Left':
            self.screen_out_state = 'Board'
            self.screen_in_state = 'Score'
            self.count_for_fade = count(0, -1)
        else:
            return
        self.state = 'Changing'

    def fade_out(self):
        if not self.show_text_input:
            self.screen_out_state = 'Fade'
            self.screen_in_state = 'Fade'
            self.state = 'Changing'
            self.screen_state = 'blank8.png'
            self.count_for_fade = count(10, -1)

    def remind(self, screen):
        pass

    def ask_for_input(self):
        if self.state == 'Board' and self.show_text_input != None:
            self.show_text_input = True


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


#  `7MMF' mm
#    MM   MM
#    MM mmMMmm .gP"Ya `7MMpMMMb.pMMMb.  ,pP"Ybd
#    MM   MM  ,M'   Yb  MM    MM    MM  8I   `"
#    MM   MM  8M""""""  MM    MM    MM  `YMMMa.
#    MM   MM  YM.    ,  MM    MM    MM  L.   I8
#  .JMML. `Mbmo`Mbmmd'.JMML  JMML  JMML.M9mmmP'


class item(pygame.sprite.Sprite):
    def __init__(self, iV=None, **kwargs):
        if iV is None:
            global i
        else:
            i = iV
        global c
        super().__init__()

        self.copy_of_c = {k:v for k,v in c.__dict__.items() if k != 'items'}

        self.activate_list = {'health': c.health}  # TODO: add more + change
        for key, value in kwargs.items():
            setattr(self, str(key).lower(), value)
            # This converts all the inputted dict into variables

        if 'name' not in self.__dict__.keys():
            raise SystemExit('Name was not passed into item')
        if 'sprite' not in self.__dict__.keys():
            raise SystemExit('Sprite was not passed into item')

        if 'start_pos' in self.__dict__.keys():
            self.image = grph.spritesheet(Apj("item_sprites.png"), (*self.sprite, 12, 12))
            self.rect = self.image.get_rect()
            self.rect.topleft = self.start_pos
        else:
            self._void()

        self.time = time.time()
        self.offset = pygame.freetype.Font(Apj('8-bit Arcade In.ttf'), 12)\
            .get_rect(self.name).width
        self.scroll = cycle(list(repeat(0, 5))
                            + [a for a in range(0, self.offset)]
                            + list(repeat(self.offset, 5))
                            + [a for a in range(self.offset,
                                                0, -1)])


        if 'key_press' in self.__dict__.keys():
            self.keypress = getattr(pygame, 'K_' + self.key_press)
            return

        # ========== This will not activate some of the time ==========

        if 'effects' in self.__dict__.keys():
            for key, value in self.effects.items():
                setattr(c, str(key), value)
        if 'instants' in self.__dict__.keys():
            for key, value in self.instants.items():
                class_changing = self.activate_list[str(key)]
                class_changing += 1

    def update(self):
        if 'duration' in self.__dict__.keys() and time.time() - self.time >= self.duration:
            self.kill()
            c.items.remove(self)
        if 'key_press' in self.__dict__.keys():
            if pygame.key.get_pressed()[self.keypress]:
                if 'instants' in self.__dict__.keys():
                    for key, value in self.instants.items():
                        if key == 'restart':
                            global i
                            i = Initi(i.lvl)
                            self.kill()
                            c.items.remove(self)
                            continue
                        class_changing = self.activate_list[str(key)]
                        key_str = str(key)
                        setattr(class_changing, key_str, getattr(class_changing, key_str) + value)

    def draw(self, go_to_pos: list = [-1, -1]) -> pygame.Surface:
        if self.rect.topleft != go_to_pos and self.rect.topleft != (-1, -1):
            self.delta = list(map(minmax, (-3, -3),
                                  map(sub, go_to_pos,
                                      self.rect.topleft),
                                  (3, 3)))
            self.rect.topleft = tuple(map(add, self.delta, self.rect.topleft))
        if self.rect.topleft == go_to_pos:
            self._void()
        return (self.image, self.rect.topleft)

    def __repr__(self) -> str:
        return str(self.name)

    def __del__(self):
        global c
        # Resets c's dict to its original state, but doesn't overwrite the items value
        c.__dict__ = {k: v for k, v in c.__dict__.items() if k == 'items'}\
        | self.copy_of_c

    def _void(self):
        '''Makes the image "underrendable"'''
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (-1, -1)


class item_manager(pygame.sprite.Sprite):
    # ==Dunder/internal methods for item_manager==
    def __init__(self):
        super().__init__()
        self.item_list = []
        self.unique_items = {}
        self.other_items = []
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def __add__(self, item_to_add: item):
        self.item_list.append(item_to_add)
        self._calculate_unique_items()
        return self

    def __delitem__(self, key: str):
        '''This deletes the last object that are of the name of the key,
            it removes the last object so it doesn't mess up ordering'''
        key = [object for object in self.item_list if object.name == key.lower()][-1]
        self.item_list.remove(key)
        self._calculate_unique_items()
    
    def remove(self, to_remove):
        self.item_list.remove(to_remove)
        self._calculate_unique_items()

    def __len__(self) -> int:
        return len(self.item_list)

    def __getitem__(self, key: str) -> item:
        return [object for object in self.item_list if object.name == key.lower()][-1]

    def _len_of_unique(self) -> int:
        return len(self.unique_items)

    def len(self, key: str) -> int:
        return self.unique_items[key.lower()]

    def empty(self):
        self.item_list = []
        self.unique_items = {}
        c._health = 0
        print(self.item_list, self.unique_items, c.health, c._health)

    def _calculate_unique_items(self):
        self.unique_items = Counter([object.name for object in self.item_list])

    def card(self, item, stacking=1):
        self.surface = pygame.Surface((28, 24), flags=pygame.SRCALPHA)
        self.surface.blit(pygame.image.load(Apj("item_background.png")), (2, 0))
        for x in range(min(stacking - 1, 2), -1, -1):
            icon = grph.spritesheet(Apj("item_sprites.png"), (*item.sprite, 12, 12))
            transparency = pygame.Surface((12, 12), pygame.SRCALPHA)
            transparency.fill((255, 255, 255, (3 - x) * 43 + 96))
            icon.blit(transparency, (0, 0),
                      special_flags=pygame.BLEND_RGBA_MIN)
            darkerener = pygame.Surface((12, 12), pygame.SRCALPHA)
            darkerener.fill((x*50, x*50, x*50))
            icon.blit(darkerener, (0, 0),
                      special_flags=pygame.BLEND_RGB_SUB)
            self.surface.blit(icon, tuple(map(sub, (2, 0), (x*2, x*2))))

        grph.word_wrap(self.surface, '{:>2}'.format(stacking),
                       pygame.freetype.Font(
                Apj('manaspace.regular.ttf'), 11),
                xy=[12, 9], colour=(46, 34, 47), antialiased=False)
        self.text_surface = pygame.Surface((256, 8), flags=pygame.SRCALPHA)
        self.text_surface2 = pygame.Surface((22, 8), flags=pygame.SRCALPHA)
        scroll = next(item.scroll)
        global i
        grph.word_wrap(self.text_surface, str(item).capitalize(),
                       pygame.freetype.Font(
                Apj('8-bit Arcade In.ttf'), 18),
            xy=[2, 7], colour=(62, 53, 70), antialiased=False
            )
        self.text_surface2.blit(self.text_surface, (-1-scroll, 0))
        self.surface.blit(self.text_surface2, (3, 13))

        if "duration" in item.__dict__.keys():
            if "cumduration" not in item.__dict__.keys():
                self.cum_time = time.time()
                for num, t in enumerate([obj for obj in self.item_list if obj.name == item.name], 1):
                    t.cumduration = 'Set'
                    t.duration = jsn.items().item_val(item.name, 'duration') * num
                    t.time = self.cum_time
            self.times = [item.time, item.duration]
            self.progress_bar = pygame.image.load(Apj("progress_bar.png"))
            self.progress_surface = pygame.Surface((max(round(24 / self.times[1] * (self.times[1] - (time.time() - self.times[0]))), 0), 1))
            self.progress_surface.blit(self.progress_bar, (0, 0))
            self.surface.blit(self.progress_surface, (2, 21))

        # if "key_press" in item.__dict__.keys():
        #     self.surface.blit(grph.button_symbol('F5').image, (0, 0))

        return self.surface

    def __repr__(self) -> str:
        return 'Item container: ' + str([obj for obj in self.item_list])

    # =='Outward facing' methods==
    def cards(self):
        self.cards_surf = pygame.Surface((208, 24), flags=pygame.SRCALPHA)
        for pos, (item, amount) in enumerate(self.unique_items.items()):
            item = self.__getitem__(item)
            self.cards_surf.blit(self.card(item, amount), (pos*25, 0))
        return self.cards_surf.convert_alpha()
        # This makes blit more efficient

    def update(self):
        [object.update() for object in self.item_list]
        # Updates every item in item_list
        self.image = self.draw()

    def draw(self) -> pygame.Surface:
        self.draw_surf = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.draw_surf.blit(self.cards(), (24, 0))
        self.poses_of_cards = {key: value for key, value in zip(
                                self.unique_items.keys(),
                               [(24 + i*25, 1) for i in range(
                                   self._len_of_unique())])
                               }
        self.draw_surf.blits([obj.draw(self.poses_of_cards[obj.name]) for obj in self.item_list])
        self.draw_surf.blits([[section[0], section[1].pop()] for section in self.other_items if len(section[1]) > 0])
        self.other_items = [section for section in self.other_items if len(section[1]) > 0]
        return self.draw_surf

    def minus_of(self, sprite: list, pos: list):
        self.move_up = zip([[pos[0], [pos[1] - i for i in range(10)][0]]],
                           [int(255/9 * i) for i in range(9, -1, -1)])
        surface = grph.spritesheet(Apj("item_sprites.png"), (*sprite, 12, 12))
        self.other_items.append([surface, self.move_up])

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


# https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
class text_input:
    def __init__(self, text='', UpperLowerSentence: str = None,
                 length: int = None, disallowed_words: list = []) -> None:
        self.text = text
        self.change = UpperLowerSentence.upper()
        self.length = length
        self.disallowed_words = disallowed_words
        self.latch = i.event_sys.latch(pygame.KEYDOWN)

    def handle_events(self):
        for event in i.event_sys.retrieve(pygame.KEYDOWN):
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN and self.text.upper() not in [w.upper() for w in self.disallowed_words]:
                self.text = self.text
                return 'Entered'
            else:
                if event.unicode in string.ascii_letters:
                    self.text += event.unicode
            self.text = self.text[:self.length]

            if self.text.upper() in [w.upper() for w in self.disallowed_words]:
                return 'Error'

            if self.change == 'S':
                self.text.sentence()
            elif self.change == 'U':
                self.text.upper()
            elif self.change == 'L':
                self.text.lower()
            return None

    def return_text(self) -> str:
        return self.text


class input_box:
    def __init__(self, x, y, chr_num, *args, **kwargs) -> None:
        w = 32 + chr_num * 56 + (chr_num - 1) * 8
        # This calculates the width according to the construct 
        Xw = max((chr_num * 56 + (chr_num - 1) * 8 - 40) // 2, 0)
        # Exclusive w, all width is based off 8bit font at 16 pt
        Lw = w - 32
        self.rect = pygame.Rect(x, y, w, 9)
        self.font = pygame.freetype.Font(Apj('8-bit Arcade In.ttf'), 128)
        self.input = text_input(*args, **kwargs)
        self.font_surface = self.font.render(self.input.text)
        self.surface = pygame.Surface((w, 72), flags=pygame.SRCALPHA)
        self.surface_alert = pygame.Surface((w, 72), flags=pygame.SRCALPHA)
        self.screen = self.surface
        self.count = []
        instructions = {(0, 0): (0, 0, 16, 72), (w - 16, 0): (56, 0, 16, 72)}
        instructions = instructions | {k: v for k, v in zip(zip(count(16, 8), repeat(8, Xw//8)), repeat((72, 8, 8, 56), Xw//8))}
        # This is the left padding on text box 
        instructions = instructions | {k: v for k, v in zip(zip(count(56 + Xw, 8), repeat(8, Xw//8)), repeat((72, 8, 8, 56), Xw//8))}
        # # This the right padding on the text box
        instructions = instructions | {(16 + Xw, 8): (16, 8, 40, 8)}
        instructions = instructions | {(16 + Xw, 56): (16, 8, 40, 8)}
        # # This is the center "artwork" being added, there is the plus 3, as x coordinates starts from 0
        instructions = instructions | {(16, 16): (0, 72, min(Lw, 184), 40)}
        if Lw > 184:
            for i in range(1, (Lw - 23) // 8 + 2):
                instructions = instructions | {(2 + 23 + 8 * (i - 1), 2): (15, 9, 8, 5)}
                # Extension of type box's input box

        for z in instructions.items():
            by = 80 if z[1][1] < 72 else 0
            self.surface.blit(grph.spritesheet(Apj("text_box-sheet3.png"),
                                               z[1]), z[0])
            self.surface_alert.blit(grph.spritesheet(Apj("text_box-sheet3.png"),
                                                (z[1][0] + by, z[1][1],
                                                z[1][2], z[1][3])),
                               z[0])

    def handle_events(self):
        x = self.input.handle_events()
        if x == 'Error':
            self.screen = self.surface_alert
            self.count = [i for i in range(3)]
        elif x == 'Entered':
            global score
            return ['Entered', self.input.return_text(), score]

    def draw(self, surface):
        if len(self.count) > 0:
            self.count.pop()
            if len(self.count) <= 0:
                self.screen = self.surface
        surface.blit(self.screen, (self.rect.x, self.rect.y))
        # surface.blit(self.font.render(self.input.return_text(), False, (46, 34, 47))[0], (self.rect.x + 16, self.rect.y + 16))
        self.font.render_to(surface, (self.rect.x + 16, self.rect.y + 16), self.input.return_text(), (46, 34, 47))
        # pygame.draw.rect(surface, self.colour, self.rect)

#                               ,,
# `7MM"""YMM                  `7MM
#   MM    `7                    MM
#   MM   d    `7MMpMMMb.   ,M""bMM
#   MMmmMM      MM    MM ,AP    MM
#   MM   Y  ,   MM    MM 8MI    MM
#   MM     ,M   MM    MM `Mb    MaM
# .JMMmmmmMMM .JMML  JMML.`Wbmd"MML.


def start(screen=None):
    global i, c, score
    c = DifficultlyStats()
    
    # Music
    pygame.mixer.stop()
    pygame.mixer.Sound(os.path.join("Assets","Sounds","Main-sound.mp3")).play(loops = -1).set_volume(0.05)

    i = Initi(screen=screen)
    score = 0
    main()


class events_sync:
    """
    Allows for pygame to be handled at the same time
    and with coordination; otherwise every system
    who wanted to listen for a particular event
    would be stepping on each other toes and the
    events may be taken from the queue accidentally
    and interfere with other systems
    """    
    def __init__(self) -> None:
        """Sets up events_sync program
        """        
        self.register = {}
        for i in ['Active', 'Paused', 'Died', 'Won']:
            self.register[i] = []
        self.latch_register = {}

    def __call__(self):
        """
        Goes through each event in the queue
        and does appropriate actions
        """
        global i
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quits game if 'X" is pressed in game window
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Allows for fullscreen
                pygame.display.toggle_fullscreen()
            for x in self.register[i.gm]:
                # Goes through every action in the register and if the action
                # matches with the selected event type
                k = list(x.keys())[0]
                v = tuple(x.values())[0]
                if event.type == k[0] and len(k) < 2:
                    v[0](*v[1], **v[2])
                elif event.type == k[0] and event.key == k[1] and len(k) == 2:
                    v[0](*v[1], **v[2])
            if event.type in self.latch_register.keys():
                self.latch_register[event.type].append(event)

    def listen(self, gm: str, event: int, action, key: int = None, *args, **kwargs):
        """Allows for an action to be performed when the associated event occurs
        if passed the listen function can also listen for specific keys, it
        also allows for args or kwargs to be passed into the action

        Parameters
        ----------
        gm : str
            At what game mode should the action trigger
        event : int
            The pygame event that should be listened too
        action : [type]
            The function that should be called when the event occurs
        key : int, optional
            If the event is a keyboard event, so on what key should
            the event occur, by default None
        """
        if key is None:
            self.register[gm].append({(event): (action, args, kwargs)})
        else:
            self.register[gm].append({(event, key): (action, args, kwargs)})

    def latch(self, event: int):
        """This allows for events to be listened too and recorded
        when events are heard, the occurrence is noted in latch
        register for the respective event and can be retrieved at anytime

        Parameters
        ----------
        event : int
            The pygame event that should be listened for
        """
        self.latch_register[event] = []

    def retrieve(self, event: int):
        """Retrieves all the events stored in the register from the requested
        event type, this function is designed to be called frequently (most
        likely once per tick) so it unlikely to have multiple events in the
        register

        Parameters
        ----------
        event : int
            The pygame event that should be retrieved

        Returns
        -------
        list
            All the events that occurred in the registers
        """
        r = self.latch_register[event]
        self.latch_register[event] = []
        return r

    def __delattr__(self, key: str) -> None:
        self.register = {k: v for k, v in self.register.items()}


if __name__ == '__main__':
    icon = pygame.image.load(os.path.join("Assets", "dodger_icon.png"))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Sushi Dodger")
    pygame.mixer.init()
    screen = pygame.display.set_mode((256, 256), flags=pygame.RESIZABLE
                                     | pygame.SCALED)
    start(screen)
