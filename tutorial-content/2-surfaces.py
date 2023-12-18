"""
Displaying images with surfaces in pygame.
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
test_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)

test_surface_rect = pygame.Surface((100, 200))
test_surface_rect.fill("Red")

sky_surface = pygame.image.load("tutorial-content\lib\graphics\Sky.png")
ground_surface = pygame.image.load("tutorial-content\lib\graphics\ground.png")
text_surface = test_font.render("Dolting", False, "Blue")

# Creating text: create an image of the text --> render on display surface
"""
1. Create a font (text size and style)
2. Write text on a surface
3. Blit the text surface
"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("user exit")
            exit()

    # blit = block image transfer (put a surface on another)
    # screen.blit(test_surface_rect, (200, 100)) 
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (120, 50))

    pygame.display.update()
    clock.tick(60)