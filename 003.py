# Falling Function Added
import pygame
import sys
import random


# Board Variables
board_y = 10
board_x = 10

board = []

for y in range(board_y):
    board.append([0] * board_x)

# Spawn & Pieces [y][x]
spn_crd = [[1, 0], [1, 1], [1, 2]]
pc_cnt = 4
x_pc = [[0, 0], [0, 1], [0, 2], [1, 3]]

plyr = [[0, 0], [0, 0], [0, 0], [0, 0]]

def spawn():
    for i in range(pc_cnt - 1):
        plyr[i] = spn_crd[i]
    
    plyr[pc_cnt - 1] = random.choice(x_pc)

    for i in range(pc_cnt):
        plyr[i][1] += int(board_y/2 - 1)

# Save plyr coordinates to the board
def pc_to_brd(typ):
    for i in range(pc_cnt):
        board[plyr[i][0]][plyr[i][1]] = typ

# Boolean Values
pc1 = (board[plyr[0][0]][plyr[0][1]] != 1)
pc2 = (board[plyr[1][0]][plyr[1][1]] != 1)
pc3 = (board[plyr[2][0]][plyr[2][1]] != 1)
pc4 = (board[plyr[3][0]][plyr[3][1]] != 1)

def fall():
    if pc1 & pc2 & pc3 & pc4:
        pc_to_brd(0)
        for i in range(pc_cnt):
            plyr[i][0] += 1
        pc_to_brd(2)

spawn()
pc_to_brd(2)

for y in range(board_y):
    print(board[y])

fall()

print()

for y in range(board_y):
    print(board[y])