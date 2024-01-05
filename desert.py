import pygame
import os
from shared import *
from pytmx.util_pygame import load_pygame

tmx_data = load_pygame("C:/Users/manaz/Desktop/Work/Game-Tinker/Tiled/Desert Game/test-level.tmx")
SCALE = 2.5     # scale to apply before rendering anything 
TILESIZE = 16   # tiles are 16 x 16 pixels

game_settings = {
    "p_movespeed": 0.8,         # Player left / right movespeed
    "jump_init_vel": -2.5,      # Controls min jump height
    "jump_force": -0.030,       # Adds to jump height if jump button held
    "jump_time": 60,            # Num frames jump_force can be applied (subtracted by jump_wait)
    "jump_wait": 30,            # Number of frames before jump_force can be applied
    "gravity_acc": 0.025        # Applies continual downward force
}

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, SCALE)
        self.rect = self.image.get_rect(topleft=pos)

class BGTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, SCALE)
        self.rect = self.image.get_rect(topleft=pos)


class DesertPlayer(Player):
    def __init__(self):
        idle_frames = []
        self.run_frames = []
        self.run_f_index = 0
        self.jump_frames = []
        self.jump_f_index = 0
        
        for filename in os.scandir("lib/graphics/desert-game/idle-frames"):
            idle_frames.append(pygame.image.load(filename.path))
        
        for filename in os.scandir("lib/graphics/desert-game/run-frames"):
            self.run_frames.append(pygame.image.load(filename.path))
    
        super().__init__(frames=idle_frames, scale=SCALE)
        obj = tmx_data.get_object_by_name("Player")
        self.start_pos = (obj.x*SCALE, obj.y*SCALE)
        self.rect = self.image.get_rect(topleft=self.start_pos)
        self.jumping = True 
        self.jump_counter = 0
        self.jump_pause = 0
        self.running = False
        self.facing_left = False
        self.curr_pos = pygame.Vector2(self.start_pos)
        self.velocity = pygame.Vector2()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Make player jump
            if (not self.jumping):
                self.jumping = True
                self.velocity.y = game_settings["jump_init_vel"]
                self.jump_counter = game_settings["jump_time"]
                self.jump_pause = game_settings["jump_wait"]
            
            # Make jump bigger if the button is held down in the air
            elif (self.jumping and self.jump_counter > 0 and self.jump_pause == 0):
                print("jf")
                self.velocity.y += game_settings["jump_force"]

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.curr_pos.x -= game_settings["p_movespeed"]
            self.running = True
            self.facing_left = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.curr_pos.x += game_settings["p_movespeed"]
            self.running = True
            self.facing_left = False
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            # TODO: Pan camera up
            pass
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # TODO: Pan camera down
            pass
        else:
            self.running = False 
        
    
    def apply_physics(self):
        # Updates the current position vector using velocity vector
        self.curr_pos.y += self.velocity.y
        # Velocity should increase if negative 
        if (self.jumping):
            self.velocity.y += 0.03
            if (self.jump_pause > 0): self.jump_pause -= 1
            self.jump_counter -= 1

        if (self.velocity.y > 0.01 and self.velocity.y < 0.01):
            self.velocity.y = 0

        if (self.curr_pos.y > 480): 
            self.curr_pos.y = 480
            self.jumping = False
            self.jump_counter = 0
        
        self.rect.y = self.curr_pos.y
        self.rect.x = self.curr_pos.x


    def jump_animation_state(self, speed_inc):
        return 
    
    def run_animation_state(self, speed_inc):
        self.run_f_index += speed_inc
        if self.run_f_index >= len(self.frames):
            self.run_f_index = 0
        img = self.run_frames[int(self.run_f_index)]
        self.image = pygame.transform.scale_by(img, self.scale)

    def animate(self):
        if (self.jumping):
            self.jump_animation_state(speed_inc=0.1)
        if (self.running):
            self.run_animation_state(speed_inc=0.025)
        else:
            self.idle_animation_state(speed_inc=0.005)
        
        if (self.facing_left): 
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
    
    def update(self):
        self.animate()
        self.player_input()
        self.apply_physics()

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


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")
    
    bg_group.draw(screen)
    platform_group.draw(screen)
    player_group.draw(screen)
    player_group.update()

    pygame.display.update()
    # clock.tick(60)
    