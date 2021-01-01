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
    import numpy as np
    # Details form https://tanalin.com/en/articles/integer-scaling/#h-algorithm
    screen = pygame.surfarray.array2d(screen)
    screen = np.array(screen)
    w, h = screen.shape[0], screen.shape[1]
    info = pygame.display.Info()
    sw,sh = info.current_w, info.current_h
    mrx, mry = int(np.floor(sw / w)), int(np.floor(sh / h))
    r = min(mrx,mry)
    print('r',r)
    uw, uh = w * r, h * r
    nscreen = np.zeros((uw,uh))
    for y in enumerate(screen):
        print('Y:',y[1],y[0])
        for x in enumerate(y[1]):
            fx = m(x[0],r)
            fy = m(y[0],r)
            print(x[1],"\'s x value:",x[0],"\tFx value:",fx,"\tFy value:",fy)
            nscreen[y[0]+fy:y[0]+r+fy,x[0] + fx:x[0]+r+fx] = x[1]
    screen = pygame.surfarray.make_surface(nscreen)
    return screen

def m(xy,r):
    return r -1  if xy > 0 else 0
