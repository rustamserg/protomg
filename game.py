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
score = 0
scoreStart = 4
scoreBonusStart = 5
scoreBonus = 0
scoreMult = 1
timeMult = 2
longestChain = 0

isMouseDown = False
isMouseMove = False
rowDown = 0
colDown = 0
rowMove = 0
colMove = 0

pygame.init()

size = [350, 600]
radius = 25
xoffset = 40
yoffset = 40
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game")

done = False
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()
hud_back = pygame.Surface((screen.get_width(), 50))
hud_back = hud_back.convert()
hud_font = pygame.font.Font(None, 36)

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
    fout = open("level.dat", "r")
    board = pickle.load(fout)


def fillBoardNow():
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column][0] == -1:
                continue
            board[row][column][0] = random.randint(1, len(colors))


def fillBoard():
    global board_row
    for row in range(2):
        for column in range(board_width):
            if board[row][column][0] == -1:
                continue
            if board[row][column][0] == 0:
                board[row][column][0] = random.randint(1, len(colors))

    for column in range(board_width):
        if board[board_row][column][0] == -1:
            continue

        if board[board_row][column][0] == 0:
            val = getBoardValue(board_row - 2, column)
            if val != -1:
                board[board_row - 2][column][0] = 0
                board[board_row][column][0] = val
                continue
            val = getBoardValue(board_row - 1, column - 1)
            if val != -1:
                board[board_row - 1][column - 1][0] = 0
                board[board_row][column][0] = val
                continue
            val = getBoardValue(board_row - 1, column + 1)
            if val != -1:
                board[board_row - 1][column + 1][0] = 0
                board[board_row][column][0] = val
                continue

    board_row = board_row - 1
    if board_row == 1:
        board_row = board_height - 1


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

# handle game logic code
match_counter = 0


def findMatchValues(value, row, column):
    global match_counter
    # upper-left
    col2 = column - 1
    row2 = row - 1
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)
    # up
    col2 = column
    row2 = row - 2
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)
    # up-right
    col2 = column + 1
    row2 = row - 1
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)
    # down-right
    col2 = column + 1
    row2 = row + 1
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)
    # down
    col2 = column
    row2 = row + 2
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)
    # down-left
    col2 = column - 1
    row2 = row + 1
    val2 = getBoardValue(row2, col2)
    if val2 == value:
        match_counter = match_counter + 1
        board[row2][col2][0] |= (1 << 5)
        findMatchValues(value, row2, col2)


def rotateUpRight():
    col = colMove
    row = rowMove
    newVal = getBoardValue(row, col)

    while True:
        col = col + 1
        row = row - 1
        oldVal = getBoardValue(row, col)
        if oldVal == -1:
            break
        board[row][col][0] = newVal | (1 << 6)
        newVal = oldVal

    col = colMove
    row = rowMove

    while True:
        newVal2 = getBoardValue(row + 1, col - 1)
        if newVal2 == -1:
            board[row][col][0] = newVal
            break
        board[row][col][0] = newVal2 | (1 << 6)
        row = row + 1
        col = col - 1


def rotateUpLeft():
    col = colMove
    row = rowMove
    newVal = getBoardValue(row, col)

    while True:
        col = col - 1
        row = row - 1
        oldVal = getBoardValue(row, col)
        if oldVal == -1:
            break
        board[row][col][0] = newVal | (1 << 6)
        newVal = oldVal

    col = colMove
    row = rowMove

    while True:
        newVal2 = getBoardValue(row + 1, col + 1)
        if newVal2 == -1:
            board[row][col][0] = newVal
            break
        board[row][col][0] = newVal2 | (1 << 6)
        row = row + 1
        col = col + 1


def rotateDownRight():
    col = colMove
    row = rowMove
    newVal = getBoardValue(row, col)

    while True:
        col = col + 1
        row = row + 1
        oldVal = getBoardValue(row, col)
        if oldVal == -1:
            break
        board[row][col][0] = newVal | (1 << 6)
        newVal = oldVal

    col = colMove
    row = rowMove

    while True:
        newVal2 = getBoardValue(row - 1, col - 1)
        if newVal2 == -1:
            board[row][col][0] = newVal
            break
        board[row][col][0] = newVal2 | (1 << 6)
        row = row - 1
        col = col - 1


def rotateDownLeft():
    col = colMove
    row = rowMove
    newVal = getBoardValue(row, col)

    while True:
        col = col - 1
        row = row + 1
        oldVal = getBoardValue(row, col)
        if oldVal == -1:
            break
        board[row][col][0] = newVal | (1 << 6)
        newVal = oldVal

    col = colMove
    row = rowMove

    while True:
        newVal2 = getBoardValue(row - 1, col + 1)
        if newVal2 == -1:
            board[row][col][0] = newVal
            break
        board[row][col][0] = newVal2 | (1 << 6)
        row = row - 1
        col = col + 1


def handleMouseMove(row, column):
    global rowMove
    global colMove
    global isMouseMove

    if not isMouseDown:
        return

    dx = rowMove - row
    dy = colMove - column

    if math.fabs(dx) == math.fabs(dy) and math.fabs(dx) > 0:
        if dx > 0 and dy < 0:
            rotateUpRight()
        if dx < 0 and dy < 0:
            rotateDownRight()
        if dx > 0 and dy > 0:
            rotateUpLeft()
        if dx < 0 and dy > 0:
            rotateDownLeft()
        rowMove = row
        colMove = column
        isMouseMove = True


def handleMouseDown(row, column):
    global rowDown
    global colDown
    global colMove
    global rowMove
    global isMouseDown
    global isMouseMove

    val = getBoardValue(row, column)
    if val == -1 or val == 0:
        return

    board[row][column][0] |= (1 << 6)

    isMouseDown = True
    isMouseMove = False
    rowDown = row
    colDown = column
    rowMove = row
    colMove = column


def handleMouseUp(row, column):
    global match_counter
    global score
    global scoreBonus
    global isMouseDown
    global longestChain

    if isMouseDown:
        for r in range(board_height):
            for c in range(board_width):
                if board[r][c][0] == -1:
                    continue
                board[r][c][0] &= ~(1 << 6)
        isMouseDown = False

    if isMouseMove:
        return

    val = getBoardValue(row, column)
    if val == -1 or val == 0:
        return

    match_counter = 1
    board[row][column][0] |= (1 << 5)
    findMatchValues(val, row, column)
    if match_counter >= scoreStart:
        scoreBonus = max(0, match_counter - scoreBonusStart)
        scoreBonus = scoreBonus * scoreBonus * scoreMult
        score = score + match_counter * scoreMult + scoreBonus
        if match_counter > longestChain:
            longestChain = match_counter

    for row in range(board_height):
        for column in range(board_width):
            if board[row][column][0] == -1:
                continue
            if match_counter < scoreStart:
                board[row][column][0] &= ~(1 << 5)
            else:
                if board[row][column][0] & (1 << 5):
                    board[row][column][0] = 0


# init empty board
initBoard()
fillBoardNow()
background.fill(black)
sessionTime = 0
maxSessionTime = 60 * 1000
isGameOver = False

# main loop 
while done == False:

    # limit to 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isGameOver = False
                sessionTime = 0
                score = 0
                isMouseDown = False
                isMouseMove = False
                rowDown = 0
                colDown = 0
                rowMove = 0
                colMove = 0
                fillBoardNow()
                background.fill(black)

        if not isGameOver:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bp = getBoardPos(pos)
                handleMouseUp(bp[0], bp[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bp = getBoardPos(pos)
                handleMouseDown(bp[0], bp[1])
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                bp = getBoardPos(pos)
                handleMouseMove(bp[0], bp[1])

    # fill empty cells
    background.fill(black)
    fillBoard()

    # draw the grid
    for row in range(board_height):
        for column in range(board_width):
            val = board[row][column]
            if val[0] > 0:
                drawHex(val[1], val[2], radius, black, 2, val[0])


    # draw the score
    hud_back.fill(pygame.Color(139, 105, 20))
    text = hud_font.render("Score: %i Longest chain: %i" % (score, longestChain), 1, white)
    hud_back.blit(text, (5, 5))

    # draw time
    sessionTime = max(0, sessionTime + clock.get_time() - timeMult * scoreBonus)
    passedTime = float(sessionTime) / max(maxSessionTime, sessionTime)
    pygame.draw.rect(hud_back, green, [0, hud_back.get_height() - 10, hud_back.get_width() * passedTime, 10])
    if passedTime == 1:
        isGameOver = True

    if isGameOver:
        text = hud_font.render("GAME OVER", 1, red)
        background.blit(text, (background.get_width() / 2 - 70, background.get_height() - 120))

        text = hud_font.render("ESC to start new...", 1, red)
        background.blit(text, (background.get_width() / 2 - 90, background.get_height() - 90))

    screen.blit(background, (0, 0))
    screen.blit(hud_back, (0, background.get_height() - 50))
    pygame.display.flip()

pygame.quit()
