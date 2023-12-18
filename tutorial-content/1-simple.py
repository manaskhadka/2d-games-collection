"""
Basic program for pygame. 
Creates a blank display and allows for user input to quit
"""
import pygame 
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

pygame.display.set_caption('Simple')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("user exit")
            exit()

    # draw all elements + update everything
    pygame.display.update()
    clock.tick(60)




