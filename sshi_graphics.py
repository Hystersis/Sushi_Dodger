# Graphics for Game
import pygame
import sshi_msci as msci
import numpy as np
import os
from pygame.freetype import Font
from itertools import repeat
from PIL import Image, ImageFilter
import random
import sshi_score as sce


class Flag:
    flags = {}

    def add(self, flagN):
        flag = pygame.sprite.Group()
        Flag.flags[flagN] = flag
        return flag

    @classmethod
    def create(cls, flag):
        if flag not in Flag.flags:
            f = cls().add(flag)
            return f
        else:
            return Flag.flags[flag]


class add:
    def __init__(self, flag, func, *args, **kwargs):
        self.flag = Flag.create(flag)
        self.f = func(*args, **kwargs)
        self.flag.add(self.f)

    def kill(self):
        self.f.kill()

    @staticmethod
    def update(flagN):
        screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        flag = Flag.create(flagN)
        flag.draw(screen)
        return screen

    @staticmethod
    def clear(flag):
        flag = flag.create(flag)
        flag.clear()


# class Leaf(pygame.sprite.Sprite):
#     shapes = [[[1, 0],
#                [1, 1]],
#               [[1, 1],
#                [1, 0]],
#               [[1, 1],
#                [0, 1]],
#               [[0, 1],
#                [1, 1]]]
#
#     def __init__(self, pos):
#         self.pos = pos
#         self.ranSH = random.randint(0, 5)
#         for x in Leaf.shapes
#     def


class Blur:
    '''Allows for blurring of screen'''
    def __init__(self, blur_amount):
        super().__init__()
        self.bAmt = blur_amount

    def __call__(self, surface):
        surf = pygame.image.tostring(surface, 'RGBA')
        blurred = Image.frombytes('RGBA', surface.get_size(), surf).filter(ImageFilter.GaussianBlur(radius=5))
        surf = pygame.image.fromstring(blurred.tobytes('raw', 'RGBA'), surface.get_size(), 'RGBA')
        return surf


class Prtcl(pygame.sprite.Sprite):
    '''Classic Prtcl, just ment to display something on a certain layer'''
    def __init__(self, pos, imge):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class MvPrtcl(pygame.sprite.Sprite):
    def __init__(self, strt, end, imge):
        super().__init__()
        self.path = msci.pthfnd(np.zeros(256, 256), *strt, *end)
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.path.pop(0)

    def update(self):
        if len(self.path) > 0:
            self.rect.topleft = self.path.pop(0)


class Background(pygame.sprite.Sprite):
    def __init__(self, bck_pth):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", bck_pth))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class FadeMove(pygame.sprite.Sprite):
    def __inti__(self, strt, end, imge):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.surface = pygame.Surface((self.image.get_width(),
                                      self.image.get_width()))
        self.path = msci.pthfnd(np.zeros(256, 256), *strt, *end)
        self.fade = iter([x for x in range(255, -1, -(255 / len(self.path)))])
        # This creates an iterator of the transparency values; it starts at 0
        # and incriments up to 255, by the len of self.path
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.path.pop(0)
        self.surface.set_alpha(next(self.fade))

    def update(self):
        if len(self.path) > 0:
            self.rect.topleft = self.path.pop()
            self.surface.set_alpha(next(self.fade))


class Transition(pygame.sprite.Sprite):
    def __init__(self, imge, score, custom_txt='Score'):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = (14, 0)
        self.text = custom_txt + ' ' + str(score)
        # word_wrap(self.image, self.text, Font(
        #         os.path.join("Assets/", '8-bit Arcade In.ttf'), 48),
        #         colour=(200, 200, 201), xy=(128, 84))
        # word_wrap(self.image, self.text, Font(
        #         os.path.join("Assets/", '8-bit Arcade Out.ttf'), 48),
        #         xy=(128, 84))

    def __repr__(self):
        return 'Transition Class'


def word_wrap(surf, text, font, colour=(255, 255, 255), xy=(0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    if xy == 'center':
        rect_b = font.get_rect(text)
        xy = [0, 0]
        xy[0] = (width - rect_b.width) // 2
        xy[1] = int((height + font.get_sized_height() - rect_b.height) / 2)
    line_spacing = font.get_sized_height() + 2
    x, y = 0 + xy[0], line_spacing - 14 + xy[1]
    space = font.get_rect(' ')
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width:
            x, y = 0, y + line_spacing
        if x + bounds.width + bounds.x >= width:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= height:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x, y), None, colour)
        x += bounds.width + space.width
    return x, y


class scoreboard(pygame.sprite.Sprite):
    def __init__(self, pos, i):
        super().__init__()
        # self.image = pygame.image.load(os.path.join("Assets",
        #                                             "scoreboard.png"))
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        for rank, ns in enumerate(i.board.get()):
            self.text = f'{rank} {ns[0]} {ns[1]}'
            word_wrap(self.image, self.text, Font(
                    os.path.join("Assets/", '8-bit Arcade In.ttf'), 48),
                    xy=(50, 52 + (16 * rank)), colour=(0, 0, 0))


class ripple(pygame.sprite.Sprite):
    def __init__(self, Glength, Gtransparency):
        super().__init__()
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (77, 101, 180, Gtransparency), (128, 128), Glength, width=2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


if __name__ == '__main__':
    Flag.create('screenHigh')
    Flag.create('screenLow')
    Flag.create('screenEffects')
    Flag.create('all')
