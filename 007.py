# Rotate Added (Not including overlap check)
import pygame
import sys
import random
import threading
import time

BACKGROUND = (30, 30, 30)
LOCKED = (120, 120, 120)
ACTIVE = (0, 255, 255)

# Board Variables
board_y = 20
board_x = 10
board = []
for y in range(board_y):
    board.append([0] * board_x)

# Screen
length = 25
gap = 5

tab_y = board_y * length + board_y * gap + gap
tab_x = board_x * length + board_x * gap + gap

# Spawn & Pieces & Coords [y][x]
spn_crd = [[1, 0], [1, 1], [1, 2]]
pc_cnt = 4
x_pc = [[0, 0], [0, 1], [0, 2], [1, 3]]
plyr = [[0, 0], [0, 0], [0, 0], [0, 0]]
past = []
lock = threading.Lock()

# Rotation (Coordinate Changes)
chng_sz = 5
chng_bf = []
chng_af = []

plyr_af = [[0, 0], [0, 0], [0, 0], [0, 0]]
for y in range(chng_sz):
    chng_bf.append([0] * chng_sz)
    chng_af.append([0] * chng_sz)

def cln_chng():
    for y in range(chng_sz):
        chng_bf[y] = ([0] * chng_sz)
        chng_af[y] = ([0] * chng_sz)

# Boolean Values
def check_flr():
    return all(plyr[i][0] + 1 < board_y and board[plyr[i][0] + 1][plyr[i][1]] != 1 for i in range(pc_cnt))
def check_l(): #moving -1
    return (all(plyr[i][1] - 1 >= 0 and board[plyr[i][0]][plyr[i][1] - 1] != 1 for i in range(pc_cnt)))
def check_r(): #moving +1
    return (all(plyr[i][1] + 1 < board_x and board[plyr[i][0]][plyr[i][1] + 1] != 1 for i in range(pc_cnt)))
def ln_check(line): # check if lines are full
    return (all(board[line][x] == 1 for x in range(board_x)))

def spawn():
    global past
    for i in range(pc_cnt - 1):
        plyr[i] = list(spn_crd[i])
    
    if not past:
        past = list(x_pc)
        random.shuffle(past)
    plyr[pc_cnt - 1] = list(past.pop(0))

    for i in range(pc_cnt):
        plyr[i][1] += int(board_x/2 - 1)
    
    pc_to_brd(2)

# Save plyr coordinates to the board
def pc_to_brd(typ):
    for i in range(pc_cnt):
        board[plyr[i][0]][plyr[i][1]] = typ

def fall():
    cnt = 0
    while True:
        time.sleep(0.5)
        with lock:
            if check_flr():
                pc_to_brd(0)
                for i in range(pc_cnt):
                    plyr[i][0] += 1
                pc_to_brd(2)
            else:
                pc_to_brd(1)
                brk_ln()
                spawn()

def move(drc):
    with lock:
        if drc == 0:
            if check_l():
                pc_to_brd(0)
                for i in range(pc_cnt):
                    plyr[i][1] -= 1
                pc_to_brd(2)

        elif drc == 1:
            if check_r():
                pc_to_brd(0)
                for i in range(pc_cnt):
                    plyr[i][1] += 1
                pc_to_brd(2)

        elif drc == 2:
            if check_flr():
                pc_to_brd(0)
                for i in range(pc_cnt):
                    plyr[i][0] += 1
                pc_to_brd(2)
            else:
                pc_to_brd(1)
                brk_ln()
                spawn()

def brk_ln():
    for y in range(board_y):
        if ln_check(y):
            for i in range(y, -1, -1):
                board[i] = board[i - 1]
            board[0] = [0] * board_x

def rotate():
    with lock:
        pc_to_brd(0)
        for i in range(pc_cnt):
            chng_bf[2 - (plyr[1][0] - plyr[i][0])][2 - (plyr[1][1] - plyr[i][1])] = i + 1
        for y in range(chng_sz):
            for x in range(chng_sz):
                chng_af[y][x] = chng_bf[x][chng_sz - y - 1]
        for y in range(chng_sz):
            for x in range(chng_sz):
                if chng_af[y][x] != 0:
                    plyr[chng_af[y][x] - 1] = [plyr[1][0] + (2 - y), plyr[1][1] + (2 - x)]
        pc_to_brd(2)

            
        for i in range(chng_sz):
            print(chng_bf[i])
        print()
        for i in range(chng_sz):
            print(chng_af[i])
        print()

        cln_chng()

def main():
    pygame.init()
    pygame.display.set_caption("Tetris 007")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)

    spawn()
    bg_thread = threading.Thread(target=fall, daemon=True)
    bg_thread.start()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move(0)
                if event.key == pygame.K_RIGHT:
                    move(1)
                if event.key == pygame.K_DOWN:
                    move(2)
                if event.key == pygame.K_SPACE:
                    rotate()
        
        screen.fill((10, 10, 10))

        with lock:
            for y in range(board_y):
                for x in range(board_x):
                    X = x * (length + gap) + gap
                    Y = y * (length + gap) + gap

                    if board[y][x] == 0:
                        pygame.draw.rect(screen, BACKGROUND, [X, Y, length, length], border_radius = 5)
                    if board[y][x] == 1:
                        pygame.draw.rect(screen, LOCKED, [X, Y, length, length], border_radius = 5)
                    if board[y][x] == 2:
                        pygame.draw.rect(screen, ACTIVE, [X, Y, length, length], border_radius = 5)
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()