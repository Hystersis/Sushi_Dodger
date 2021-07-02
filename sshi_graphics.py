# Graphics for Game
import pygame
from sshi_msci import Apj
import numpy as np
import os
from pygame.freetype import Font
from PIL import Image, ImageFilter
from abc import ABC, abstractmethod
from itertools import count, cycle


class G(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass


class able_to_lock_in_menu(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_size(self):
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


def word_wrap(surf, text, font, colour=(255, 255, 255), xy=[0, 0], antialiased=True):
    font.origin = True
    font.antialiased = antialiased
    words = text.split(' ')
    width, height = surf.get_size()
    txt_bounds = font.get_rect(text)

    if xy[0] == 'center':
        xy[0] = 0
        xy[0] = width // 2 - txt_bounds.width // 2
    elif xy[1] == 'center':
        xy[1] = 0
        xy[1] = height // 2 - (txt_bounds.height // 2 - 128 // height)
    elif xy == 'center':
        xy = [0, 0]
        xy[0] = width // 2 - txt_bounds.width // 2
        xy[1] = height // 2 + (txt_bounds.height + 2) // 2

    line_spacing = font.get_sized_height() + 2
    if txt_bounds.height >= 14:
        x, y = 0 + xy[0], line_spacing - 14 + xy[1]
    else:
        x, y = 0 + xy[0], 0 + xy[1]
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


class message_box(pygame.sprite.Sprite, G):
    def __init__(self, text, colour, wh: list = [256, 16], xy: list = [0, 240],
                 locking_object: able_to_lock_in_menu = None, *args, **kwargs):
        super().__init__()
        self.text = text
        self.colour = colour
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self._xy = xy
        self.offset_from_left = 0
        self.font_size = max(wh[1] // 16, 1) * 12
        if locking_object is not None:
            self.locking_object = locking_object
            print(tuple(locking_object.get_size().values()))
            self.mask = pygame.mask.Mask(size=tuple(locking_object.get_size()
                                                    .values()))
            self.mask_pos = self.locking_object._xy
            self.offset_from_left = locking_object.get_size()['width']
            self.group = pygame.sprite.Group(self.locking_object)
        self.offset_font_based = Font(Apj('manaspace.regular.ttf'), self.font_size)\
            .get_rect(self.text).width
        self.text_surface = pygame.Surface((max(256, self.offset_font_based) - (256 - wh[0]) - self.offset_from_left, wh[1]),
                                           flags=pygame.SRCALPHA)
        if Font(Apj('manaspace.regular.ttf'), self.font_size).get_rect(self.text).width \
                > 256 - self.offset_from_left:
            # This means that font is bigger than the surface
            self.scroll = self.offset_font_based - (256 - self.offset_from_left)
            self.scroll = cycle([a for a in range(0, self.scroll + 3, wh[1] // 16)]
                                + [a for a in range(self.scroll + 3,
                                                    0, -wh[1] // 16)])

    def update(self, text=None, xy=None):
        self.image.fill((0, 0, 0, 0))
        self.text_surface.fill(self.colour)  # Makes it blank
        word_wrap(self.text_surface, self.text, Font(
                  Apj('manaspace.regular.ttf'), self.font_size),
                  xy=[self.offset_from_left, 'center'])
        if text is not None:
            self.text = text
        if 'scroll' in self.__dict__.keys():
            self.image.blit(self.text_surface, (self._xy[0]-next(self.scroll), self._xy[1]))
        else:
            self.image.blit(self.text_surface, self._xy)

        if 'locking_object' in self.__dict__.keys():
            self.locking_object.update()
            self.mask.to_surface(self.image, unsetcolor=self.colour, dest=self.mask_pos)
            self.group.draw(self.image)


class button_symbol(pygame.sprite.Sprite, able_to_lock_in_menu):
    def __init__(self, letter: str, colour: tuple = (199, 220, 208),
                 xy: list = [150, 150], click_action = None):
        super().__init__()
        self.image = pygame.image.load(Apj('button.png'))
        print(colour)
        self.image.fill(colour, special_flags=pygame.BLEND_MAX)
        print(self.image)
        self.letter = letter[0]
        self.letter_surface = pygame.surface.Surface((32, 32),
                                                     flags=pygame.SRCALPHA)
        word_wrap(self.letter_surface, self.letter, Font(
                  Apj('8-bit Arcade In.ttf'), 32),
                  xy=[9, 11], colour=(0, 0, 0))
        self.letter_mask = pygame.mask.from_surface(self.letter_surface)
        self.letter_mask.to_surface(self.image, unsetsurface=self.image,
                                    setcolor=(0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self._xy = xy
        if click_action is not None:
            self.click_action = click_action

    def get_size(self):
        return {'width': self.rect.width, 'height': self.rect.height}

    def bounce(self, above_pos, dampening=0.8):
        '''This should only be called once for each bounce'''
        self.y0 = above_pos
        self.v0 = -1
        self.g = 1
        self.dampening = dampening
        self.rect.topleft = (self.rect.topleft[0],
                             self.rect.topleft[1] - above_pos)
        self.t = count(1, step=0.5)
        print(self._xy)
        self.bouncing_object = True

    def update(self):
        if 'bouncing_object' in self.__dict__.keys():
            self.current_t = next(self.t)
            if self.rect.topleft[1] < self._xy[1] or self._flip is True:
                self.rect.topleft = (self.rect.topleft[0], self._xy[1]
                                     - (self.y0 + self.v0*self.current_t
                                     + 0.5 * -1 * self.current_t**2))
                print(self.rect.topleft[1])
                self._flip = False
            else:
                self._impact()
        if 'click_action' in self.__dict__.keys():
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.topleft[0] <= mouse_pos[0] <= self.rect.bottomright[0] and self.rect.topleft[1] <= mouse_pos[1] <= self.rect.bottomright[1]:
                print(mouse_pos)
                for event in pygame.event.get():
                    print(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__['button'] == 1:
                        self.click_action()

    def _impact(self):
        self.t = count(1, step=0.5)
        self.v0 *= self.dampening
        self.y0 *= self.dampening
        self._flip = True


def spritesheet(imge, rect):
    """In rect argument the (x,y,w,h)
    so x,y equal the position of the sprite in the sheet by topleft
    the w,h correspond to the width,height of the sprites in the sheet."""
    rect = pygame.Rect(rect)
    image = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
    image.blit(pygame.image.load(imge), (0, 0), rect)
    return image


def test():
    print('clicked')
