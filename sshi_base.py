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


class M_page:
    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)

    def draw(self):
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.group.draw(t_screen)
        return t_screen


class M_main(M_page):
    def __init__(self):
        self.b1 = Button((77, 59), (103, 24), (0, 0, 0), 'Play', core.start)
        self.b2 = Button((77, 117), (103, 24), (0, 0, 0), 'Settings', test)
        self.b3 = Button((77, 175), (103, 24), (0, 0, 0), 'Credits', M_credits)  # Credits is a built in variable, so it can't be assigned
        self.group = pygame.sprite.Group()
        self.group.add(self.b1), self.group.add(self.b2)
        self.group.add(self.b3)


class M_credits(M_page):
    def __init__(self):
        global m
        m(M_credits)
        self.b1 = Button((0, 0), (256, 24), (0, 0, 0), '(c) Marcus Wishart', test, True)
        self.b2 = Button((0, 24), (256, 24), (0, 0, 0), 'b', test, True)
        self.b3 = Button((0, 48), (256, 24), (0, 0, 0), 'c', test, True)
        self.group = pygame.sprite.Group()
        self.group.add(self.b1), self.group.add(self.b2)
        self.group.add(self.b3)
        self.scroll = 0

    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.scroll = core.minmax(0, self.scroll - event.__dict__['y'] * 10, 1024)
                print('changed')
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        s_screen = pygame.Surface((256, 1024), pygame.SRCALPHA)
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        print(self.scroll)
        self.group.draw(s_screen)
        t_screen.blit(s_screen, (0, 0 + self.scroll))
        return t_screen


class Button(pygame.sprite.Sprite):
    def __init__(self, xy, wh, colour, txt, action, font=None):
        super().__init__()
        self.xy, self.wh = xy, wh
        self.image = pygame.Surface(wh)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.action = action
        self.txt = txt
        self.font = font
        self.colour = colour

    def update(self, *args, **kwargs):
        if self.font == None:
            mouse_pos = pygame.mouse.get_pos()
            if self.xy[0] <= mouse_pos[0] <= (self.xy[0] + self.wh[0]) and self.xy[1] <= mouse_pos[1] <= (self.xy[1] + self.wh[1]):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__['button'] == 1:
                        if self.action == core.start:
                            self.action(**kwargs)
                        else:
                            self.action()
                self.image.fill((100, 100, 100))
            else:
                self.image.fill(self.colour)
            grph.word_wrap(self.image, self.txt, pygame.freetype.Font(os.path.join("Assets/", '8-bit Arcade In.ttf'), 16), (255, 255, 255), 'center')
        else:
            self.image.fill(self.colour)
            grph.word_wrap(self.image, self.txt, pygame.freetype.SysFont('comic sans', 14), (255, 255, 255), 'center')


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


class Menus:
    state = M_main

    def __init__(self):
        self.state = Menus.state()

    def __call__(self, state):
        if Menus.state != state:
            Menus.state = state
            self.state = Menus.state()

    def draw(self):
        self.screen = self.state.draw()
        return self.screen

    def update(self, *args, **kwargs):
        self.state.update(*args, **kwargs)


def test(*args, **kwargs):
    print('done')


if __name__ == '__main__':
    pygame.freetype.init()
    clock = pygame.time.Clock()
    mscreen = make_screen()
    m = Menus()
    while True:
        pygame.display.flip()
        clock.tick(60)  # Locks the frame rate to 60 fps
        mscreen.blit(pygame.image.load(os.path.join('Assets', 'background_res1.png')), (0,0))
        m.update(screen=mscreen)
        mscreen.blit(m.draw(), (0, 0))
        core.events()
