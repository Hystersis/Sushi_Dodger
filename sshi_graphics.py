# Graphics for Game
import random
import pygame
import sshi_InDrw as ld
import numpy as np

global maze
maze = []
b = []
for x in range(256):
    for y in range(256):
        b.append(0)
    maze.append(b)
    b = []

class mv_prtcl(pygame.sprite.Sprite):
    def __init__(self,strt,end,imge):
        self.path = ld.draw_line(np.zeros((256,256)),strt[0],strt[1],end[0],end[1])
        self.image = pygame.image.load(imge)
        self.rect = self.image.get_rect()
        self.rect.topleft = strt
        print(self.path)
    def update(self):
        if len(self.path) <= 1:
            # Add any animations for end here
            self.kill()
        else:
            self.rect.topleft = self.path.pop(0)

pr = mv_prtcl([0,0],[256,256],"dodger_1.png")
ddger_group = pygame.sprite.Group()
ddger_group.add(pr)

while len(ddger_group) > 0:
    ddger_group.update()
    print("ran")
