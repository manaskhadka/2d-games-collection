"""
Changing states in pygame. Adds a gameover and start state
NOTE: State changes are not implemented using pygame, just normal control flow logic
"""
import pygame 
from sys import exit

def display_score():
    curr_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'{curr_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return curr_time
 
pygame.init()
pygame.display.set_caption('Game States')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()

snail_surf = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomleft=(600, 300))

player_surf = pygame.image.load("tutorial-content/lib/graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80,300))
player_gravity = 0

# Intro screen 
player_stand = pygame.image.load("tutorial-content/lib/graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name =  pixel_font.render("Dolt Runner", False, (111, 130, 196))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = pixel_font.render('Press space to jump', False, (111,130,196))
game_message_rect = game_message.get_rect(center=(400, 325))

game_active = False
start_time = 0
score = 0

screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("User exit")
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                print("Jump button pressed")
                if player_rect.bottom == 300: player_gravity = -20
            if event.key == pygame.K_SPACE and not game_active:
                snail_rect.left = 800
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        
        # Snail (Enemy)
        if snail_rect.right <= 0: snail_rect.left = 800
        snail_rect.left -= 4
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.top += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        if snail_rect.colliderect(player_rect):
            print("Gameover collision!")
            game_active = False
    else:
        screen.fill((94, 180, 94))
        screen.blit(player_stand, player_stand_rect)
        score_message = pixel_font.render(f"Your score: {score}", False, (111,130,196))
        score_message_rect = score_message.get_rect(center=(400, 40))
        screen.blit(game_name, game_name_rect)
        screen.blit(score_message, score_message_rect)
        screen.blit(game_message, game_message_rect)


    pygame.display.update()
    clock.tick(60)