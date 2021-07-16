import pygame
import os
from operator import sub, add, mul
from itertools import repeat, cycle
import math
import random
from sshi_msci import Apj


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
        print(self, start_pos, orientation)
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
        self.colours = [(174, 35, 52), (232, 59, 59), (249, 194, 43)]

    def update(self, ddger, sshiG: pygame.sprite.Group):
        self.image.fill((0, 0, 0, 0))
        # https://gamedev.stackexchange.com/questions/17313/how-does-one-prevent-homing-missiles-from-orbiting-their-targets
        delta = tuple(map(sub, self.rect2.topleft, ddger.rect.topleft))

        Sdelta = tuple(map(sign, delta))
        NSdelta = Sdelta[0] + 2

        if Sdelta[0] == -1:
            NSdelta = abs(NSdelta - 8)
        elif Sdelta[0] == 0:
            NSdelta = (NSdelta - 1) * 2
        self.orientate(NSdelta)

        # This returns the backside coords of the craft
        self.backside = list(map(add, self.rect.center,
                                  tuple(map(sub, (0, 0), Sdelta))
                                  * (self.rect.size[0] // 2)))

        self.particles.append([self.backside, [random.gauss(0, 0.6), -2], random.uniform(3, 4)])
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.15
            colour = [a + b + c for a, b, c in zip(map(mul, self.colours[0], repeat(sinsq(min(p[2], 2), 4, 2))),
                        map(mul, self.colours[1], repeat(sinsq(p[2], 4))),
                        map(mul, self.colours[2], repeat(sinsq(max(p[2], 2), 4, 2))))]
            pygame.draw.circle(self.image, colour, tuple(map(int, p[0])), int(p[2]))
        self.particles = [p for p in self.particles if p[2] > 0]

        d = math.sqrt(delta[0] ** 2 + delta[1] ** 2)  # Pythagoras for distance
        a = self.acceleration
        s = math.sqrt((max(self.rect2.topleft[0] - (ddger.rect.topleft[0] + ddger.dirnx), 0) ** 2)
                      + (max(self.rect2.topleft[1] - (ddger.rect.topleft[1] + ddger.dirny), 0) ** 2))
        # Speed in a quadratic sense with Pythagoras, so in an 2d plane
        esttime = (math.sqrt(s**2 + 2 * a * d) - s) / a
        estpos = (ddger.rect.topleft[0] + ddger.dirnx * esttime,
                  ddger.rect.topleft[1] + ddger.dirny * esttime)
        accel = tuple(map(sign, map(sub, ddger.rect.topleft, estpos)))
        self.rect2.topleft = tuple(map(add, accel, self.rect2.topleft))
        self.image.blit(self.missile, self.rect2.topleft)

    def orientate(self, orientation):
        '''Orientates the missile to be faces the 'right' direction
        in 90° incraments'''
        # Orintation is 0 for facing bottom
        # Orientation is 1 for facing left-bottom (45o)
        if orientation % 2 == 0:
            self.missile = pygame.image.load(os.path.join('Assets', 'missile.png'))
        else:
            # Rotated sprite
            self.missile = pygame.image.load(os.path.join('Assets', 'missile_rot.png'))
        self.missile = pygame.transform.rotate(self.missile, self.orientation // 2 * 90)

    def do_hit(self, ddger):
        self.a = None


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
