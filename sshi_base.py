import pygame
import os
import time
import ctypes
import pygame.freetype

import sshi_core as core
import sshi_graphics as grph

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
        self.b2 = Button((77, 117), (103, 24), (0, 0, 0), 'Settings', M_settings)
        self.b3 = Button((77, 175), (103, 24), (0, 0, 0), 'Credits', M_credits)  # Credits is a built in variable, so it can't be assigned
        self.group = pygame.sprite.Group()
        self.group.add(self.b1), self.group.add(self.b2)
        self.group.add(self.b3)
    
    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)
        for event in pygame.event.get():
            events(event)


class M_credits(M_page):
    def __init__(self):
        global m
        m(M_credits)
        self.b = []
        self.b.append(Button((0, 0), (256, 24), (0, 0, 0), '(c) Marcus Wishart', test, True))
        self.b.append(Button((0, 24), (256, 24), (0, 0, 0), 'Original idea', test, True))
        self.b.append(Button((0, 48), (256, 24), (0, 0, 0), 'Original design in Lua', test, True))
        self.b.append(Button((0, 72), (256, 24), (0, 0, 0), '=' * 15, test, True))
        self.b.append(Button((0, 96), (256, 24), (0, 0, 0), 'Fonts from:', test, True))
        self.b.append(Button((0, 120), (256, 24), (0, 0, 0), '8-bit Arcade In &', test, True))
        self.b.append(Button((0, 144), (256, 24), (0, 0, 0), '8-bit Arcade Out', test, True))
        self.b.append(Button((0, 168), (256, 24), (0, 0, 0), 'From Damien Gosset', test, True))
        self.b.append(Button((0, 192), (256, 24), (0, 0, 0), '+' * 15, test, True))
        self.b.append(Button((0, 216), (256, 24), (0, 0, 0), 'Manaspace', test, True))
        self.b.append(Button((0, 240), (256, 24), (0, 0, 0), 'From codeman38', test, True))

        self.group = pygame.sprite.Group()

        self.elapsed_time = time.time()
        self.message = grph.message_box('Press the key esc to leave', (106, 23, 45, 200), [256, 16], xy=[0, 240])
        for x in self.b:
            self.group.add(x)
        self.scroll = 0

    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)
        if time.time() - self.elapsed_time > 7.5:
            self.message.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.scroll = core.minmax(0, self.scroll + event.__dict__['y'] * 10, 5)
            events(event)

    def draw(self):
        s_screen = pygame.Surface((256, 1024), pygame.SRCALPHA)
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.group.draw(s_screen)
        t_screen.blit(s_screen, (0, 0 - self.scroll))
        t_screen.blit(self.message.image, (0, 0))
        return t_screen


class M_settings(M_page):
    def __init__(self):
        global m
        m(M_settings)
        self.b = []
        self.b.append(Button((0, 0), (256, 24), (0, 0, 0), 'Marcus Wishart', test))
        self.group = pygame.sprite.Group()
        for x in self.b:
            self.group.add(x)
        self.scroll = 0
        self.elapsed_time = time.time()
        self.message = grph.message_box('Press the key esc to leave', (106, 23, 45, 200), [256, 16], xy=[0, 240])
    
    def update(self, *args, **kwargs):
        self.group.update(*args, **kwargs)
        if time.time() - self.elapsed_time > 7.5:
            self.message.update()
        for event in pygame.event.get():
            events(event)
    
    def draw(self):
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.group.draw(t_screen)
        t_screen.blit(self.message.image, (0, 0))
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
                            self.action(kwargs[self.txt])
                        else:
                            self.action()
                    events(event)
                self.image.fill([min(a + 100, 255) for a in self.colour])
            else:
                self.image.fill(self.colour)
            grph.word_wrap(self.image, self.txt, pygame.freetype.Font(os.path.join("Assets/", '8-bit Arcade In.ttf'), 16), (255, 255, 255), 'center')
        else:
            self.image.fill(self.colour)
            grph.word_wrap(self.image, self.txt, pygame.freetype.Font(os.path.join("Assets/", 'manaspace.regular.ttf'), 12), (255, 255, 255), 'center')


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


def events(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        m(M_main)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()

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
        mscreen.blit(pygame.image.load(os.path.join('Assets', 'menu_background.png')), (0,0))
        m.update(Play=mscreen) # The key is the txt on the button
        mscreen.blit(m.draw(), (0, 0))
