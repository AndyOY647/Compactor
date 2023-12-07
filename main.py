import pygame
import random
pygame.init()



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
s_width = 1000
s_height = 768
play_width = 640  # meaning 300 // 10 = 30 width per block
play_height = 640  # meaning 600 // 20 = 20 height per block
block_size = 64

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [[
      '.....',
      '.....',
      '..0..',
      '.....',
      '.....'

]]

B = [[
      '.....',
      '.....',
      '..00.',
      '..00.',
      '.....'
]]

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



shapes = [L,LL, S, B]
shape_colors = [(0, 255, 0), (255, 0, 0), (0,0, 255), (128,128,128)]
shape_images = ['Red_Sprite.png','green_sprite.png','yellow_sprite.png','blue_sprite.png']



# index 0 - 3 represent shape
# 4 shapes


class Piece(object):
    row = 10
    col = 10

    def __init__(self,x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        self.image = pygame.image.load(shape_images[shapes.index(shape)])
        self.image_rect = self.image.get_rect()

    def display(self, surface, image):
        surface.blit(image)



def create_grid(locked_positions={}):
    # creates a black 10 by 10 grid
    grid = [[(0,0,0) for i in range(10)]for i in range(10)]

    for row in range(len(grid)):
        for col in range(len(grid)):
            if(col, row) in locked_positions:
                c = locked_positions[(col,row)]
                grid[row][col] = c
    return grid

def convert_shape_format(shape, surface):
    positions = []
    # Getting the sublist for each rotation
    format = shape.shape[shape.rotation % len(shape.shape)]

    # Checking every line
    for i, line  in  enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x +j, shape.y + i))





    for i , pos in enumerate(positions):
        # offset shape left and up
        positions[i] = pos[0] - 2, pos[1] - 4

    surface.blit(shape.image, positions[i])
    return positions




def valid_space(shape, grid, surface):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape, surface)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    global shapes, shape_colors, shape_images
    c_shape = Piece(3,0, random.choice(shapes))
    return c_shape




def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, row, col):
    # start_pos x, y
    sx = top_left_x
    sy = top_left_y

    # Grid lines
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx+ j *block_size, sy), (sx + j* block_size , sy + play_height))





def clear_rows(grid, locked):
    inc = 0
    #looping the grid backward
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if(0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    #Shifting the row
    # if inc > 0:
    ##############comment###################
    #     #The lambda function returns the second item of the list while looping the list backward
    #     # so we don't overwrite any existing rows
    ###############comment##################
    #     for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
    #         x, y = key
    #         if y < ind:
    #             newKey = (x, y + inc)
    #             locked[newKey] = locked.pop(key)



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 10)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x +play_width
    sy = top_left_y + play_height/2 -100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                #Draw image in the shape form then shift to the side of the screen
                #pygame.draw.rect(surface, shape.color, (sx + j*block_size/2, sy +i *block_size/2, block_size/2, block_size/2), 0)
                surface.blit(shape.image,(sx + j*block_size/2, sy+i *block_size/2, block_size/2, block_size/2))
    surface.blit(label, (sx+70, sy))



def draw_window(surface, grid, shape):
    row = 10
    col = 10
    #currentImage
    c_image = shape.image
    p_image = []



    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Grand9K Pixel', 50)
    label = font.render('Compactor', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #If we need bg color for the block
            # pygame.draw.rect(surface, grid[i][j],
            #                  (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

            # Replace block with asset if not black
            if grid[i][j] != (0,0,0):
                surface.blit(c_image, (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))
            # elif grid[i][j] == (0,0,0):
            #     previous_image = c_image
            #     surface.blit(previous_image, (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))
    # boarder for grid
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    
    draw_grid(surface, row, col)
    #pygame.display.update()

def draw_lock_pos(surface, image, pos):
    surface.blit(image, pos)
def main(win):
    lock_positions = {}
    grid = create_grid(lock_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    previous_piece = current_piece
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.40
    current_piece.x = 4
    level_time = 0
    p_image = []
    while run:
        grid = create_grid(lock_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        p_image.append(current_piece.image)
        
        
        
        
        #Music here
        #################
        if fall_time /1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid, win) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True
                previous_piece = current_piece


        #Key press check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                #Left
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    #check boarder
                    if not(valid_space(current_piece, grid, win)):
                        current_piece.x += 1
                #Right
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid, win)):
                        current_piece.x -= 1
                #Down
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space( current_piece,grid, win)):
                        current_piece.y -= 1
                #UP
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space( current_piece, grid, win)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece, win)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: #If we are not at the top of the grid
                grid[y][x] = current_piece.color #update the color value







        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                lock_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            current_piece.x = 4
            change_piece = False
            clear_rows(grid, lock_positions)


        draw_window(win, grid, current_piece)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost(lock_positions):
            run = False

    pygame.display.quit()


def main_menu(win):

    run = True
    while run:
        win.fill((0,0,0))
        win.blit(menu_bg, (0,-50))


        if start_button.draw():
            print("start is clicked")
            win.blit(start2, (300,300))
            win.blit(credit1, (300,500))
            pygame.display.update()
            pygame.time.delay(300)
            main(win)


        if credit_button.draw():
            win.blit(credit2, (300,500))
            win.blit(start1, (300,300))
            win.fill((0,0,0))
            win.blit(credits, (300,300))
            pygame.display.update()
            pygame.time.delay(2000)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

class Button():
    def __init__(self, x,y, image, scale):

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, ( int(width * scale), int(height * scale) ))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        #check mouse over  and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        win.blit(self.image, (self.rect.x, self.rect.y))

        return action

win = pygame.display.set_mode((s_width, s_height))
#bg and button
menu_bg = pygame.image.load('BGMenu.png').convert_alpha()
start1 = pygame.image.load('Start1.png').convert_alpha()
start2 = pygame.image.load('Start2.png').convert_alpha()
credit1 = pygame.image.load('Credits1.png').convert_alpha()
credit2 = pygame.image.load('Credits2.png').convert_alpha()
credits = pygame.image.load('credits.png').convert_alpha()
credits = pygame.transform.scale(credits, (300,300))

credit_button = Button(300,500, credit1, 1)
start_button = Button(300,300, start1, 1)

pygame.display.set_caption('KillTrash')
main_menu(win)  # start game
