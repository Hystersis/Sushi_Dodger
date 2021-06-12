import pygame
import os
from operator import sub, add


class missile(pygame.sprite.Sprite):
    def __init__(self, start_pos, orientation: int):
        super().__init__()
        self.orientation = orientation
        self.orientate()
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos

    def update(self, ddger):
        self.delta = list(map(sign,
                              list(map(sub, ddger.rect.center,
                                       self.rect.center))))
        self.rect.topleft = tuple(map(add, self.delta, self.rect.topleft))
        if 0 in self.delta:
            self.orientation = (lambda x, y: (0 if x == abs(x) else 4)
                                + (2 if y == abs(y) else 6))(*self.delta)
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


def sign(num: int) -> int:
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1
