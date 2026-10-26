# Save Plyr Coordinates on the Board

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

plyr = [[], [], [], []]

def spawn():
    for i in range(pc_cnt - 1):
        plyr[i] = spn_crd[i]
    
    plyr[pc_cnt - 1] = random.choice(x_pc)

    for i in range(pc_cnt):
        plyr[i][1] += int(board_y/2 - 1)

# Save plyr coordinates to the board
def pc_to_board():
    for i in range(pc_cnt):
        board[plyr[i][0]][plyr[i][1]] = 1

spawn()
pc_to_board()

for y in range(board_y):
    print(board[y])