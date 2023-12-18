"""
Displaying images with surfaces (pygame object representing images).
Main concept:
    There exists a display surface that is always visible (game window)
    We can make as many surfaces as we want that we can render on display surface
    Analogy: Display surface = whiteboard, surfaces = sticky notes
"""

import pygame 
from sys import exit

pygame.init()
pygame.display.set_caption('Surfaces')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill("Red")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("user exit")
            exit()

    screen.blit(test_surface, (200, 100)) # blit = block image transfer (put a surface on another)

    pygame.display.update()
    clock.tick(60)