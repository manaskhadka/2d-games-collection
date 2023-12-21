"""
A recreation of the game snake in pygame.
"""
import pygame 
from sys import exit
from random import randint, choice

class Board():
    """
    A class to represent the board, including the snake, fruit, and empty squares.

    ...

    Attributes
    ----------
    direction : str
        current direction the head of the snake is pointing
    head : Cell
        cell representing the head of the snake
    tail : Cell
        cell representing the tail of the snake
    body : list(Cell)
        list containing all the cells representing the snake (except the head)
    fruit : list(Cell)
        list containing all the cells representing fruit
    num_rows : int 
        number of cells making the width of the board
    num_cols: int 
        number of cells making the height of the board
    grid : list(pygame.Sprite.Group(Cell))
        representation of the board in a 2D array
    
    Methods
    -------
    player_input()
        Updates direction depending on user key input
    init_board()
        Initializes the board with Cells
    init_snake()
        Initializes the head of the snake
    move_snake()
        Moves the snake based on direction
    get_cell(grid_coord)
        Returns a Cell object given its grid coords
    spawn_fruit()
        Adds a fruit to a random open Cell on the grid
    print()
        Prints debug info
    update()
        Refreshes board display and updates game state logic
    """
    def __init__(self):
        """
        Constructor for Board 
        """
        super().__init__()
        # Snake info
        self.input_direction = "right"
        self.facing = "right"
        self.head = None
        self.tail = None
        self.body = [] 
        self.fruit = [] # contains the cells that are to be collected

        # Grid info
        self.num_rows = 0
        self.num_cols = 0
        self.grid = [] # contains groups of sprites (each group is a column)

    def player_input(self):
        """
        """
        keys = pygame.key.get_pressed()
        adjacent_snake_cell = ""
        if (self.tail):
            adjacent_snake_cell = get_opposite_direction(self.facing)
        if keys[pygame.K_w] or keys[pygame.K_UP] and adjacent_snake_cell != "up":
            self.input_direction = "up"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT] and adjacent_snake_cell != "left":
            self.input_direction = "left"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN] and adjacent_snake_cell != "down":
            self.input_direction = "down"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and adjacent_snake_cell != "right":
            self.input_direction = "right"
            
    def init_board(self):
        counter_y = 0
        for y in range(100, WINDOW_HEIGHT - 100, block_size):
            counter_x = 0
            group = pygame.sprite.Group()
            for x in range(100, WINDOW_WIDTH - 100, block_size):
                cell = Cell((x, y))
                cell.grid_coord = (counter_x, counter_y)
                print(cell.grid_coord)
                group.add(cell)
                counter_x += 1
            counter_y += 1
            self.grid.append(group)

        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])

    def init_snake(self):
        # Put the head of the snake ~halfway down, and ~1/3 from the left
        start_row = int(self.num_rows / 2)
        start_col = int(self.num_cols / 3)
        start_cell = self.get_cell((start_row, start_col))
        start_cell.is_head = True
        self.head = start_cell
    
    def move_snake(self):
        # Move the snake in the direction that the head is facing
        self.facing = self.input_direction
        x, y = self.head.grid_coord
        end = None
        if self.input_direction == "up":
            end = (x, y - 1)
        elif self.input_direction == "left":
            end = (x - 1, y)
        elif self.input_direction == "down":
            end = (x, y + 1)
        elif self.input_direction == "right":
            end = (x + 1, y)
        
        # Wall collision
        if (check_wall_collision(end, self.num_rows, self.num_cols)):
            # End game 
            print("WALL COLLISION")
            return
                
        dest_cell = self.get_cell(end)
        # Body collision
        if (dest_cell.is_body):
            print("BODY COLLISION")
            return 

        # Fruit collisions: Body doesn't need to be moved
        elif (dest_cell.is_fruit):
            print("FRUIT COLLISION")
            # Update the colliding cells
            # score += 1
            old_head = self.head
            old_head.is_head = False 
            old_head.is_body = True
            dest_cell.is_head = True
            dest_cell.is_fruit = False
            self.fruit.remove(dest_cell)
            # Update snake struct
            self.head = dest_cell 
            if (not self.tail):
                self.tail = old_head
            else:
                self.body.append(old_head)
            return
        
        # Body movement: delete the tail and extend the head
        old_head = self.head
        old_head.is_head = False 
        new_head = self.get_cell(end)
        new_head.is_head = True 
        self.head = new_head
        if (self.tail):
            if (not self.body):
                # Move the tail to the old head
                old_tail = self.tail
                old_tail.is_body = False
                old_head.is_body = True
                self.tail = old_head
            else:
                # Delete the tail, let the next body part be the tail. Append the old head to the body
                old_tail = self.tail 
                old_tail.is_body = False 
                self.tail = self.body.pop(0)
                old_head.is_body = True
                self.body.append(old_head)

    def get_cell(self, grid_coord):
        g = self.grid[grid_coord[1]]
        cell = g.sprites()[grid_coord[0]]
        return cell

    def spawn_fruit(self):
        if self.fruit: # if the list is not empty
            return

        free_cells = []
        for g in self.grid:
            sprites = g.sprites()
            for cell in sprites:
                if not cell.is_body and not cell.is_head:
                    free_cells.append(cell)
        
        chosen_cell = choice(free_cells)
        chosen_cell.is_fruit = True 
        self.fruit.append(chosen_cell)
        return chosen_cell
        
    def print(self):
        print(f"rows, col: {self.num_rows}, {self.num_cols}")
        
    def update(self):
        self.spawn_fruit()
        self.move_snake()
        for g in self.grid:
            g.update()


class Cell(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        surface = pygame.Surface((block_size - cell_spacing, 
                                  block_size - cell_spacing))
        self.image = surface
        self.rect = self.image.get_rect(center=coord)
        self.is_body = False         # Track if this cell is part of the body (does not include head)
        self.is_head = False         # Track if this cell is the head of the snake
        self.is_fruit = False        # Track if this cell holds a fruit
        self.grid_coord = None       # The coordinate of this cell in the 2D array
    
    def update(self):
        if (self.is_head):
            self.image.fill("Blue")
        elif (self.is_body):
            self.image.fill("Gray")
        elif (self.is_fruit):
            self.image.fill("Red")
        else:
            self.image.fill("Pink")

def check_wall_collision(coord: tuple, num_rows: int, num_cols: int) -> bool:
    '''
    
    '''
    # NOTE: Possible to allow for wall-to-wall warping using -1 due to python list indexing
    y, x = coord
    if (x >= num_rows) or (y >= num_cols):
        return True
    elif (x < 0) or (y < 0):
        return True 
    return False


def get_opposite_direction(direction):  
    if direction == "left":
        return "right"
    elif direction == "right":
        return "left"
    elif direction == "up":
        return "down"
    else:
        return "up"

# Init
pygame.init()
pygame.display.set_caption('Snake')
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("tutorial-content/lib/font/Pixeltype.ttf", 50)

# Game trackers
game_active = False
start_time = 0
score = 0

# Game settings
speed_coeff = 8
block_size = 25
cell_spacing = int(block_size/10)

# Game init
board = Board()
board.init_board()
board.init_snake()
board.print()

# Timers
movement_timer = pygame.USEREVENT + 1
pygame.time.set_timer(movement_timer, int(1000 / speed_coeff))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == movement_timer:
            board.update()

    board.grid[0].draw(screen)
    for group in board.grid:
        group.draw(screen)

    board.player_input()
    pygame.display.update()
    clock.tick(60)