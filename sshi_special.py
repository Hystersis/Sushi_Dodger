from sshi_core import minmax
import pygame
import os
from operator import sub, add, mul
from itertools import repeat, cycle
import math
import random

from pygame import surface
from sshi_msci import Apj
import time


def sign(num: int, amount: int = 1) -> int:
    '''Function that takes an interger and return an absolute positive, negative or null value; the positive and negative values
    equalling the amount (default 1).'''
    if num > 0:
        return amount
    elif num == 0:
        return 0
    else:
        return -amount


class missile(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple, orientation: int):
        super().__init__()
        self.colours = [(174, 35, 52), (232, 59, 59), (249, 194, 43)]
        self.time = time.time()
        self.life_span = 7
        self.orientation = orientation
        self.orientate(self.orientation)
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.rect2 = self.missile.get_rect()
        self.rect2.topleft = start_pos
        self.acceleration = 1
        self.dirnx = 0
        self.dirny = 0
        self.particles = []
        self.explosion = []
        self._hit = True
        self.last_dist = math.inf

    def update(self, ddger, sshiG: pygame.sprite.Group):
        self.image.fill((0, 0, 0, 0))
        # https://gamedev.stackexchange.com/questions/17313/how-does-one-prevent-homing-missiles-from-orbiting-their-targets
        delta = tuple(map(sub, self.rect2.topleft, ddger.rect.topleft))

        # This returns the backside coords of the craft
        self.backside = list(map(add, self.rect2.center,
                                 tuple(map(sub, (0, 0), map(sign, delta)))
                                 * (self.rect2.size[0] // 2)))

        if self._hit:
            self.particles.append([self.backside, [random.gauss(0, 0.6), sign(self.rect2.center[1] - self.backside[1]) * 2], random.uniform(3, 4)])

        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.1
            colour = [a + b + c for a, b, c in zip(map(mul, self.colours[0], repeat(sinsq(min(p[2], 2), 4, 2))),
                        map(mul, self.colours[1], repeat(sinsq(p[2], 4))),
                        map(mul, self.colours[2], repeat(sinsq(max(p[2], 2), 4, 2))))]
            pygame.draw.circle(self.image, colour, tuple(map(int, p[0])), int(p[2]))

        for p in self.explosion:
            p[1] -= 1.5
            for i in [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]:
                self.particles.append([list(p[0]), i, random.uniform(3, 4)])
            expface = pygame.Surface((32, 32), flags=pygame.SRCALPHA)
            # Black outer circle
            pygame.draw.circle(expface, (46, 34, 47), (16, 16), 16 - p[1])
            # Red inner circle
            pygame.draw.circle(expface, (179, 56, 49), (16, 16), 16 - p[1] - 2)
            # Transparent cut-out circle
            pygame.draw.circle(expface, (0, 0, 0, 0), (16, 16),
                               12 - p[1] - int(p[1] / 3.2))
            self.image.blit(expface, (p[0][0] - 16, p[0][1] - 16))

        self.particles = [p for p in self.particles if p[2] > 0]
        self.explosion = [p for p in self.explosion if p[1] > 0]

        if self._hit:
            d = math.sqrt(delta[0] ** 2 + delta[1] ** 2)  # Pythagoras for distance
            a = self.acceleration
            s = math.sqrt(sum(map(self.calspeed, delta, self.rect2.topleft,
                                  ddger.rect.topleft, (ddger.dirnx, ddger.dirny))))
            # Speed in a quadratic sense with Pythagoras, so in an 2d plane
            esttime = (math.sqrt(s**2 + 2 * a * d) - s) / a
            estpos = (ddger.rect.topleft[0] + ddger.dirnx * esttime,
                    ddger.rect.topleft[1] + ddger.dirny * esttime)
            accel = tuple(map(self.expsign, map(sub, estpos, self.rect2.topleft)))
            self.dirnx += accel[0]
            self.dirny += accel[1]

            ordegrees = anglebetween(self.rect2.topleft, tuple(map(add, self.rect2.topleft, (self.dirnx, self.dirny))))
            self.orientate(abs((ordegrees + 90) // 45))

            self.rect2.topleft = tuple(map(minmax, (0, 0), tuple(map(add, (self.dirnx, self.dirny), self.rect2.topleft)), (239, 239)))
            self.image.blit(self.missile, self.rect2.topleft)

            if esttime <= 3 and esttime >= self.last_dist or (time.time() - self.time) > self.life_span:
                self.do_hit(ddger, sshiG)
                self._hit = False
            self.last_dist = esttime

    def orientate(self, orientation):
        """Orientates the missile in one of eight orientates as listed below
        also adds a fill effect to show how long until it self destructs

        Parameters
        ----------
        orientation : int
            Orientates the missile in 45o increments - 0 is facing bottom left
                 up
            +---+---+---+
            | 5 | 4 | 3 |       1
            +---+---+---+
       left | 6 |N/A| 2 | right 0
            +---+---+---+
            | 7 | 0 | 1 |       -1
            +---+---+---+        ^
                down             y
              -1  0   1        <x
        """
        # Orintation is 0 for facing bottom
        # Orientation is 1 for facing left-bottom (45o)
        colour = *self.colours[0], 255
        if orientation % 2 == 0:
            self.missile = pygame.image.load(os.path.join('Assets', 'missile.png'))
        else:
            # Rotated sprite
            self.missile = pygame.image.load(os.path.join('Assets', 'missile_rot.png'))
        durview = pygame.Surface((16, 16))
        durview.fill(colour)
        p16 = int((self.life_span - (time.time() - self.time)) / 0.4375)
        self.missile = pygame.transform.rotate(self.missile, orientation // 2 * 90)
        self.missile.blit(durview, (0, p16), special_flags=pygame.BLEND_RGBA_MULT)

    def do_hit(self, ddger, sshiG):
        """Calculates hit when the missile explodes

        Parameters
        ----------
        ddger : pygame.sprite.Sprite
            The ddger, so it can calculate hits
        sshiG : pygame.sprite.Group
            sshi group, for hits

        Notes
        -----
        The algorithm creates a circle of radius 30 then sees if that circle centered
        on the missile collides with the sprite mask of the sprites of either
        ddger or sshi_group, the sprite mask makes sure in only collides with
        the sprite not the empty space.
        """
        if self._hit:
            hit_surface = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
            pygame.draw.circle(hit_surface, (0, 0, 0), self.rect2.center, 30)
            mask = pygame.mask.from_surface(hit_surface)
            for sprite in sshiG:
                hit = mask.overlap(pygame.mask.from_surface(sprite.image),
                                sprite.rect.topleft)
                if type(hit) is tuple:
                    sprite.killed()
            hit = mask.overlap(pygame.mask.from_surface(ddger.image),
                            ddger.rect.topleft)
            if type(hit) is tuple:
                ddger.killed()
            self.explosion.append([self.rect2.center, 16])

    def calspeed(self, delta: tuple, sxy: tuple, dxy: tuple, dirn: tuple):
        """Calculates the speed that the ddger is travelling at relative to the missile

        Parameters
        ----------
        delta : tuple or list
            This is the delta calculated earlier
        sxy : tuple or list
            self xy - the x or y coordinate of the missile
        dxy : tuple or list
            ddger xy - the x or y coordinate of the ddger
        dirn : tuple or list
            ddger's dirn(x/y) - its movement in different direction

        Returns
        -------
        float
            Returns number that will be put into a quadratic equation later,
            so this the reason there is the square
        """
        return (abs(delta) - abs(sxy - (dxy + dirn)))**2

    def expsign(self, val: int):
        """Returns a value between 0 and 1

        Parameters
        ----------
        val : int
            The starting value should be an int

        Returns
        -------
        float or int
            A value that gets smaller the closer to zero and it cannot be
            bigger than 1
        """
        return min(val / 64, 1)


class laser_enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple):
        super().__init__()
        self.image = pygame.Surface((256, 256), flags=pygame.SRCALPHA)
        self.ship = pygame.image.load(Apj("ship.png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.rect2 = self.ship.get_rect()
        self.charge_cycle = cycle(range(18))
        self.time = time.time()

    def update(self, ddger, sshiG: pygame.sprite.Group):
        """Movement and firing solutions for laser

        Parameters
        ----------
        ddger : pygame.sprite.Sprite
            The dodger/player
        sshiG : pygame.sprite.Group
            The group of sshi

        Notes
        -----
        The algorithm 'draws' a line of where the ddger will be
        if it continued on its current directory, it then sees
        where the dodger will be at the time it would be able
        fire laser, if it was fired now - it then checks if it can hit
        the ddger by drawing lines off it. If the missile cannot hit it
        it calculates what postion it should be to hit it by - but
        every position moved is more delay for the laser so the coordinate
        that it predicts the ddger will be at it is moved by that amount and
        then it checks if it can hit.
        The laser is three pixels wide.
        """
        self.image.fill((0, 0, 0, 0))
        # Calculate where to move
        ang = abs(anglebetween(ddger.rect.center, self.rect2.center))
        if ang % 45 == 0:
            self.fire()
        else:
            # https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
            # This returns the angle closest to the current angle
            angto = min([ang // 45 * 45, (ang // 45 + 1) * 45], key=lambda x:abs(x-ang))
            # This makes the underflow/overflow of an angle
            trangto = (angto - 90) % 360
            delta = math.sqrt((ddger.rect.center[0] - self.rect2.topleft[0]) ** 2 +
                              (ddger.rect.center[1] - self.rect2.topleft[1]) ** 2)
            delta2 = (ddger.rect.center[0] - self.rect2.topleft[0],
                      ddger.rect.center[1] - self.rect2.topleft[1])
            if delta > 100:
                # Move towards dodger
                moveto = tuple(map(add, self.rect2.center, tuple(map(sign, delta2))))
            elif delta < 30:
                # Back away from dodger
                moveto = tuple(map(add, self.rect2.center, tuple(map(sign, delta2, (-1, -1)))))
            else:
                moveto = (self.rect2.center[0]
                                    + math.cos(trangto * math.pi / 180),
                                    self.rect2.center[1]
                                    + math.sin(trangto * math.pi / 180))
            self.rect2.center = tuple(map(minmax, (8, 8), moveto, (247, 247)))
        ordegrees = anglebetween(self.rect2.center, ddger.rect.center)
        self.orientate(abs((ordegrees - 90) // 45))
        self.image.blit(self.ship, self.rect2.topleft)
        # for v in range(0, 256):
        #     gopm = [self.rect2.center]
        #     est_pos = dco[min(len(dco), 13 + v)]
        #     collide_offset = anglebetween(self.rect2.center, est_pos) - 90
        #     if collide_offset % 45 == 0:
        #         go_to_pos = collide_offset
        #     if go_to_pos == self.rect2.center:
        #         self.fire()
        #     self.rect2.center += tuple(map(sign, map(sub, go_to_pos, self.rect2.center)))

        delta = tuple(map(sub, self.rect2.topleft, ddger.rect.topleft))
        Sdelta = tuple(map(sign, delta))
        # This returns the backside coords of the craft
        self.backside = list(map(add, self.rect2.center,
                                 tuple(map(sub, (0, 0), map(sign, delta)))
                                 * (self.rect2.size[0] // 2)))
        # Mapping of cycle:
        # 0 - reset everything
        # 1-10 charge laser
        # 11-14 fire laser:
        #    11 show outline
        #    12 make outline bigger
        #    13 calculate hits
        #    14 leave remanent of laser blast
        # 15-17 cooldown
        # n = next(self.charge_cycle)
        # if n >= 1 and n < 11:
        #     # -----Charge of laser-----
        #     pygame.draw.circle(self.image, tuple(map(add,
        #                                              map(mul,
        #                                                  (255, 255, 255, 150),
        #                                                  repeat(1 / 10 * (11 - n))),
        #                                               map(mul,
        #                                                   (77, 155, 230, 245),
        #                                                   repeat(1 / 10 * n)))), 
        #                        self.backside)
        # elif n >= 11 and n < 15:
        #     # -----Firing of laser-----
        #     pygame.draw.line()

    def fire(self):
        """The craft fires in one directions, as it won't fire often
        """
        print('fire!', time.time())

    def orientate(self, orientation):
        """Orientates the laser in one of eight orientates as listed below

        Parameters
        ----------
        orientation : int
            Orientates the missile in 45o increments - 0 is facing bottom left
                 up
            +---+---+---+
            | 5 | 4 | 3 |       1
            +---+---+---+
       left | 6 |N/A| 2 | right 0
            +---+---+---+
            | 7 | 0 | 1 |       -1
            +---+---+---+        ^
                down             y
              -1  0   1        <x
        """
        # Orintation is 0 for facing bottom
        # Orientation is 1 for facing left-bottom (45o)
        if orientation % 2 == 0:
            self.ship = pygame.image.load(os.path.join('Assets', 'ship.png'))
        else:
            # Rotated sprite
            self.ship = pygame.image.load(os.path.join('Assets', 'ship_rot.png'))
        self.ship = pygame.transform.rotate(self.ship, (orientation // 2 * 90))


# From https://realpython.com/python-rounding/#rounding-down
def roundd(num, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(num * multiplier) / multiplier


def roundu(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def sinsq(n: float, width: int, deviation=0) -> float:
    return math.sin((n+deviation) / (width / math.pi))**2


def minmax(a, b, c):
    '''This function returns the middle variable between the min variable
    and the max variable.'''
    return (lambda x: sorted(x)[1])([a, b, c])


def anglebetween(avector: tuple, bvector: tuple):
    """Find the angle between two vectors using atan2

    Parameters
    ----------
    avector : tuple
        The first 2D vector
    bvector : tuple
        The second 2D vector

    Notes
    -----
    The algorithm first finds the deltas: ydelta is bvector.y - avector.y then
    xdelta is bvector.x - avector.x, it than does atan2(ydelta, xdelta),
    it then converts that to degrees

    Returns
    -------
    [type]
        [description]
    """
    return math.degrees(math.atan2(bvector[1] - avector[1],
                                   bvector[0] - avector[0]))


def closer(a, b, c, by=1, maximise=False):
    """This angle determines which number b is closer too
    either a or c

    Parameters
    ----------
    a : int or float
        1st number to test which is closer to
    b : int or float
        The number to test how close it is to others
    c : int or float
        2nd number to test which is closer to
    by : int, optional
        The movement of b so how much should b be moved by, by default 1
    maximise : bool, optional
        Should invert the result instead returning which one b is further from,
        by default False

    Returns
    -------
    int or float
        Returns what the b value should be so it is closer to either of the
        two values (a or c)
    """
    smaller = min(a, c)
    larger = max(a, c)
    minus = [(b - by) - smaller, b - by]
    addition = [larger - (b + by), b + by]
    if min(minus[0], addition[0]) == minus[0]\
            or maximise and min(minus[0], addition[0]) == addition[0]:
        return minus[1]
    else:
        return addition[1]
