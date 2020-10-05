# Sushi Dodger
# Created by Hystersis W, 2020
# Screen size = 256*256
import math
import random
import pygame
import tkinter as tk
import grid_values as gr
from tkinter import messagebox



#                                                 ,,         ,,
# MMP""MM""YMM                     db           `7MM       `7MM
# P'   MM   `7                    ;MM:            MM         MM
#      MM       ,pW"Wq.          ,V^MM.      ,M""bMM    ,M""bMM
#      MM      6W'   `Wb        ,M  `MM    ,AP    MM  ,AP    MM
#      MM      8M     M8        AbmmmqMA   8MI    MM  8MI    MM
#      MM      YA.   ,A9       A'     VML  `Mb    MM  `Mb    MM
#    .JMML.     `Ybmd9'      .AMA.   .AMMA. `Wbmd"MML. `Wbmd"MML.

# Add checking in Line 168 for negtives


pygame.init()

def initi():
    global flag, screen_width, screen, ddger_group, sshi_group, lvel, ddger
    flag = True
    # Game Screen
    screen_width = 256
    screen = pygame.display.set_mode((screen_width,screen_width))
    pygame.display.set_caption("Sushi Dodger")
    pygame.mouse.set_visible(False)
    # Level and dodger initilization
    lvel = Level()
    ddger = dodger("dodger_1.png")
    ddger_group = pygame.sprite.Group()
    ddger_group.add(ddger)
    # sushi setup code
    sshi_group = pygame.sprite.Group()
    for a in range(11):
        sshi = sushi([random.randrange(256),random.randrange(256)])
        sshi_group.add(sshi)


class Level:
    lev = 1
    def __init__(self):
        lev_num = self.lev
    def get_num(self, num_sshi = 0):
        if num_sshi >= 40:
            num_sshi = 40
        else:
            num_sshi = self.lev * 2 + 14
        return int(num_sshi)
    def get_lev(self):
        return int(self.lev)
    def next_lev(self, is_endless = False):
        if self.lev < 5 or is_endless:
            self.lev += 1
            next_Lvl()





#                               ,,
# `7MM"""Yb.                  `7MM
#   MM    `Yb.                  MM
#   MM     `Mb  ,pW"Wq.    ,M""bMM  .P"Ybmmm .gP"Ya `7Mb,od8
#   MM      MM 6W'   `Wb ,AP    MM :MI  I8  ,M'   Yb  MM' "'
#   MM     ,MP 8M     M8 8MI    MM  WmmmP"  8M""""""  MM
#   MM    ,dP' YA.   ,A9 `Mb    MM 8M       YM.    ,  MM
# .JMMmmmdP'    `Ybmd9'   `Wbmd"MML.YMMMMMb  `Mbmmd'.JMML.
#                                  6'     dP
#                                  Ybmmmd'


class dodger(pygame.sprite.Sprite):
    pos = [128,16]
    dirnx = 0
    dirny = 0
    def __init__(self, picture_path):
        super().__init__()
        # Sprite
        self.image = pygame.image.load(picture_path)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    print('Going left',self.dirnx,self.dirny)
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    print('Going right',self.dirnx,self.dirny)
                else:
                    self.dirnx = 0

                if keys[pygame.K_UP]:
                    self.dirny = -1
                    print('Going up',self.dirnx,self.dirny)
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    print('Going down',self.dirnx,self.dirny)
                else:
                    self.dirny = 0

        self.dirny += 0.025
        if 0 < self.pos[0] and self.dirnx <= 0:
            self.pos[0] += self.dirnx
        elif 240 > self.pos[0] and self.dirnx >= 0:
            self.pos[0] += self.dirnx
        if 0 < self.pos[1] and self.dirny <= 0:
            self.pos[1] += self.dirny
        if 240 > self.pos[1] and self.dirny >= 0:
            self.pos[1] += self.dirny
        # update self.position
        self.rect.topleft = self.pos
    def where_am_i(self):
        poses = []
        poses.append(self.pos[0])
        poses.append(self.pos[1])
        return poses




#                              ,,          ,,
#  .M"""bgd                  `7MM          db
# ,MI    "Y                    MM
# `MMb.   `7MM  `7MM  ,pP"Ybd  MMpMMMb.  `7MM
#   `YMMNq. MM    MM  8I   `"  MM    MM    MM
# .     `MM MM    MM  `YMMMa.  MM    MM    MM
# Mb     dM MM    MM  L.   I8  MM    MM    MM
# P"Ybmmd"  `Mbod"YML.M9mmmP'.JMML  JMML..JMML.





class sushi(pygame.sprite.Sprite):
    def __init__(self, sop):
        super().__init__()
        self.sop = [0,0]
        self.sop[0] = sop[0]
        self.sop[1] = sop[1]
        self.dirny = self.dirnx = 0
        self.rt = pygame.image.load('sushi_template.png')
        self.directory = 'sushi_center_'
        self.ran = random.randrange(2)
        self.directory = self.directory + str(self.ran) + '.png'
        self.center = pygame.image.load(str(self.directory))
        self.image = self.rt.copy()
        self.image.blit(self.center, (0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.sop
    def update(self,d_xy):
        # Makes Maze's 'walls'
        self.d = []
        self.z = [round(d_xy[0]),round(d_xy[1])]
        for xac in range(18):
            self.z_copy = [self.z[0] + 1, self.z[1]]
            self.d.append(self.z)
            for yio in range(3):
                self.d.append([self.z[0],self.z[1] - (yio + 1)])
            self.z = self.z_copy

        # Makes maze
        self.maze = []
        self.add = []
        # for ce in self.d:
        #     print(ce,'\t',self.d.index(ce),'\t',len(self.d))
        for aoe in range(256):
            for bve in range(256):
                for value in self.d:
                    if value == [bve,aoe]:
                        self.add.append(1)
                        break
                else:
                    self.add.append(0)

                if bve >= 255:
                    self.maze.append(self.add)
                    self.add = []
        print('\n',self.maze)
        self.endx = (int(d_xy[0]) - 16)
        self.endy = (int(d_xy[1]) - 8)
        self.end = (self.endx, self.endy) # edit this
        self.move = a_star_main(self.maze,self.sop,self.end)


def next_Lvl():
    global ddger, ddger_group, sshi_group
    sshi_group.clear()
    sshi_group = pygame.sprite.Group()
    lvel.next_lev()
    for sushi in range(lvel.get_num()):
        sshi = sushi((random.randrange(256),random.randrange(256)))
        sshi_group.add(sshi)




#                            ,,
# `7MMM.     ,MMF'           db
#   MMMb    dPMM
#   M YM   ,M MM   ,6"Yb.  `7MM  `7MMpMMMb.
#   M  Mb  M' MM  8)   MM    MM    MM    MM
#   M  YM.P'  MM   ,pm9MM    MM    MM    MM
#   M  `YM'   MM  8M   MM    MM    MM    MM
# .JML. `'  .JMML.`Moo9^Yo..JMML..JMML  JMML.


def main():
    clock = pygame.time.Clock()
    while flag:
        global ddger_group, sshi_group
        pygame.time.delay(300)
        clock.tick(60)
        pygame.display.flip()
        screen.fill((0,0,0))
        sshi_group.draw(screen)
        ddger_group.draw(screen)
        ddger_group.update()
        pstn = ddger.where_am_i()
        sshi_group.update(pstn)



#
#       db                    mm
#      ;MM:                   MM
#     ,V^MM.        ,pP"Ybd mmMMmm  ,6"Yb.  `7Mb,od8
#    ,M  `MM        8I   `"   MM   8)   MM    MM' "'
#    AbmmmqMA       `YMMMa.   MM    ,pm9MM    MM
#   A'     VML      L.   I8   MM   8M   MM    MM
# .AMA.   .AMMA.    M9mmmP'   `Mbmo`Moo9^Yo..JMML.


class Node():
    # """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    # """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def a_star_main(maze,start, end):
    path = astar(maze, start, end)
    return path



#                               ,,
# `7MM"""YMM                  `7MM
#   MM    `7                    MM
#   MM   d    `7MMpMMMb.   ,M""bMM
#   MMmmMM      MM    MM ,AP    MM
#   MM   Y  ,   MM    MM 8MI    MM
#   MM     ,M   MM    MM `Mb    MM
# .JMMmmmmMMM .JMML  JMML.`Wbmd"MML.



initi()
main()
