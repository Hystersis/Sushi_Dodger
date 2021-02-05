# Graphics for Game
import random
import pygame
import sshi_LnDrw as ld
import numpy as np

global maze, particles, litr

pygame.freetype.init(resolution=48)

litr = {'Active' : None,
        'Paused' : None,
        'Died' : "defeat_screen.png",
        'Won' : None} # Code must be added here in the future to list the .png for 'Won'
particles = pygame.sprite.Group()

class mv_prtcl(pygame.sprite.Sprite):
    def __init__(self,strt,end,imge):
        self.path = ld.draw_line(np.zeros((256,256)),strt[0],strt[1],end[0],end[1])
        self.image = pygame.image.load(imge)
        self.rect = self.image.get_rect()
        self.rect.topleft = strt
        # add any animations for start here
    def update(self):
        if len(self.path) < 1:
            # Add any animations for end here
            self.kill()
        else:
            self.rect.topleft = self.path.pop(0)


def particle(mode,image,map = None,startC = None, endC = None,pr = None,inplace = False):
    pr = mv_prtcl(startC,endC,image) if mode == 0 else pr
    # pr = /Add next particle/
    particles.add(pr)

class transition:
    """tr is transition"""
    count = 0
    def __init__(self):
        self.image = None
        transition.count += 1
        if transition.count > 1:
            raise ValueError('The amount of transition is over threshold.')
    def update(self,image):
        if image != None:
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
    def draw(self):
        return self.image

def screenLow(screen):
    screen = screen.copy()
    return screen

def screenHigh(screen,gm):
    screen = screen.copy()
    particles.update()
    particles.draw(screen)
    tr.update(litr[gm])
    screen.blit(tr.draw(),[42,0]) if tr.draw() != None else None
    return screen

tr = transition()

def word_wrap(surf, text, font, color=(0, 0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    x, y = 0, line_spacing
    space = font.get_rect(' ')
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width:
            x, y = 0, y + line_spacing
        if x + bounds.width + bounds.x >= width:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= height:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x, y), None, color)
        x += bounds.width + space.width
    return x, y
