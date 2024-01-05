import pygame
import os
from shared import *
from pytmx.util_pygame import load_pygame

tmx_data = load_pygame("C:/Users/manaz/Desktop/Work/Game-Tinker/Tiled/Desert Game/test-level.tmx")
SCALE = 2.5     # scale to apply before rendering anything 
TILESIZE = 16   # tiles are 16 x 16 pixels

LEFT = -1
RIGHT = 1
NO_INPUT = 0

game_settings = {
    "def_movespeed": 5,     # Player left / right movespeed
    "jump_init_vel": -15,   # Controls min jump height
    "jump_force": -0.8,     # Adds to jump height if jump button held
    "jump_time": 15,        # Num frames jump_force can be applied (subtracted by jump_wait)
    "jump_wait": 5,         # Number of frames before jump_force can be applied
    "gravity_acc": 1,       # Applies continual downward force
    "t_vel": 10             # Limits fall speed
}

game_tracker = {
    "world_shift": 0,
    "player_speed": 0
}

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, SCALE)
        self.rect = self.image.get_rect(topleft=pos)
        self.origin = self.rect.copy()
    
    def update(self, ofs):
        self.rect.x += ofs


class BGTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, SCALE)
        self.rect = self.image.get_rect(topleft=pos)
        self.origin = self.rect.copy()
    
    def update(self, ofs):
        self.rect.x += ofs


class DesertPlayer(Player):
    def __init__(self):
        # Frames
        idle_frames = []
        self.run_frames = []
        self.jump_frames = []
        self.run_f_index = 0
        self.jump_f_index = 0

        for filename in os.scandir("lib/graphics/desert-game/idle-frames"):
            idle_frames.append(pygame.image.load(filename.path))
        for filename in os.scandir("lib/graphics/desert-game/run-frames"):
            self.run_frames.append(pygame.image.load(filename.path))
    
        super().__init__(frames=idle_frames, scale=SCALE)
        obj = tmx_data.get_object_by_name("Player")
        self.start_pos = (obj.x*SCALE, obj.y*SCALE)
        self.rect = self.image.get_rect(topleft=self.start_pos)
        
        # Movement
        self.direction = NO_INPUT
        self.velocity = pygame.Vector2()
        self.airborne = True 
        self.jump_counter = 0
        self.jump_pause = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        # Vertical movement (Jump)
        if keys[pygame.K_SPACE]: self.jump()
        
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = LEFT
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = RIGHT
        else:
            self.direction = NO_INPUT

        # Camera control
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # TODO: Pan camera up
            pass
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # TODO: Pan camera down
            pass
    
    
    def apply_physics(self):
        # Updates the current position vector using velocity vector
        if (self.airborne):
            if self.velocity.y <= game_settings["t_vel"]:
                self.velocity.y += game_settings["gravity_acc"]
            self.jump_pause -= 1
            self.jump_counter -= 1
        else:
            self.velocity.y = 0
        
    def movement(self):
        # Horizontal movement + collisions
        player.rect.x += player.direction * self.velocity.x
        collisions = pygame.sprite.spritecollide(self, platform_group, dokill=False)
        for p in collisions:
            if self.direction == LEFT:
                self.rect.left = p.rect.right
            elif self.direction == RIGHT:
                self.rect.right = p.rect.left

        # Vertical movement + collisions
        self.rect.y += self.velocity.y
        collisions = pygame.sprite.spritecollide(self, platform_group, dokill=False)
        floor_collision = False
        for p in collisions:
            if self.velocity.y >= 0:
                self.airborne = False 
                self.jump_counter = 0
                self.rect.bottom = p.rect.top
                floor_collision = True
            else:
                self.rect.top = p.rect.bottom
                # If you hit your head, you can't extend jump
                self.jump_counter = 0
                self.velocity.y = -0.01  # < 0 due to other collision check
        
        if (not floor_collision): self.airborne = True
        
    def jump(self):
        # Make player jump
        if (not self.airborne):
            self.airborne = True
            self.velocity.y = game_settings["jump_init_vel"]
            self.jump_counter = game_settings["jump_time"]
            self.jump_pause = game_settings["jump_wait"]
        
        # Make jump bigger if the button is held down in the air
        elif (self.airborne and self.jump_counter > 0 and self.jump_pause <= 0):
            self.velocity.y += game_settings["jump_force"]

    def jump_animation_state(self, speed_inc):
        return 
    
    def run_animation_state(self, speed_inc):
        self.run_f_index += speed_inc
        if self.run_f_index >= len(self.frames):
            self.run_f_index = 0
        img = self.run_frames[int(self.run_f_index)]
        self.image = pygame.transform.scale_by(img, self.scale)

    def animate(self):
        if (self.airborne):
            self.jump_animation_state(speed_inc=0.1)
        if (self.direction != NO_INPUT):
            self.run_animation_state(speed_inc=0.15)
        else:
            self.idle_animation_state(speed_inc=0.05)
        
        if (self.direction == LEFT): 
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
    
    def update(self):
        self.animate()
        self.apply_physics()
        self.movement()
        self.player_input()

def scroll_x(player_group):
    player = player_group.sprite
    player_x = player.rect.centerx
    direction_x = player.direction

    if player_x < WINDOW_WIDTH / 4 and direction_x < 0:
        game_tracker["world_shift"] = game_settings["def_movespeed"]
        player.velocity.x = 0
    elif player_x > WINDOW_WIDTH - (WINDOW_WIDTH / 4) and direction_x > 0:
        game_tracker["world_shift"] = -1*game_settings["def_movespeed"]
        player.velocity.x = 0
    else:
        game_tracker["world_shift"] = 0
        player.velocity.x = game_settings["def_movespeed"]

platform_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
player = DesertPlayer()
player_group = pygame.sprite.GroupSingle(player)

for layer in tmx_data.visible_layers:
    # Grab only non object layers
    if hasattr(layer, 'data'):     
        for x, y, surf in layer.tiles():
            pos = (x*TILESIZE*SCALE, y*TILESIZE*SCALE)
            if layer.name == "Platforms":
                Platform(pos=pos, surf=surf, groups=platform_group)
            else:
                BGTile(pos=pos, surf=surf, groups=bg_group)

# Hitbox for debugging:
hb = player_group.sprite.image 
hb.fill("blue")
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")

    # Level tiles
    bg_group.update(game_tracker["world_shift"])
    bg_group.draw(screen)
    platform_group.update(game_tracker["world_shift"])
    platform_group.draw(screen)
    scroll_x(player_group)

    # Player
    player_group.update()
    screen.blit(hb, player_group.sprite.rect)
    player_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
    