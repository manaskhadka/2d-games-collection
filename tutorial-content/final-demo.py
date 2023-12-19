"""
This is a recreation of the last demo, but made using sprites and OOP.
Also adds music.
NOTE:
    pygame handles spriteworking as follows (simplified):
    1. Create a sprite
    2. Place sprites in a Group or GroupSingle (group for single sprite)
    3. draw/update all sprites in a group at a time
"""
import pygame 
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("tutorial-content/lib/graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("tutorial-content/lib/graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("tutorial-content/lib/graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("tutorial-content/lib/audio/jump.mp3")
        self.jump_sound.set_volume(0.25)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        y_pos = 0
        if (type == "fly"):
            fly_frame_1 = pygame.image.load("tutorial-content/lib/graphics/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("tutorial-content/lib/graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("tutorial-content/lib/graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("tutorial-content/lib/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x < -100:
            self.kill()

def display_score():
    curr_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'{curr_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return curr_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return False
    return True

pygame.init()
pygame.display.set_caption('Dolt Runner')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound("tutorial-content/lib/audio/music.wav")
bg_Music.set_volume(0.20)
bg_Music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load("tutorial-content/lib/graphics/Sky.png").convert()
ground_surface = pygame.image.load("tutorial-content/lib/graphics/ground.png").convert()
obstacle_rects = []

# Intro screen 
player_stand = pygame.image.load("tutorial-content/lib/graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))
game_name =  pixel_font.render("Dolt Runner", False, (111, 130, 196))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = pixel_font.render('Press space to jump', False, (111,130,196))
game_message_rect = game_message.get_rect(center=(400, 325))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

screen.blit(sky_surface, (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if (not game_active):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
    
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2): # either 0 or 1
                    obstacle_group.add(Obstacle("snail"))
                else: 
                    obstacle_group.add(Obstacle("fly"))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        
    else:
        obstacle_group.empty()
        screen.fill((94, 180, 94))
        screen.blit(player_stand, player_stand_rect)
        score_message = pixel_font.render(f"Your score: {score}", False, (111,130,196))
        score_message_rect = score_message.get_rect(center=(400, 40))
        screen.blit(game_name, game_name_rect)
        screen.blit(score_message, score_message_rect)
        screen.blit(game_message, game_message_rect)


    pygame.display.update()
    clock.tick(60)