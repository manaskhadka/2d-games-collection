import pygame 
from random import randint

# Vars to be used across games
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pixel_font_big = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 80)
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 60)
pixel_font_small = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 30)
pixel_font_small2 = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 45)

class PauseScreen():
    """
    A class to represent the pause screen and any info to be displayed there
    """
    def __init__(self, screen):
        super().__init__()
        WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
        cont_pos = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30)
        quit_pos = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 45)
        self.image = screen
        self.boxes = [cont_pos, quit_pos]
        self.curr_highlighted = 0
        self.selected = False
        
    def player_input(self, game_tracker):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if (self.curr_highlighted > 0): 
                self.curr_highlighted -= 1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if (self.curr_highlighted < len(self.boxes) - 1):
                self.curr_highlighted += 1
        elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            # TODO: add enums for following
            if (self.curr_highlighted == 0):
                game_tracker["game_paused"] = False
            else:
                return -1

    def draw(self):
        self.image.fill("Black")
        pause_img = pixel_font_big.render("PAUSED", False, "White")
        pause_rect = pause_img.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 150))
        cont_img = pixel_font.render("Continue", False, "White")
        cont_rect = cont_img.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 25))
        quit_img = pixel_font.render("Exit to Main Menu", False, "White")
        quit_rect = quit_img.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
        select_box_img = pygame.Surface((500, 60))
        select_box_img.fill("darkgray")
        select_box_rect = select_box_img.get_rect(center=self.boxes[self.curr_highlighted])
        
        self.image.blit(select_box_img, select_box_rect)
        self.image.blit(pause_img, pause_rect) 
        self.image.blit(cont_img, cont_rect)
        self.image.blit(quit_img, quit_rect)
    
    def update(self, game_tracker):
        status = self.player_input(game_tracker)
        self.draw()
        return status


class Player(pygame.sprite.Sprite):
    def __init__(self, frames, scale):
        super().__init__()
        self.scale = scale
        self.frames = frames
        self.frame_index = 0
        self.image = pygame.transform.scale_by(frames[0], self.scale)
        self.rect = self.image.get_rect()
        
    def player_input(self):
        """ TO BE OVERWRITTEN """
        raise NotImplementedError("Player.player_input not overwritten")

    def idle_animation_state(self, speed_inc=0.1):
        # TODO: This works, but is it really a good way to do this? (performance)
        #       ^ Probably not, considering it has eaten upto 5% of my CPU
        self.frame_index += speed_inc
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        img = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale_by(img, self.scale)

    def update(self):
        self.player_input()
        self.idle_animation_state()


class GridBackground():
    def __init__(self, blocksize, scale):
        self.scale = scale
        self.total_weight = 0
        self.grid = []
        self.block_imgs = []
        self.selection_ranges = []
        self.blocksize = blocksize
        self.displacement = 0

        # Used for shading effects for drill game
        self.black_overlay = pygame.surface.Surface((128, 128))
        self.black_overlay.set_alpha(0)
    
    def add_blocks(self, *blocks):
        for block in blocks:
            img = block[0]
            weight = block[1]
            selection_range = (self.total_weight, self.total_weight + weight)
            self.total_weight += weight
            self.block_imgs.append(img)
            self.selection_ranges.append(selection_range)
    
    def choose_block(self):
        # TODO: =( this can be entirely replaced by using built in python .choice method (it allows weighting)
        # TODO: optimize the following to O(log(n)) using bisection on selection_ranges
        selection = randint(0, self.total_weight - 1)
        for i in range(len(self.selection_ranges)):
            elem = self.selection_ranges[i]
            if selection < elem[1]:
                return i

    def init_background(self):
        self.displacement = 0
        self.grid.clear()
        b_size = int(self.blocksize * self.scale)
        for y in range(0, WINDOW_HEIGHT + b_size, b_size):
            group = pygame.sprite.Group()
            for x in range(0, WINDOW_WIDTH, b_size):
                index = self.choose_block()
                cell = GridCell(self.block_imgs[index], (x, y), self.scale)
                group.add(cell)
            self.grid.append(group)
    

    def update_darkness(self, value):
        self.black_overlay.set_alpha(value)
    
    def add_layer(self):
        b_size = int(self.blocksize * self.scale)
        y = WINDOW_HEIGHT
        if (self.displacement >= b_size):
            # delete top layer which is offscreen
            self.grid.pop(0) 
            # add new layer below, offscreen
            group = pygame.sprite.Group()
            for x in range(0, WINDOW_WIDTH, b_size):
                index = self.choose_block()
                cell = GridCell(self.block_imgs[index], (x, y), self.scale)
                cell.image.blit(self.black_overlay, (0, 0))
                group.add(cell)
            self.grid.append(group)
            self.displacement = 0
                
    def draw(self, screen):
        for group in self.grid:
            group.draw(screen)

    def update(self):
        self.add_layer()
        for group in self.grid:
            group.update()
        self.displacement += 1


class GridCell(pygame.sprite.Sprite):
    def __init__(self, image, coord, scale):
        super().__init__()
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect(topleft=coord)
    
    def update(self):
        self.rect.y -= 1
        return


class PointObject(pygame.sprite.Sprite):
    def __init__(self, frames, scale):
        super().__init__()
        self.scale = scale
        self.frames = frames
        self.frame_index = 0
        self.image = pygame.transform.scale_by(frames[0], self.scale)
        self.rect = self.image.get_rect()
    
    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        img = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale_by(img, self.scale)
    
    def update(self):
        self.animation_state()


def draw_score(game_tracker, offset):
    score = game_tracker["score"]
    high_score = game_tracker["high_score"]
    s_image = pixel_font_small.render(f"Score: {score}", False, "gray")
    s_rect = s_image.get_rect(topleft=(offset, 15))
    hs_image = pixel_font_small.render(f"High Score: {high_score}", False, "gray")
    hs_rect = hs_image.get_rect(topright=(WINDOW_WIDTH - offset, 15))
    screen.blit(s_image, s_rect)
    screen.blit(hs_image, hs_rect)

def draw_gameover(screen, color):
    x, y = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    end_text = pixel_font_big.render("GAME OVER", False, color)
    end_text_rect = end_text.get_rect(center=(x, y))
    cont_text = pixel_font_small.render("press SPACE or RETURN to continue", False, color)
    cont_text_rect = cont_text.get_rect(center=(x, y + 40))
    return_text = pixel_font_small.render("press ESC to exit to menu", False, color)
    return_text_rect = return_text.get_rect(center=(x, y + 65))

    screen.blit(end_text, end_text_rect)
    screen.blit(cont_text, cont_text_rect)
    screen.blit(return_text, return_text_rect)