"""
Basic drawing in pygame using pygame.draw. Also looks into rgb and hexadecimal colors instead of defaults
Looks into how pygame rectangles (and other objects) can be used for drawing and coloring.
"""
import pygame 
from sys import exit

pygame.init()
pygame.display.set_caption('Animations')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)
text_color = (64, 64, 64)
box_color = "#c0e8ec"

sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()

snail_surf = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomleft=(600, 300))

player_surf = pygame.image.load("tutorial-content/lib/graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80,300))

score_surf = pixel_font.render("Score:", False, text_color)
score_rect = score_surf.get_rect(midbottom=(400, 50))

screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("User exit")
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, box_color, score_rect)
    pygame.draw.rect(screen, "Pink", score_rect, border_radius=14)
    screen.blit(score_surf, score_rect)

    #pygame.draw.line(surface=screen, color="Black", 
    #                 start_pos=screen.get_rect().topleft, 
    #                 end_pos=screen.get_rect().bottomright)
    pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100))
    
    

    if snail_rect.right <= 0: snail_rect.left = 800
    snail_rect.left -= 4
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)