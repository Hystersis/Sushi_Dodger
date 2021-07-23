import pygame
import os
from operator import sub, add, mul
from itertools import repeat, cycle
import math
import random

from pygame import surface
from sshi_msci import Apj
import time


def sign(num: int, amount: int = 1) -> int:
    '''Function that takes an interger and return an absolute positive, negative or null value; the positive and negative values
    equalling the amount (default 1).'''
    if num > 0:
        return amount
    elif num == 0:
        return 0
    else:
        return -amount


class missile(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple, orientation: int):
        super().__init__()
        self.colours = [(174, 35, 52), (232, 59, 59), (249, 194, 43)]
        self.time = time.time()
        self.orientation = orientation
        self.orientate(self.orientation)
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.rect2 = self.missile.get_rect()
        self.rect2.topleft = start_pos
        self.acceleration = 1
        self.dirnx = 0
        self.dirny = 0
        self.particles = []
        self.life_span = 1
        self._hit = True
        self.last_dist = math.inf

    def update(self, ddger, sshiG: pygame.sprite.Group):
        self.image.fill((0, 0, 0, 0))
        # https://gamedev.stackexchange.com/questions/17313/how-does-one-prevent-homing-missiles-from-orbiting-their-targets
        delta = tuple(map(sub, self.rect2.topleft, ddger.rect.topleft))

        # This returns the backside coords of the craft
        self.backside = list(map(add, self.rect2.center,
                                  tuple(map(sub, (0, 0), map(sign, delta)))
                                  * (self.rect2.size[0] // 2)))

        self.particles.append([self.backside, [random.gauss(0, 0.6), sign(self.rect2.center[1] - self.backside[1]) * 2], random.uniform(3, 4)])
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.1
            colour = [a + b + c for a, b, c in zip(map(mul, self.colours[0], repeat(sinsq(min(p[2], 2), 4, 2))),
                        map(mul, self.colours[1], repeat(sinsq(p[2], 4))),
                        map(mul, self.colours[2], repeat(sinsq(max(p[2], 2), 4, 2))))]
            if self._hit:
                pygame.draw.circle(self.image, colour, tuple(map(int, p[0])), int(p[2]))
        self.particles = [p for p in self.particles if p[2] > 0]

        if self._hit:
            d = math.sqrt(delta[0] ** 2 + delta[1] ** 2)  # Pythagoras for distance
            a = self.acceleration
            s = math.sqrt(sum(map(self.calspeed, delta, self.rect2.topleft,
                                  ddger.rect.topleft, (ddger.dirnx, ddger.dirny))))
            # Speed in a quadratic sense with Pythagoras, so in an 2d plane
            esttime = (math.sqrt(s**2 + 2 * a * d) - s) / a
            estpos = (ddger.rect.topleft[0] + ddger.dirnx * esttime,
                    ddger.rect.topleft[1] + ddger.dirny * esttime)
            accel = tuple(map(self.expsign, map(sub, estpos, self.rect2.topleft)))
            self.dirnx += accel[0]
            self.dirny += accel[1]

            NSdelta = sign(accel[1]) + 2

            if sign(accel[0]) == -1:
                NSdelta = abs(NSdelta - 8)
            elif sign(accel[0]) == 0:
                NSdelta = (NSdelta - 1) * 2
            self.orientate(NSdelta)

            self.rect2.topleft = tuple(map(minmax, (0, 0), tuple(map(add, (self.dirnx, self.dirny), self.rect2.topleft)), (239, 239)))
            self.image.blit(self.missile, self.rect2.topleft)

            if esttime <= 3 and esttime >= self.last_dist or (time.time() - self.time) > 7:
                self.do_hit(ddger, sshiG)
                self._hit = False
            self.last_dist = esttime

    def orientate(self, orientation):
        """Orientates the missile in one of eight orientates as listed below
        also adds a fill effect to show how long until it self destructs

        Parameters
        ----------
        orientation : int
            Orientates the missile in 45o increments - 0 is facing bottom left
                 up
            +---+---+---+
            | 5 | 4 | 3 |
            +---+---+---+
       left | 6 |N/A| 2 | right
            +---+---+---+
            | 7 | 0 | 1 |
            +---+---+---+
                down
        """
        # Orintation is 0 for facing bottom
        # Orientation is 1 for facing left-bottom (45o)
        colour = *self.colours[0], 255
        if orientation % 2 == 0:
            self.missile = pygame.image.load(os.path.join('Assets', 'missile.png'))
        else:
            # Rotated sprite
            self.missile = pygame.image.load(os.path.join('Assets', 'missile_rot.png'))
        durview = pygame.Surface((16, 16))
        durview.fill(colour)
        print(durview)
        p16 = int((7 - (time.time() - self.time)) / 0.4375)
        self.missile = pygame.transform.rotate(self.missile, orientation // 2 * 90)
        self.missile.blit(durview, (0, p16), special_flags=pygame.BLEND_RGBA_MULT)

    def do_hit(self, ddger, sshiG):
        if self._hit:
            hit_surface = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
            pygame.draw.circle(hit_surface, (0, 0, 0), self.rect2.center, 30)
            mask = pygame.mask.from_surface(hit_surface)
            for sprite in sshiG:
                hit = mask.overlap(pygame.mask.from_surface(sprite.image),
                                sprite.rect.topleft)
                if type(hit) is tuple:
                    sprite.killed()
            hit = mask.overlap(pygame.mask.from_surface(ddger.image),
                            ddger.rect.topleft)
            if type(hit) is tuple:
                ddger.killed()
            self.particles.append([list(self.rect2.center), [0, 0], 20])

    def calspeed(self, delta: tuple, sxy: tuple, dxy: tuple, dirn: tuple):
        """Calculates the speed that the ddger is travelling at relative to the missile

        Parameters
        ----------
        delta : tuple | list
            This is the delta calculated earlier
        sxy : tuple | list
            self xy - the x or y coordinate of the missile
        dxy : tuple | list
            ddger xy - the x or y coordinate of the ddger
        dirn : tuple | list
            ddger's dirn(x/y) - its movement in different direction

        Returns
        -------
        float
            Returns number that will be put into a quadratic equation later,
            so this the reason there is the square
        """
        return (abs(delta) - abs(sxy - (dxy + dirn)))**2

    def expsign(self, val: int):
        """Returns a value between 0 and 1

        Parameters
        ----------
        val : int
            The starting value should be an int

        Returns
        -------
        float | int
            A value that gets smaller the closer to zero and it cannot be
            bigger than 1
        """
        return min(val / 64, 1)


class laser_enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple):
        super().__init__()
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.ship = pygame.image.load(Apj("ship.png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.rect2 = self.ship.get_rect()
        self.charge_cycle = cycle(range(18))

    def update(self, ddger, sshiG: pygame.sprite.Group):
        Sdelta = tuple(map(sign, delta))
        # This returns the backside coords of the craft
        self.backside = tuple(map(add, self.rect.center,
                                  tuple(map(sub, (0, 0), Sdelta))
                                  * (self.rect.size[0] // 2)))
        # Mapping of cycle:
        # 0 - reset everything
        # 1-10 charge laser
        # 11-14 fire laser:
        #    11 show outline
        #    12 make outline bigger
        #    13 calculate hits
        #    14 leave remanent of laser blast
        # 15-17 cooldown
        n = next(self.charge_cycle)
        if n >= 1 and n < 11:
            # -----Charge of laser-----
            pygame.draw.circle(self.image, tuple(map(add,
                                                     map(mul,
                                                         (255, 255, 255, 150),
                                                         repeat(1 / 10 * (11 - n))),
                                                      map(mul,
                                                          (77, 155, 230, 245),
                                                          repeat(1 / 10 * n)))), 
                               self.backside)
        elif n >= 11 and n < 15:
            # -----Firing of laser-----
            pygame.draw.line()


# From https://realpython.com/python-rounding/#rounding-down
def roundd(num, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(num * multiplier) / multiplier


def roundu(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def sinsq(n: float, width: int, deviation=0) -> float:
    return math.sin((n+deviation) / (width / math.pi))**2


def minmax(a, b, c):
    '''This function returns the middle variable between the min variable
    and the max variable.'''
    return (lambda x: sorted(x)[1])([a, b, c])
