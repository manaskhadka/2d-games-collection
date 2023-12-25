"""
A 2D vertical endless runner in pygame.
"""
import pygame 
from sys import exit
from math import fabs
from shared import *

class Drill(Player):
    def __init__(self, frames, scale):
        super().__init__(frames, scale)
        self.dimensions = (self.image.get_size())
        self.x_input = False
        self.vel_x = 0
        self.start_coord = (WINDOW_WIDTH/2 - self.dimensions[0], game_settings["max_y_ofs_up"])
        self.rect = self.image.get_rect(topleft=self.start_coord)
        
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

    def update(self):
        self.player_input()
        self.decelerate()
        self.apply_velocity()
        self.animation_state()
        self.animation_apply_rotate()
        

class Enemy(Player):
    def __init__(self, frames, scale):
        super().__init__(frames, scale)

    def player_input(self):
        return
    

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
    "max_y_ofs_down" : 150,
    "y_pos_increment" : 5
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

# Enemies init
mole_1 = pygame.image.load("lib/graphics/drill-game/mole1.png").convert_alpha()
mole_2 = pygame.image.load("lib/graphics/drill-game/mole2.png").convert_alpha()
worm_1 = pygame.image.load("lib/graphics/drill-game/worm1.png").convert_alpha()
worm_2 = pygame.image.load("lib/graphics/drill-game/worm2.png").convert_alpha()
mole_enemy = Enemy([mole_1, mole_2], scale)
worm_enemy = Enemy([worm_1, worm_2], scale)
mole_enemy.rect.center = (100, 300)
worm_enemy.rect.center = (100, 200)
enemies = pygame.sprite.Group()
enemies.add(mole_enemy, worm_enemy)

# Collectables init
gem1 = pygame.image.load("lib/graphics/drill-game/gem1.png").convert_alpha()
gem2 = pygame.image.load("lib/graphics/drill-game/gem2.png").convert_alpha()
gem3 = pygame.image.load("lib/graphics/drill-game/gem3.png").convert_alpha()
gem4 = pygame.image.load("lib/graphics/drill-game/gem4.png").convert_alpha()
gems = [gem1, gem2, gem3, gem4]

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
movement_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(movement_timer, int(1000 / game_settings["speed_coeff"]))

while True:
    background.draw(screen)
    background.update()
    counter = 0
    for gem in gems:
        big = pygame.transform.scale_by(gem, scale)
        screen.blit(big, big.get_rect(center=(300 + 50*counter, 200 + 50*counter)))
        counter += 1
    # screen.fill("brown")
    wall = pygame.Surface((drill.dimensions[0], WINDOW_HEIGHT))
    wall_rect = wall.get_rect(bottomright=(LEFT_BOUND, WINDOW_HEIGHT))
    wall_rect2 = wall.get_rect(bottomleft=(RIGHT_BOUND, WINDOW_HEIGHT))
    wall.fill("black")
    screen.blit(wall, wall_rect)
    screen.blit(wall, wall_rect2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_tracker["game_active"]:
            pass

    if game_tracker["game_active"]:
        hitbox = drill.image.copy()
        # hitbox.fill("blue")
        screen.blit(hitbox, drill.rect)
        enemies.draw(screen)
        enemies.update()
        player.draw(screen)
        player.update()

    
    else:
        # Game over
        pass

    pygame.display.update()
    clock.tick(60)
