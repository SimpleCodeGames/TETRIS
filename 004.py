# Auto Falling Added
import pygame
import sys
import random
import threading
import time


# Board Variables
board_y = 10
board_x = 10
board = []
for y in range(board_y):
    board.append([0] * board_x)

# Spawn & Pieces & Coords [y][x]
spn_crd = [[1, 0], [1, 1], [1, 2]]
pc_cnt = 4
x_pc = [[0, 0], [0, 1], [0, 2], [1, 3]]
plyr = [[0, 0], [0, 0], [0, 0], [0, 0]]

def spawn():
    for i in range(pc_cnt - 1):
        plyr[i] = list(spn_crd[i])
    
    plyr[pc_cnt - 1] = list(random.choice(x_pc))

    for i in range(pc_cnt):
        plyr[i][1] += int(board_y/2 - 1)
    
    pc_to_brd(2)

# Save plyr coordinates to the board
def pc_to_brd(typ):
    for i in range(pc_cnt):
        board[plyr[i][0]][plyr[i][1]] = typ

def fall():
    cnt = 0
    while True:
        time.sleep(0.5)
        # Boolean Values
        if all(plyr[i][0] + 1 < board_y and board[plyr[i][0] + 1][plyr[i][1]] != 1 for i in range(pc_cnt)):
            pc_to_brd(0)
            for i in range(pc_cnt):
                plyr[i][0] += 1
            pc_to_brd(2)
        else:
            pc_to_brd(1)
            spawn()

def main():
    spawn()
    bg_thread = threading.Thread(target=fall, daemon=True)
    bg_thread.start()
    
    for i in range(15):
        time.sleep(0.5)
        for y in range(board_y):
            print(board[y])
        print()

if __name__ == '__main__':
    main()