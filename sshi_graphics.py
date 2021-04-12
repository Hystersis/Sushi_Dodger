# Graphics for Game
import random
import pygame
import sshi_msci as msci
import numpy as np
import os
import itertools

class Flag:
    flags = []
    def add(self,flag):
        flag = pygame.sprite.Group()
        Flag.flags.append(flag)
        return flag
    @classmethod
    def create(cls,flag):
        if flag not in Flag.flags:
            f = cls.add(flag)
            return f
        else:
            return flag

Flag.create('screenHigh')
Flag.create('screenLow')
Flag.create('all')

class add:
    def __init__(self,flag,func,*args,**kwargs):
        self.flag = Flag.create(flag)
        self.f = func(*args,**kwargs)
        self.flag.add(self.f)

    def kill(self):
        self.f.kill()
    @staticmethod
    def update(flag):
        screen = pygame.Surface((256,256))
        flag = flag.create(flag)
        flag.draw(screen)
        return screen
    @staticmethod
    def clear(flag):
        flag = flag.create(flag)
        flag.clear()



class MvPrtcl(pygame.sprite.Sprite):
    def __init__(self,strt,end,imge):
        self.path = msci.pthfnd(np.zeros(256,256),*strt,*end)
        self.image = pygame.image.load(os.path.join("Assets",imge))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.path.pop(0)
    def update(self):
        if len(self.path) > 0:
            self.rect.topleft = self.path.pop(0)

class Background(pygame.sprite.Sprite):
    def __init__(self,bck_pth):
        self.background = pygame.image.load(os.path.join("Assets",bck_pth))

class FadeMove(pygame.sprite.Sprite):
    def __inti__(self,strt,end,imge):
        self.image = pygame.image.load(os.path.join("Assets",imge))
        self.surface = pygame.Surface((self.image.get_width(),self.image.get_width()))
        self.path = msci.pthfnd(np.zeros(256,256),*strt,*end)
        self.fade = iter([x for x in range(255, -1, -(255 / len(self.path)))]) #This creates an iterator of the transparency values; it starts at 0 and incriments up to 255, by the len of self.path
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.path.pop(0)
        self.surface.set_alpha(next(self.fade))
    def update(self):
        if len(self.path) > 0:
            self.rect.topleft = self.path.pop()
            self.surface.set_alpha(next(self.fade))

class Transition(pygame.sprite.Sprite):
    def __init__(self,imge,score,custom_txt = 'Score'):
        self.image = pygame.image.load(os.path.join("Assets",imge))
        self.rect = self.imge.get_rect()
        self.text = custom_txt + score
        word_wrap(self.image,self.text,pygame.freeetype.Font(os.path.join("Assets/",'8-bit Arcade Out.ttf'),48),colour=(200,200,201),xy = (84,128))
        word_wrap(self.image,self.text,pygame.freeetype.Font(os.path.join("Assets/",'8-bit Arcade In.ttf'),48),xy = (84,128))

def word_wrap(surf, text, font, colour=(255, 255, 255),xy=(0,0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
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

if __name__ == '__main__':
    screenHigh = pygame.sprite.Group()
    screenLow = pygame.sprite.Group()
