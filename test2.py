import pygame
import os

a = pygame.image.load(os.path.join('Assets','mw_sushi_dodger_sprites.png'))

b = pygame.image.tostring(a, 'RGBA')
print(b)
print('\n===8 bit===\n')
c = pygame.image.tostring(a, 'P')
print(c)