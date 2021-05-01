import pygame
import sshi_core as core
import os
import ctypes
import sshi_graphics as grph
import pygame.freetype

# `7MMM.     ,MMF'
#   MMMb    dPMM
#   M YM   ,M MM  .gP"Ya `7MMpMMMb.`7MM  `7MM
#   M  Mb  M' MM ,M'   Yb  MM    MM  MM    MM
#   M  YM.P'  MM 8M""""""  MM    MM  MM    MM
#   M  `YM'   MM YM.    ,  MM    MM  MM    MM
# .JML. `'  .JMML.`Mbmmd'.JMML  JMML.`Mbod"YML.


class Menu:
    def __init__(self):
        self.b1 = Button((77, 59), (103, 24), (0, 0, 0), 'Play', core.start)
        self.b2 = Button((77, 117), (103, 24), (0, 0, 0), 'Settings', test)
        self.b3 = Button((77, 175), (103, 24), (0, 0, 0), 'Credits', credits)
        self.group = pygame.sprite.Group()
        self.group.add(self.b1), self.group.add(self.b2)
        self.group.add(self.b3)

    def __call__(self):
        return self.group


class Button(pygame.sprite.Sprite):
    def __init__(self, xy, wh, colour, txt, action):
        super().__init__()
        self.xy, self.wh = xy, wh
        print(self.xy, self.wh)
        self.image = pygame.Surface(wh)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.action = action
        self.txt = txt
        print(f'Button at {id(self)}')

    def update(self, *args, **kwargs):
        mouse_pos = pygame.mouse.get_pos()
        if self.xy[0] <= mouse_pos[0] <= (self.xy[0] + self.wh[0]) and self.xy[1] <= mouse_pos[1] <= (self.xy[1] + self.wh[1]):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.action(*args, **kwargs)
            self.image.fill((100, 100, 100))
        else:
            self.image.fill((0, 0, 0))
        grph.word_wrap(self.image, self.txt, pygame.freetype.Font(os.path.join("Assets/", '8-bit Arcade In.ttf'), 16), (255, 255, 255), 'center')


def make_screen():
    icon = pygame.image.load(os.path.join("Assets", "dodger_icon.png"))
    pygame.display.set_icon(icon)
    myappid = 'mycompany.myproduct.subproduct.version'
    # allows for taskbar icon to be changed
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    pygame.display.set_caption("Sushi Dodger")
    screen = pygame.display.set_mode((256, 256), flags=pygame.RESIZABLE
                                     | pygame.SCALED)
    # This allows the screen to be bigger that it was
    return screen


# core.start(screen=mscreen)



def test(*args, **kwargs):
    print('done')


if __name__ == '__main__':
    pygame.freetype.init()
    m = Menu()
    g = m()
    clock = pygame.time.Clock()
    mscreen = make_screen()
    while True:
        pygame.display.flip()
        clock.tick(60)  # Locks the frame rate to 60 fps
        mscreen.blit(pygame.image.load(os.path.join('Assets', 'background_res1.png')), (0,0))
        g.update(screen=mscreen)
        g.draw(mscreen)
        core.events()
