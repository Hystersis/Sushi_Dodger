# Graphics for Game
import pygame
import sshi_msci as msci
import numpy as np
import os
from pygame.freetype import Font
from PIL import Image, ImageFilter
from abc import ABC, abstractmethod


class G(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass


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


class Prtcl(pygame.sprite.Sprite, G):
    '''Classic Prtcl, just ment to display something on a certain layer'''
    def __init__(self, pos, imge):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class MvPrtcl(pygame.sprite.Sprite, G):
    def __init__(self, strt, end, imge):
        super().__init__()
        self.path = msci.pthfnd(np.zeros(256, 256), *strt, *end)
        self.image = pygame.image.load(os.path.join("Assets", imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.path.pop(0)

    def update(self):
        if len(self.path) > 0:
            self.rect.topleft = self.path.pop(0)


class Background(pygame.sprite.Sprite, G):
    def __init__(self, bck_pth):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", bck_pth))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class FadeMove(pygame.sprite.Sprite, G):
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


class Transition(pygame.sprite.Sprite, G):
    def __init__(self, score, custom_txt='Score'):
        super().__init__()
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


def word_wrap(surf, text, font, colour=(255, 255, 255), xy=[0, 0]):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    txt_bounds = font.get_rect(text)
    if xy[0] == 'center':
        xy[0] = 0
        xy[0] = width // 2 - txt_bounds.width // 2 
    elif xy[1] == 'center':
        xy[1] = 0
        xy[1] = height // 2 + (txt_bounds.height + 2) // 2  
    elif xy == 'center':
        xy = [0, 0]
        xy[0] = width // 2 - txt_bounds.width // 2
        xy[1] = height // 2 + (txt_bounds.height + 2) // 2
    # match xy:
    #         case [x,y]:
    #             return [x, y]
            
    #         case ['center', y]:
    #             xy[0] = 0
    #             xy[0] = width // 2 - txt_bounds.width // 2
    #             return [x, y]
            
    #         case [x, 'center']:
    #             xy[1] = 0
    #             xy[1] = height // 2 - (txt_bounds.height // 2)
    #             return [x, y]

    #         case 'center':
    #             xy = [0, 0]
    #             xy[0] = width // 2 - txt_bounds.width // 2
    #             xy[1] = height // 2 - (txt_bounds.height // 2)
    #             return [x, y]
    
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
    return xy


class scoreboard(pygame.sprite.Sprite, G):
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


class ripple(pygame.sprite.Sprite, G):
    def __init__(self):
        self.transparency = self.Transparency(64)
        self.length = self.Length(64)
        super().__init__()
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def Transparency(self, length):
        while True:
            for i in range(length):
                yield (255 // length) * (length - i)

    def Length(self, length):
        while True:
            for i in range(length):
                yield (128 // length) * i

    def update(self):
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (77, 101, 180,
                                        next(self.transparency)), (128, 128),
                           next(self.length), width=2)
