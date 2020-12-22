# Graphics for Game
import random
import pygame
import astar as at


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
        self.path = at.main(maze,strt,end)
        self.image = imge
        self.rect = self.image.get_rect()
        self.rect.topleft = strt
    def update(self):
        pass

# def main():
#     screen =
