# Rotation Overlap Check Added
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

# Boolean Values
def check_flr():
    return all(0 <= plyr[i][1] < board_x and plyr[i][0] + 1 < board_y and board[plyr[i][0] + 1][plyr[i][1]] != 1 for i in range(pc_cnt))
def check_l(): #moving -1
    return all(0 <= plyr[i][0] < board_y and plyr[i][1] - 1 >= 0 and board[plyr[i][0]][plyr[i][1] - 1] != 1 for i in range(pc_cnt))
def check_r(): #moving +1
    return all(0 <= plyr[i][0] < board_y and plyr[i][1] + 1 < board_x and board[plyr[i][0]][plyr[i][1] + 1] != 1 for i in range(pc_cnt))
def ln_check(line): # check if lines are full
    return all(board[line][x] == 1 for x in range(board_x))
def check_rt():
    for i in range(pc_cnt):
        dy = plyr[i][0] - plyr[1][0]
        dx = plyr[i][1] - plyr[1][1]
        new_y = plyr[1][0] + dx
        new_x = plyr[1][1] - dy
        
        if not (0 <= new_y < board_y and 0 <= new_x < board_x):
            return False
        if board[new_y][new_x] == 1:
            return False
    return True

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
        if check_rt():
            pc_to_brd(0)
            temp_plyr = []
            for i in range(pc_cnt):
                dy = plyr[i][0] - plyr[1][0]
                dx = plyr[i][1] - plyr[1][1]
                new_y = plyr[1][0] + dx
                new_x = plyr[1][1] - dy
                temp_plyr.append([new_y, new_x])
            for i in range(pc_cnt):
                plyr[i] = temp_plyr[i]
            pc_to_brd(2)

def main():
    pygame.init()
    pygame.display.set_caption("Tetris 009")
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