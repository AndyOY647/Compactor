import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid

"""

pygame.font.init()

# GLOBALS VARS
s_width = 768
s_height = 768
play_width = 640  # meaning 300 // 10 = 30 width per block
play_height = 640  # meaning 600 // 20 = 20 height per block
block_size = 64

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

LL = [['.....',
      '.....',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..0..',
      '.....']]

L = [['.....',
      '.....',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '.....',
      '.....']]



shapes = [L,LL]
shape_colors = [(0, 255, 0), (255, 0, 0)]


# index 0 - 1 represent shape
# Only 2 shapes


class Piece(object):
    def __init__(self,x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # creates a black 10 by 10 grid
    grid = [[(0,0,0) for i in range(10)]for i in range[10]]

    for row in range(len(grid)):
        for col in range(len(grid)):
            if(col, row) in locked_positions:
                c = locked_positions[(col,row)]
                grid[row][col] = c
    return grid

def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass


def get_shape():
    return Piece(random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size,block_size),0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height),4)



def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Grand9K Pixel', 32)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    draw_grid(surface, grid)
    pygame.display.update()

def main():
    lock_positions = {}
    grid = create_grid(lock_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                if event.key == pygame.K_UP:
                    current_piece.y -= 1
def main_menu():
    pass


main_menu()  # start game