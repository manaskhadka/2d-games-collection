"""
Adding logic for enemy spawns using timers.
Concept:
    1. Create a custom event
    2. Trigger that event continously 
    3. Add code to event loop for these changes
Enemy Spawning Logic:
    1. Create a list of obstacle rects
    2. When event is triggered (via timer), add a rect to the list
    3. Every frame, move each rect in the list left 
    4. Delete any rects that move off-screen
"""
import pygame 
from sys import exit
from random import randint

def display_score():
    curr_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'{curr_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return curr_time

def obstacle_movement(obstacle_rects):
    if not obstacle_rects: return []
    for rect in obstacle_rects:
        rect.x -= 5
        if rect.bottom == 300:
            screen.blit(snail_surf, rect)
        else:
            screen.blit(fly_surf, rect)
    
    obstacle_rects = [rect for rect in obstacle_rects if rect.x > -100] 
    
    print(obstacle_rects)
    return obstacle_rects

def player_collision(player, obstacles):
    if not obstacles: return False
    for rect in obstacle_rects:
        if player.colliderect(rect):
            return True
    return False

pygame.init()
pygame.display.set_caption('Game States')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

# Background
sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()

# Obstacles
snail_surf = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
fly_surf = pygame.image.load("tutorial-content/lib/graphics/fly/fly1.png").convert_alpha()
obstacle_rects = []

# Player
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

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)


screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_rect.bottom == 300: player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
 
        if event.type == obstacle_timer and game_active:
            if randint(0, 2): # either 0 or 1
                obstacle_rects.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
            else: 
                obstacle_rects.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.top += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rects = obstacle_movement(obstacle_rects)
        if (player_collision(player_rect, obstacle_rects)): game_active = False

    else:
        obstacle_rects.clear()
        screen.fill((94, 180, 94))
        screen.blit(player_stand, player_stand_rect)
        score_message = pixel_font.render(f"Your score: {score}", False, (111,130,196))
        score_message_rect = score_message.get_rect(center=(400, 40))
        screen.blit(game_name, game_name_rect)
        screen.blit(score_message, score_message_rect)
        screen.blit(game_message, game_message_rect)


    pygame.display.update()
    clock.tick(60)