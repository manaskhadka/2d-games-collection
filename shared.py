import pygame 

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_OFFSET =  40
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pixel_font_big = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 80)
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 60)
pixel_font_small = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 30)

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
                # TODO: quit to main menu
                print("QUIT PRESSED")
                pass

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
        self.player_input(game_tracker)
        self.draw()

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

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        img = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale_by(img, self.scale)

    def update(self):
        self.player_input()
        self.animation_state()

def draw_score(game_tracker):
    score = game_tracker["score"]
    high_score = game_tracker["high_score"]
    s_image = pixel_font_small.render(f"Score: {score}", False, "gray")
    s_rect = s_image.get_rect(topleft=(WINDOW_OFFSET, 15))
    hs_image = pixel_font_small.render(f"High Score: {high_score}", False, "gray")
    hs_rect = hs_image.get_rect(topright=(WINDOW_WIDTH - WINDOW_OFFSET, 15))
    screen.blit(s_image, s_rect)
    screen.blit(hs_image, hs_rect)