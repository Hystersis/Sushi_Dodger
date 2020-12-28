# Graphics for Game
import random
import pygame
import sshi_LnDrw as ld
import numpy as np

global maze, particles


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

def screenLow(screen):
    screen = screen.copy()
    return screen

def screenHigh(screen):
    screen = screen.copy()
    particles.update()
    particles.draw(screen)
    return screen

def particle(mode,image,map = None,startC = None, endC = None,pr = None,inplace = False):
    pr = mv_prtcl(startC,endC,image) if mode == 0 else pr
    # pr = /Add next particle/
    particles.add(pr)

def scaling(screen):
    screen = pygame.surfarray.array2d(screen)
    screen = np.array(screen)
    info = pygame.display.Info()
    sw,sh = info.current_w, info.current_h
    mrx, mry = int(np.floor(sw / 256)), int(np.floor(sh / 256))
    r = min(mrx,mry)
    uw, uh = w * r, w * r
    nscreen = np.zeros((uw,uh))
    for y in enumerate(screen):
        for x in enumerate(y[1]):
            nscreen[x[0]:x[0]+r,y[0]:y[0]+r] = x[1] #Change the pixels on the nscreen to the original value
    screen = pygame.surfarray.make_surface(nscreen)
    return screen
