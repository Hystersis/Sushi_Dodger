import pygame
import sshi_core as core

# `7MMM.     ,MMF'
#   MMMb    dPMM
#   M YM   ,M MM  .gP"Ya `7MMpMMMb.`7MM  `7MM
#   M  Mb  M' MM ,M'   Yb  MM    MM  MM    MM
#   M  YM.P'  MM 8M""""""  MM    MM  MM    MM
#   M  `YM'   MM YM.    ,  MM    MM  MM    MM
# .JML. `'  .JMML.`Mbmmd'.JMML  JMML.`Mbod"YML.

class Menu:
    def __init__(self):
        pass

class Button(pygame.sprite.Sprite):
    def __init__(self, xy, wh, colour, txt):
        self.image = pygame.Surface(*wh)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = xy

    def update(self, action):
        mouse_pos = pygame.mouse.get_pos()
        if xy[0] <= mouse_pos[0] <= (xy[0] + wh[0]) and xy[0] <= mouse_pos[1] <= (xy[1] + wh[1]):
            #Do action
            action()

core.start()
