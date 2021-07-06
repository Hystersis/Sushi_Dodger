import pygame
import os
from operator import sub, add, mul
from itertools import cycle
import math


class missile(pygame.sprite.Sprite):
    def __init__(self, start_pos, orientation: int):
        super().__init__()
        self.orientation = orientation
        self.orientate()
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.burst = cycle([int(roundd(x / 12)) for x in range(1, 13)])

    def update(self, ddger):
        self.delta = list(map(sign,
                              list(map(sub, ddger.rect.center,
                                       self.rect.center))))
        self.rect.topleft = tuple(map(add, self.delta, self.rect.topleft))
        if next(self.burst) == 1:
            self.rect.topleft = tuple(map(add, map(mul, self.delta, [9,9]), self.rect.topleft))
        if 0 in self.delta:
            self.orientation = (lambda x, y: (x*2 if x == abs(x) else 6)
                                + (0 if y == abs(y) else 4))(*self.delta)
        else:
            self.orientation = (lambda x, y: abs((-6 if x != abs(x) else 2)
                                - y))(*self.delta)
        self.orientate()

    def orientate(self):
        '''Orientates the missile to be faces the 'right' direction
        in 90° incraments'''
        # Orintation is 0 for facing bottom
        # Orientation is 1 for facing left-bottom (45o)
        if self.orientation % 2 == 0:
            self.image = pygame.image.load(os.path.join('Assets', 'missile.png'))
        else:
            # Rotated sprite
            self.image = pygame.image.load(os.path.join('Assets', 'missile_rot.png'))
        self.image = pygame.transform.rotate(self.image, self.orientation // 2 * 90)


class laser_enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        pass


def sign(num: int, amount: int = 1) -> int:
    '''Function that takes an interger and return an absolute positive, negative or null value; the positive and negative values
    equalling the amount (default 1).'''
    if num > 0:
        return amount
    elif num == 0:
        return 0
    else:
        return -amount


# From https://realpython.com/python-rounding/#rounding-down
def roundd(num, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(num * multiplier) / multiplier
