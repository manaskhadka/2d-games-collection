"""
A 2D vertical endless runner in pygame.
"""
import pygame 
from sys import exit
from random import randint
from shared import *
from enum import Enum

class Drill(Player):
    def __init__(self, frames : list, scale : int):
        super().__init__(frames, scale)
        self.dimensions = (self.image.get_size())
        self.x_input = False
        self.vel_x = 0
        self.start_coord = (WINDOW_WIDTH/2 - self.dimensions[0], game_settings["max_y_ofs_up"])
        self.rect = self.image.get_rect(topleft=self.start_coord)

        # Animation logic on hit
        self.hit = False
        self.num_iframes = 0
        self.damage_frames = []
        self.dmg_frame_index = 0  

        for img in self.frames:
            cpy = img.copy()
            cpy_t = cpy.copy()
            cpy_t.set_alpha(40)
            self.damage_frames.extend([cpy, cpy_t])
                
    def player_input(self):
        # UP, DOWN: move player position directly
        # LEFT, RIGHT: update player velocity
        curr_y_ofs = self.rect.y - self.start_coord[1]
        y_limit_up = game_settings["max_y_ofs_up"]
        y_limit_down = game_settings["max_y_ofs_down"]
        vel_limit = game_settings["vel_limit"]
        vel_increment = game_settings["vel_increment"]
        y_increment = game_settings["y_pos_increment"]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if (curr_y_ofs > -1*y_limit_up):
                self.rect.y -= y_increment
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if (curr_y_ofs < y_limit_down):
                self.rect.y += y_increment
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if (self.vel_x > -1*vel_limit):
                self.vel_x -= vel_increment
                self.x_input = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if (self.vel_x < vel_limit):
                self.vel_x += vel_increment  
                self.x_input = True

    def decelerate(self):
        # Reduce velocity when player is not controlling it
        if (not self.x_input):
            dec = game_settings["vel_decrement"]
            if (self.vel_x < 0):
                self.vel_x += dec 
            else:
                self.vel_x -= dec
        self.x_input = False

    def apply_velocity(self):
        self.rect.x += self.vel_x
        if self.rect.left < LEFT_BOUND:
            self.rect.left = LEFT_BOUND
        if self.rect.right > RIGHT_BOUND:
            self.rect.right = RIGHT_BOUND
    
    def animation_apply_rotate(self):
        # Rotate drill based on its x velocity
        angle = int(50 * (self.vel_x / game_settings["vel_limit"]))
        if (abs(angle) > 1):
            # Avoid jitter
            self.image = pygame.transform.rotate(self.image, angle)

    def dmg_animation_state(self):
        self.dmg_frame_index += 0.1 * int(len(self.damage_frames) / len(self.frames))
        if self.dmg_frame_index >= len(self.damage_frames):
            self.dmg_frame_index = 0
        img = self.damage_frames[int(self.dmg_frame_index)]
        self.image = pygame.transform.scale_by(img, self.scale)
        self.num_iframes -= 1
        if (self.num_iframes <= 0): self.hit = False

    def update(self):
        self.player_input()
        self.decelerate()
        self.apply_velocity()
        if (self.hit):
            self.dmg_animation_state()
        else:
            self.animation_state()
        self.animation_apply_rotate()
        

class Enemy(Player):
    max_y_ofs = 50
    move_speed = 1
    osc_freq = 50
    def __init__(self, frames : list, scale : int, e_type : str, 
                 spawn_coord : tuple, facing : str):
        super().__init__(frames, scale)
        self.type = e_type
        self.origin = spawn_coord
        self.facing = facing
        self.rect = self.image.get_rect(center=spawn_coord)
        # Only for mole:
        self.movement_counter = 0
        self.vert_speed = 2
    
    def flip_self(self):
        if (self.facing == "right"):
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def movement(self):
        direction = -1 if (self.facing == "left") else 1
        if self.type == "worm":
            self.rect.x += direction * Enemy.move_speed
            self.rect.y -= game_settings["scroll_speed"]
        else:
            if (self.movement_counter >= Enemy.osc_freq):
                self.movement_counter = 0
                self.vert_speed *= -1
            self.rect.x += direction * Enemy.move_speed
            self.rect.y += self.vert_speed
            self.movement_counter += 1
            self.rect.y -= game_settings["scroll_speed"]
    
    def destroy(self):
        if self.rect.y <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.flip_self()
        self.movement()
        self.destroy()


class Gemtype(Enum):
    AMETHYST = 0
    SAPPHIRE = 1
    EMERALD = 2 
    RUBY = 4


class Gem(PointObject):
    emerald = pygame.image.load("lib/graphics/drill-game/gem1.png").convert_alpha()
    amethyst = pygame.image.load("lib/graphics/drill-game/gem2.png").convert_alpha()
    ruby = pygame.image.load("lib/graphics/drill-game/gem3.png").convert_alpha()
    sapphire = pygame.image.load("lib/graphics/drill-game/gem4.png").convert_alpha()
    gems = [amethyst, sapphire, emerald, ruby]
    def __init__(self, scale : int, gemtype : Gemtype):
        frames = [Gem.gems[gemtype]] # Singular Frame
        super().__init__(frames, scale)
        w, h = self.image.get_size()
        origin = (randint(w, WINDOW_WIDTH - w), WINDOW_HEIGHT + 2*h)
        self.rect = self.image.get_rect(topleft=origin)
        self.gemtype = gemtype

    def destroy(self):
        if (self.rect.y <= -100):
            self.kill()

    def update(self):
        self.rect.y -= game_settings["scroll_speed"]


def spawn_enemy(e_type : str, facing : str) -> Enemy:
    frames = [mole_1, mole_2] if e_type == "mole" else [worm_1, worm_2]
    if (facing == "right"):
        coords = (-100, randint(WINDOW_HEIGHT - 50, WINDOW_HEIGHT + 150))
    else:
        coords = (WINDOW_WIDTH + 100, randint(WINDOW_HEIGHT - 50, WINDOW_HEIGHT + 150))
    return Enemy(frames, scale, e_type, coords, facing)


def collide_enemy():
    if (player.sprite.hit): return
    # We want more precise hit detection for this (using masks)
    hits = pygame.sprite.spritecollide(player.sprite, enemies, dokill=False)
    for sprite in hits:
        if (pygame.sprite.collide_mask(player.sprite, sprite)):
            drill = player.sprite
            # Update vars associated with player damage
            drill.hit = True
            # TODO: Figure out a better way to give 3 seconds of invulnerability:
            drill.num_iframes = 60 * 3
            drill.dmg_frame_index = int(drill.frame_index * 2)


def collide_valuable():
    hits = pygame.sprite.spritecollide(player.sprite, valuables, dokill=True)
    for gem in hits:
        print(f"Player hit: gem {gem.gemtype}")


# Track game states and other info
game_tracker = {
    "game_active": True,
    "game_paused": False,
    "score": 0,
    "high_score": 0
}

# Game settings
default_game_settings = {
    "vel_limit" : 7,
    "vel_increment" : 0.35,
    "vel_decrement" : 0.15,
    "max_y_ofs_up" : 50,
    "max_y_ofs_down" : 350,
    "y_pos_increment" : 5,
    "scroll_speed" : 1
}

game_settings = default_game_settings.copy()

# Player init
drill_1 = pygame.image.load("lib/graphics/drill-game/drill1.png").convert_alpha()
drill_2 = pygame.image.load("lib/graphics/drill-game/drill2.png").convert_alpha()
drill_3 = pygame.image.load("lib/graphics/drill-game/drill3.png").convert_alpha()
drill_frames = [drill_1, drill_2, drill_3]
scale = 2.5
drill = Drill(drill_frames, scale=scale)
player = pygame.sprite.GroupSingle(drill)
LEFT_BOUND = drill.dimensions[0]
RIGHT_BOUND = WINDOW_WIDTH - drill.dimensions[0]

# Enemies & Valuabes init
mole_1 = pygame.image.load("lib/graphics/drill-game/mole1.png").convert_alpha()
mole_2 = pygame.image.load("lib/graphics/drill-game/mole2.png").convert_alpha()
worm_1 = pygame.image.load("lib/graphics/drill-game/worm1.png").convert_alpha()
worm_2 = pygame.image.load("lib/graphics/drill-game/worm2.png").convert_alpha()
enemies = pygame.sprite.Group()
valuables = pygame.sprite.Group()

# Background init
block_1 = pygame.image.load("lib/graphics/drill-game/dirt1.png").convert_alpha()
block_2 = pygame.image.load("lib/graphics/drill-game/dirt2.png").convert_alpha()
block_3 = pygame.image.load("lib/graphics/drill-game/dirt3.png").convert_alpha()
block_4 = pygame.image.load("lib/graphics/drill-game/dirt4.png").convert_alpha()
background = GridBackground(block_1.get_size()[0], scale)
background.add_blocks((block_1, 80), (block_2, 30), (block_3, 40), (block_4, 5))
background.init_background(20)

pause_screen = PauseScreen(screen)

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_tracker["game_active"]:
            if event.type == obstacle_timer:
                facing = "left" if randint(0, 1) else "right"
                enemy = "worm" if randint(0, 1) else "mole"
                enemies.add(spawn_enemy(enemy, facing))
                valuables.add(Gem(scale, randint(0, len(Gem.gems)-1)))

    if game_tracker["game_active"]:
        background.draw(screen)
        background.update()
        valuables.draw(screen)
        valuables.update()
        enemies.draw(screen)
        enemies.update()
        player.draw(screen)
        player.update()

        # Collisions
        collide_valuable()
        collide_enemy()

        wall = pygame.Surface((drill.dimensions[0], WINDOW_HEIGHT))
        wall_rect = wall.get_rect(bottomright=(LEFT_BOUND, WINDOW_HEIGHT))
        wall_rect2 = wall.get_rect(bottomleft=(RIGHT_BOUND, WINDOW_HEIGHT))
        wall.fill("black")
        screen.blit(wall, wall_rect)
        screen.blit(wall, wall_rect2)

    else:
        # Game over
        pass

    pygame.display.update()
    clock.tick(60)
