#!/usr/bin/env python
import pygame
import math
import random
import pickle

# define some colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)
selected = pygame.Color(139, 105, 20)

colors = [white, green, blue,
          pygame.Color(160, 32, 240),
          pygame.Color(30, 144, 255),
          pygame.Color(165, 42, 42),
          pygame.Color(255, 165, 0)]

board_width = 8
board_height = 20
board_row = board_height - 1
board = []
history = []

pygame.init()

size = [350, 600]
radius = 25
xoffset = 40
yoffset = 40
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Editor")

done = False
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()

# board routines
def getBoardPos(pos):
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column] != -1:
                px = board[row][column][1]
                py = board[row][column][2]
                if math.pow(px - pos[0], 2) + math.pow(py - pos[1], 2) < radius * radius:
                    return [row, column]
    return [-1, -1]


def getBoardValue(row, column):
    if row >= 0 and row < board_height:
        if column >= 0 and column < board_width:
            return board[row][column][0]
    return -1


def initBoard():
    global board
    board = []
    for row in range(board_height):
        board.append([])
        idx = 0
        for column in range(board_width):
            if row % 2 == 0 and column % 2 != 0:
                board[row].append([-1, 0, 0])
            elif row % 2 != 0 and column % 2 == 0:
                board[row].append([-1, 0, 0])
            else:
                px = idx * radius * 3 + row % 2 * (radius * 3 / 2)
                py = row * radius * math.sqrt(3) / 2
                idx = idx + 1
                board[row].append([0, px + xoffset, py + yoffset])


def fillBoardNow():
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column][0] == -1:
                continue
            board[row][column][0] = random.randint(1, len(colors))


def saveBoard():
    fout = open("level.dat", "w")
    pickle.dump(board, fout)
    fout.close()
    print "Level saved"


def drawHex(px, py, r, bc, w, value):
    points = []
    for ang in range(6):
        x = px + r * math.cos(math.radians((ang + 1) * 60))
        y = py + r * math.sin(math.radians((ang + 1) * 60))
        points.append([x, y])
    cid = value & ((1 << 5) - 1)
    color = colors[cid - 1]
    pygame.draw.polygon(background, color, points)
    pygame.draw.polygon(background, bc, points, w)


def handleMouseDown(row, column):
    val = getBoardValue(row, column)
    if val == -1:
        return

    history.append([row, column, val])
    board[row][column][0] = -1


def historyBack():
    if len(history) > 0:
        val = history.pop()
        board[val[0]][val[1]][0] = val[2]

# init empty board
initBoard()
fillBoardNow()
background.fill(black)

# main loop 
while done == False:

    # limit to 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                history = []
                fillBoardNow()
                background.fill(black)
            if event.key == pygame.K_RETURN:
                saveBoard()
            if event.key == pygame.K_BACKSPACE:
                historyBack()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            bp = getBoardPos(pos)
            handleMouseDown(bp[0], bp[1])

    # fill empty cells
    background.fill(black)

    # draw the grid
    for row in range(board_height):
        for column in range(board_width):
            val = board[row][column]
            if val[0] > 0:
                drawHex(val[1], val[2], radius, black, 2, val[0])

    screen.blit(background, (0, 0))
    pygame.display.flip()

pygame.quit()
