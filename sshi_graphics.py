# Graphics for Game
import random
import pygame
import sshi_msci as msci
import numpy as np
import os

global maze, updateg, litr

pygame.freetype.init(resolution=48)

litr = {'Active' : None,
        'Paused' : None,
        'Died' : "defeat_screen.png",
        'Won' : None} # Code must be added here in the future to list the .png for 'Won'
data = {}
updateg = pygame.sprite.Group()

class mv_prtcl(pygame.sprite.Sprite):
    def __init__(self,**kwags):
        self.path = msci.pthfnd(np.zeros((256,256)),kwags['strt'][0],kwags['strt'][1],kwags['end'][0],kwags['end'][1])
        self.image = pygame.image.load(os.path.join("Assets/",kwags['imge']))
        self.rect = self.image.get_rect()
        self.rect.topleft = kwags['strt']
        # add any animations for start here
    def update(self):
        if len(self.path) < 1:
            # Add any animations for end here
            self.kill()
        else:
            self.rect.topleft = self.path.pop(0)

class transition(pygame.sprite.Sprite):
    """tr is transition"""
    count = 0
    def __init__(self):
        self.image = None
        transition.count += 1
        if transition.count > 1:
            raise ValueError('The amount of transition is over threshold.') from None
    def update(self,image,score):
        self.image = pygame.image.load(os.path.join("Assets/",image)) if image != None else None
        self.rect = self.image.get_rect() if image != None else None
        self.text = text_eight(screenHigh.screen,(f'Score {data["score"]}'),(84,128)) if image != None else None
    def draw(self):
        return self.image

class fademove(pygame.sprite.Sprite):
    def __init__(self,**kwags):
        for k, v in kwags.iteritems():
            setattr(self, k, v)
        self.image = pygame.image.load(self.image)
        self.move_x = iter(self.strtc[0] - self.endc[0])
        self.move_y = iter(self.strtc[1] - self.endc[1])
        self.rect = self.image.get_rect()
        self.move = max(map(lambda s,e: s-e, self.strtc,self.endc))
        self.fade = iter([x for x in range(255,-1, -(255 // self.move))])
        self.surface = pygame.Suface(self.image.get_rect().size)
        # self.image = pygame.image.load(kwags['image'])
        # self.strt_c = kwags['strtc']
        # self.end_c = kwags['endc']
        # self.move_x = iter(kwags['strtc'][0] - kwags['endc'][0])
        # self.move_y = iter(kwags['strtc'][1] - kwags['endc'][1])
        # self.rect = self.ime.get_rect()
        # self.rect.topleft = kwags['strtc']
        # self.move = max(kwags['strtc'][0] - kwags['endc'][0],kwags['strtc'][1] - kwags['endc'][1])
        # self.fade = iter([x for x in range(255,-1, -(255 // self.move))])
        # self.surface = pygame.Suface(self.image.get_rect().size)
    def update(self):
        if (c := next(self.move_x, 0)) != 0:
            self.rect.topleft[0] - c
        if (c := next(self.move_y, 0)) != 0:
            self.rect.topleft[1] - c
        if (c := next(self.fade, None)) != None:
            self.surface.set_alpha(c)
        self.image = self.surface


def screenLow(screen):
    screen = screen.copy()
    return screen

def screenHigh(screen,gm):
    screenHigh.screen = screen.copy()
    updateg.update()
    updateg.draw(screenHigh.screen)
    screenHigh.screen.blit(tr.draw(),[42,0]) if tr.draw() != None else None
    # tr.update(litr[gm],data['score']) # Remeber to change this back to litr[gm]
    return screenHigh.screen

class text_eight(pygame.sprite.Sprite):
    def __init__(self,**kwags): # Required: surf, text; Opitional: xy, colour
        for k, v in kwags.iteritems():
            setattr(self, k, v)
        if not xy in locals(): self.xy = (0,0)
        if not colour in locals(): self.colour = (0,0,0)
        print('Locals',locals())
    def update(self):
        word_wrap(surf,text,pygame.freetype.Font(os.path.join("Assets/",'8-bit Arcade Out.ttf'),48),colour = (200,200,201),xy = xy)
        word_wrap(surf,text,pygame.freetype.Font(os.path.join("Assets/",'8-bit Arcade In.ttf'),48),xy = xy)

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

def add(func,grp,**kwags):
    z = func(kwags)
    updateg.add(z)
    
    if not grp in globals():
        global grp
        grb = pygame.sprite.Group()
        grb.add(x)
