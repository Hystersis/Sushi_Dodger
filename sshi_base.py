import pygame
import os
import time
import ctypes
import pygame.freetype

import sshi_core as core
import sshi_graphics as grph
import sshi_json as jsn

# `7MMM.     ,MMF'
#   MMMb    dPMM
#   M YM   ,M MM  .gP"Ya `7MMpMMMb.`7MM  `7MM
#   M  Mb  M' MM ,M'   Yb  MM    MM  MM    MM
#   M  YM.P'  MM 8M""""""  MM    MM  MM    MM
#   M  `YM'   MM YM.    ,  MM    MM  MM    MM
# .JML. `'  .JMML.`Mbmmd'.JMML  JMML.`Mbod"YML.


class M_page:
    """A PARENT class template for all pages in the menu screen
    """
    def update(self, *args, **kwargs):
        """A basic template for the update method of the pages
        """
        self.group.update(*args, **kwargs)

    def draw(self):
        """A basic template for the draw method of the pages

        Returns
        -------
        pygame.Surface
            Returns a surfaces with all the objects drawn on it
        """
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.group.draw(t_screen)
        return t_screen


class M_main(M_page):
    """The main landing page for Sushi Dodger

    Parameters
    ----------
    M_page : class
        It is the parent class for all the pages,
        allowing for structural pattern adherence
    """
    def __init__(self):
        """The initalisation module for the main page
        """
        self.b1 = Button((77, 59), (103, 24), (0, 0, 0), 'Play', core.start)
        self.b2 = Button((77, 117), (103, 24), (0, 0, 0), 'Settings', M_settings)
        self.b3 = Button((77, 175), (103, 24), (0, 0, 0), 'Credits', M_credits)  # Credits is a built in variable, so it can't be assigned
        self.group = pygame.sprite.Group()
        self.group.add(self.b1)
        self.group.add(self.b2)
        self.group.add(self.b3)

    def update(self, *args, **kwargs):
        """The update method for the main page, very similar to the parent class' update method just
        has event management
        """        
        self.group.update(*args, **kwargs)
        for event in pygame.event.get():
            events(event)


class M_credits(M_page):
    """The credits page off the main landing page

    Parameters
    ----------
    M_page : class
        It is the parent class for all the pages, allowing for structural pattern adherence
    """    
    def __init__(self):
        """The initalisation method for the credits page, all the text in created 
        """        
        global m
        # This tells the menu system (m) that the credits page is now the main page
        m(self)

        self.group = pygame.sprite.Group()
        self.group.add(Button((0, 0), (256, 24), (0, 0, 0), '(c) Hystersis', void, True))
        self.group.add(Button((0, 24), (256, 24), (0, 0, 0), 'Original idea', void, True))
        self.group.add(Button((0, 48), (256, 24), (0, 0, 0), 'Original design in Lua', void, True))

        # This is a 'line' break between sections
        self.group.add(Button((0, 72), (256, 24), (0, 0, 0), '=' * 15, void, True))

        self.group.add(Button((0, 96), (256, 24), (0, 0, 0), 'Fonts from:', void, True))
        self.group.add(Button((0, 120), (256, 24), (0, 0, 0), '8-bit Arcade In &', void, True))
        self.group.add(Button((0, 144), (256, 24), (0, 0, 0), '8-bit Arcade Out', void, True))
        self.group.add(Button((0, 168), (256, 24), (0, 0, 0), 'From Damien Gosset', void, True))

        # This is a 'line' break between paragraphs
        self.group.add(Button((0, 192), (256, 24), (0, 0, 0), '+' * 15, void, True))

        self.group.add(Button((0, 216), (256, 24), (0, 0, 0), 'Manaspace', void, True))
        self.group.add(Button((0, 240), (256, 24), (0, 0, 0), 'From codeman38', void, True))

        self.group.add(Button((0, 264), (256, 24), (0, 0, 0), '=' * 15, void, True))

        self.group.add(Button((0, 288), (256, 24), (0, 0, 0), 'Music:', void, True))
        self.group.add(Button((0, 312), (256, 24), (0, 0, 0), 'Main game music is', void, True))
        self.group.add(Button((0, 336), (256, 24), (0, 0, 0), 'Kung Fu Fighters March - Fast', void, True))
        self.group.add(Button((0, 360), (256, 24), (0, 0, 0), 'By Loco Loco', void, True))

        self.group.add(Button((0, 384), (256, 24), (0, 0, 0), '+' * 15, void, True))

        self.group.add(Button((0, 408), (256, 24), (0, 0, 0), 'Backgroup music is', void, True))
        self.group.add(Button((0, 432), (256, 24), (0, 0, 0), 'Temple of the Dragon Friendship', void, True))
        self.group.add(Button((0, 456), (256, 24), (0, 0, 0), 'By Loco Loco', void, True))

        self.elapsed_time = time.time()

        # Adds a message box to alert people that they can escape out of credits page
        self.message = grph.message_box('Press the key esc to leave', (106, 23, 45, 200), [256, 16], xy=[0, 240])
        self.scroll = 0

    def update(self, *args, **kwargs):
        """Update method for credits of sushi dodger
        """        
        self.group.update(*args, **kwargs)

        if time.time() - self.elapsed_time > 7.5:
            # After 7.5 seconds, show the alert message box
            self.message.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                # Allows for scrolling up and down of the page
                # Scrolling 'up' the scroll wheel, scrolls up the page and vice versa
                # This can be changed with the negative sign in front of 'event.__dict__[y]'
                self.scroll = core.minmax(0, self.scroll + -event.__dict__['y'] * 10, 224)
            events(event)

    def draw(self):
        """Draws the scrolling screen to 256*256 area

        Returns
        -------
        pygame.Surface
            Returns a surfaces with all the objects drawn on it
        """
        # The scrolling screen
        s_screen = pygame.Surface((256, 1024), pygame.SRCALPHA)

        # The 'viewing' screen in 256*256 resolution
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)

        # Draws all the text onto the scrolling screen
        self.group.draw(s_screen)

        # 'Scrolls' the screen up or down in the viewpot 
        t_screen.blit(s_screen, (0, 0 - self.scroll))
        t_screen.blit(self.message.image, (0, 0))
        return t_screen


class M_settings(M_page):
    """The settings page off the main landing page

    Parameters
    ----------
    M_page : class
        It is the parent class for all the pages, allowing for structural pattern adherence
    """
    def __init__(self):
        """The initialisation system for the settings page
        """        
        global m
        # This tells the menu system (m) that the settings page is now the main page
        m(self)

        self.group = pygame.sprite.Group()
        # The SFX Toggle
        self.group.add(Button((5, 5), (128, 24), (0, 0, 0), 'Do Sound Effects', void, do_hover=False))
        self.group.add(StateFullButton((220, 5), (30, 24), jsn.config().sget('SFX'), void, {True: (0,230,118), False: (255,23,68),
                                                                        'txt': {True: 'T', False: 'F'}}, SFX_control()))

        # The Music Toggle
        self.group.add(Button((5, 34), (128, 24), (0, 0, 0), 'Do Music', void, do_hover=False))
        self.group.add(StateFullButton((220, 34), (30, 24), jsn.config().sget('Music'), void, {True: (0,230,118), False: (255,23,68),
                                                                        'txt': {True: 'T', False: 'F'}}, music_control()))

        # Adds an alert box to tell people they can exit 
        self.elapsed_time = time.time()
        self.message = grph.message_box('Press the key esc to leave', (106, 23, 45, 200), [256, 16], xy=[0, 240])

    def update(self, *args, **kwargs):
        """The update method for the settings page
        """
        # Puts a different backgroup for the settings page
        mscreen.blit(pygame.image.load(os.path.join('Assets', 'sunset1.png')), (0,0))
        self.group.update(*args, **kwargs)

        if time.time() - self.elapsed_time > 7.5:
            # After 7.5 seconds, show the alert message box
            self.message.update()
        for event in pygame.event.get():
            events(event)

    
    def draw(self):
        """The drawing method for the settings screen

        Returns
        -------
        pygame.Surface
            Returns a surfaces with all the objects drawn on it
        """        
        t_screen = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.group.draw(t_screen)
        t_screen.blit(self.message.image, (0, 0))
        return t_screen


class SFX_control:
    """The sound effects (SFX) control class, allowing for toggling on or off
    of sound effects
    """
    def __init__(self) -> None:
        self.num_of_channels = pygame.mixer.get_num_channels()

    @property
    def val(self):
        return self._state
    
    @val.setter
    def val(self, value):
        self._state = value
        if value:
            # Turning on playback, so value is True
            jsn.config().write("SFX", True)
            
        else:
            # Turning off playback, so value is False
            jsn.config().write("SFX", False)


class music_control:
    def __init__(self):
        self._state = False

    @property
    def val(self):
        return self._state
    
    @val.setter
    def val(self, value):
        self._state = value
        if value:
            jsn.config().write("Music", True)
            pygame.mixer.Channel(0).set_volume(1)
        else:
            jsn.config().write("Music", False)
            pygame.mixer.Channel(0).set_volume(0)
        print(pygame.mixer.Channel(0).get_volume())
    

class Button(pygame.sprite.Sprite):
    def __init__(self, xy, wh, colour, txt, action, font=None, do_hover=True):
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
        self.do_hover = do_hover

    def update(self, *args, **kwargs):
        if self.font == None:
            mouse_pos = pygame.mouse.get_pos()
            if self.xy[0] <= mouse_pos[0] <= (self.xy[0] + self.wh[0]) and self.xy[1] <= mouse_pos[1] <= (self.xy[1] + self.wh[1]) and self.do_hover:
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

class StateFullButton(pygame.sprite.Sprite):
    def __init__(self, xy, wh, current_state, action, state_dict: dict, state_latch = None):
        """[summary]

        Parameters
        ----------
        xy : tuple
            The xy position of the topleft corner
        wh : tuple
            The width and height of the button
        current_state : bool
            The current state either True or False
        action : Any
            Any action to be performed on a state change
        state_dict : dict
            The colours that should be change between:
            dict should be in this form:
            {True: (a, b, c), False: (x, y, z)}
            -- or --
            {True: (a, b, c), False: (x, y, z), 'txt' : {True: 'text1', False: 'text2'}}
        """        
        super().__init__()
        self.xy, self.wh = xy, wh
        self.image = pygame.Surface(wh)
        self.image.fill(state_dict[current_state])
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.action = action
        self._state = current_state
        if state_latch is not None:
            self._latch = state_latch
        self.state_dict = state_dict
        # The state is dict of colour 

    def update(self, *args, **kwargs):
        mouse_pos = pygame.mouse.get_pos()
        if self.xy[0] <= mouse_pos[0] <= (self.xy[0] + self.wh[0]) and self.xy[1] <= mouse_pos[1] <= (self.xy[1] + self.wh[1]):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__['button'] == 1:
                    # This means that the mouse button has been pressed
                    self._state = not self._state
                    # Flips self.state from one bool to another
                    if '_latch' in self.__dict__.keys():
                        self._latch.val = self._state

        self.image.fill(self.state_dict[self._state])
        if 'txt' in self.state_dict.keys():
            nex_xy = grph.word_wrap(self.image, self.state_dict['txt'][self._state], pygame.freetype.Font(os.path.join("Assets/", '8-bit Arcade In.ttf'), 32), (255, 255, 255), 'center')
            grph.word_wrap(self.image, self.state_dict['txt'][self._state], pygame.freetype.Font(os.path.join("Assets/", '8-bit Arcade Out.ttf'), 32), (197,202,233), nex_xy)
    
    # class change_state:
    #     def __init__(self, change_class, change_variable):
    #         self.change_str = f'{change_class}.{change_variable}'
        
    #     def __call__(self, arg):
    #         exec(f'{self.change_str} = {arg}')
        
    #     def __setattr__(self, __name: str, arg) -> None:
    #         exec(f'{self.change_str} = {arg}')

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
        m(M_main())
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()

class Menus:
    def __init__(self):
        self.state = M_main()

    def __call__(self, state):
        if self.state != state:
            self.state = state

    def draw(self):
        self.screen = self.state.draw()
        return self.screen

    def update(self, *args, **kwargs):
        self.state.update(*args, **kwargs)


def void(*args, **kwargs):
    print('done')


if __name__ == '__main__':
    jsn.init()
    pygame.freetype.init()
    clock = pygame.time.Clock()
    mscreen = make_screen()
    m = Menus()
    core.start_sounds()

    # Music
    if jsn.config().sget("Music"):
        pygame.mixer.Channel(0).play(sound := pygame.mixer.Sound(os.path.join("Assets","Sounds","Background-sound.mp3")), loops = -1)
        sound.set_volume(0.08)

    while True:
        pygame.display.flip()
        clock.tick(60)  # Locks the frame rate to 60 fps
        mscreen.blit(pygame.image.load(os.path.join('Assets', 'menu_background.png')), (0,0))
        m.update(Play=mscreen) # The key is the txt on the button
        mscreen.blit(m.draw(), (0, 0))
