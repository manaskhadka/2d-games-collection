"""
Positioning surfaces and collisions using rectangles & detecting mouse collisions
Main Concept:
    NOTE: The following can be simplified using a Sprite object (combines surface + rect)
    Rectangles allow for precise positioning of surfaces and can be used for basic collisions.
    1. Use a surface for image info
    2. Place the surface using rectangle
    3. Use rectangle to detect surface collisions
"""
import pygame 
from sys import exit

pygame.init()
pygame.display.set_caption('Collisions')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()
text_surface = pixel_font.render("Dolting", False, "Blue")

snail_surf = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomleft=(600, 300))

player_surf = pygame.image.load("tutorial-content/lib/graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80,300))

screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("User exit")
            exit()

        if event.type == pygame.MOUSEMOTION:
            if (player_rect.collidepoint(event.pos)):
                print(f"Mouse collision detected. Buttons: {pygame.mouse.get_pressed()}")

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (120, 50))

    if snail_rect.right <= 0: snail_rect.left = 800
    snail_rect.left -= 4
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    collision = player_rect.colliderect(snail_rect) # Returns 0 or 1 depending on collision status
    if collision:
        print("Collision")

    """
    The below is done in the event loop
    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed())
    """

    pygame.display.update()
    clock.tick(60)