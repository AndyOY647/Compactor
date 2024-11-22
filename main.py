import pygame
import random
pygame.init()

pygame.mixer.init()

row_clear_sound = pygame.mixer.Sound('KillTrash/Balloon_pop.mp3')
pygame.mixer.music.load('KillTrash/Melody_energy.mp3')
gameOver = pygame.mixer.Sound('KillTrash/game_over.wav')
yay = pygame.mixer.Sound('KillTrash/Yay.mp3')


window_img = pygame.image.load('KillTrash/window.png')
window_img = pygame.transform.scale(window_img, (200,200))
firework = pygame.image.load('KillTrash/firework.jpg')
firework = pygame.transform.scale(firework, (1000,768))


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
shape_images = ['KillTrash/Red_Sprite.png','KillTrash/green_sprite.png','KillTrash/yellow_sprite.png','KillTrash/blue_sprite.png']




    # pygame.transform.scale(bg_images[image], (1000,1000))



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

def get_image(sheet, frame, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame*width), 0, width,height))
    image = pygame.transform.scale(image,  (s_width,s_height))

    return image
def create_grid(locked_positions={}):
    # creates a black 10 by 10 grid
    grid = [[(0,0,0) for i in range(10)]for i in range(10)]

    for row in range(len(grid)):
        for col in range(len(grid)):
            if(col, row) in locked_positions:
                c = locked_positions[(col,row)]
                grid[row][col] = c
    return grid


        # surface.blit(loaded , (0,0))



def convert_shape_format(shape):
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

   
    return positions




def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
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
    global shapes, shape_colors
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
                    pygame.mixer.music.pause()
                    row_clear_sound.set_volume(0.05)
                    pygame.mixer.Sound.play(row_clear_sound)
                    pygame.mixer.music.play(10)
                    del locked[(j,i)]
                except:
                    continue


    if inc > 0:
    ##############comment###################
    #     #The lambda function returns the second item of the list while looping the list backward
    #     # so we don't overwrite any existing rows
    ###############comment##################
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                # Shifting the row
                #locked[newKey] = locked.pop(key)
    return inc



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 18)
    label = font.render('Next Shape', 1, (0,0,0))

    sx = top_left_x +play_width
    sy = top_left_y + play_height/2 -100

    format = shape.shape[shape.rotation % len(shape.shape)]

    surface.blit(window_img, (sx-10, sy-20))
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                #Draw image in the shape form then shift to the side of the screen
                #pygame.draw.rect(surface, shape.color, (sx + j*block_size/2, sy +i *block_size/2, block_size/2, block_size/2), 0)

                surface.blit(shape.image,(sx + j*block_size/2, sy+i *block_size/2, block_size/2, block_size/2))
    surface.blit(label, (sx+55, sy+20))




def draw_window(surface, grid, shape, score=0):
    row = 10
    col = 10
    p_list = []
    #currentImage
    c_image = shape.image
    p_list.append(c_image)


    pygame.font.init()
    font = pygame.font.SysFont('Grand9K Pixel', 50)
    title = pygame.image.load("KillTrash/Title.png")

    surface.blit(title, (top_left_x + play_width / 2 - (title.get_width() / 2), -70))



    sx = top_left_x + play_width
    sy = top_left_y + play_height / 2 - 100

    font = pygame.font.SysFont('Sharpe Sans', 50)
    label = font.render('Score: ' + str(score), 1, (57, 74, 160))
    label2 = font.render('Score: ' + str(score), 1, (255, 238, 0))


    surface.blit(label, (sx-800, sy+98))
    surface.blit(label2, (sx - 800, sy + 102))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #If we need bg color for the block
            # pygame.draw.rect(surface, grid[i][j],
            #                  (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

            # Replace block with asset if not black
            if grid[i][j] in shape_colors:
                surface.blit(c_image, (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))
            # elif grid[i][j] == (0,0,0):
            #     previous_image = c_image
            #     surface.blit(previous_image, (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))
    # boarder for grid
            pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    
    draw_grid(surface, row, col)
    #pygame.display.update()


def main(win):
    lock_positions = {}
    grid = create_grid(lock_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.40
    current_piece.x = 4
    level_time = 0
    p_list = []
    piece_in_pList = 0
    bg_animation = []
    animation_steps = 8
    last_update = pygame.time.get_ticks()
    cooldown = 250
    frame = 0
    score = 0
    win.fill((0, 0, 0))
    for x in range(animation_steps):
        bg_animation.append(get_image(bg_image, x, 500, 1000))

    while run:
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(bg_animation):
                frame = 0

        win.blit(bg_animation[frame], (0, 0))

        grid = create_grid(lock_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time /1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True


        #Key press check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu(win)
            if event.type == pygame.KEYDOWN:
                #Left
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    #check boarder
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                #Right
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                #Down
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y -= 1
                #UP
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: #If we are not at the top of the grid
                grid[y][x] = current_piece.color #update the color value


        if change_piece:
            p_list.append(current_piece.image)
            for pos in shape_pos:
                p = (pos[0], pos[1])
                lock_positions[p] = current_piece.color

            current_piece = next_piece
            next_piece = get_shape()
            current_piece.x = 4
            change_piece = False
            score += clear_rows(grid, lock_positions) * 10


        draw_window(win, grid, current_piece, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost(lock_positions):
            run = False
            pygame.mixer.music.stop()
            gameOver.set_volume(0.1)
            pygame.mixer.Sound.play(gameOver)
            pygame.time.delay(4000)

    main_menu(win)


def main_menu(win):

    run = True
    while run:
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        win.blit(menu_bg, (0,-50))


        if start_button.draw():
            win.blit(start2, (300,300))
            win.blit(credit1, (300,500))
            pygame.display.update()
            pygame.time.delay(300)
            main(win)


        if credit_button.draw():

            win.blit(credit2, (300,500))
            win.blit(start1, (300,300))
            win.blit(firework, (0, 0))
            win.blit(credits, (250,100))
            pygame.mixer.music.stop()
            yay.set_volume(0.1)
            pygame.mixer.Sound.play(yay)
            pygame.display.update()
            pygame.time.delay(5000)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

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
bg_image = pygame.image.load('KillTrash/bg_image.png').convert_alpha()
menu_bg = pygame.image.load('KillTrash/BGMenu.png').convert_alpha()
start1 = pygame.image.load('KillTrash/Start1.png').convert_alpha()
start2 = pygame.image.load('KillTrash/Start2.png').convert_alpha()
credit1 = pygame.image.load('KillTrash/Credits1.png').convert_alpha()
credit2 = pygame.image.load('KillTrash/Credits2.png').convert_alpha()
credits = pygame.image.load('KillTrash/credits.png').convert_alpha()
credits = pygame.transform.scale(credits, (500,500))

credit_button = Button(300,500, credit1, 1)
start_button = Button(300,300, start1, 1)

pygame.display.set_caption('Compactor')
main_menu(win)  # start game
