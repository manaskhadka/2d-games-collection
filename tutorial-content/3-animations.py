"""
Basic animations in pygame.
Moves a static image from right to left. 
Repositions image after moving offscreen to give a visual loop effect.
"""
import pygame 
from sys import exit

pygame.init()
pygame.display.set_caption('Animations')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()
text_surface = pixel_font.render("Dolting", False, "Blue")
snail_surface = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
snail_x_pos = 600
snail_y_pos = 250

screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("user exit")
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (120, 50))

    snail_x_pos -= 4
    if snail_x_pos < -100: snail_x_pos = 800

    screen.blit(snail_surface, (snail_x_pos, snail_y_pos))

    pygame.display.update()
    clock.tick(60)