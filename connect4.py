"""
Connect Four Game
This code implements the game Connect Four using the Pygame library.
The game board is represented by a 6x7 grid, and players take turns dropping
their pieces (red or yellow) into the columns. The first player to connect
four of their pieces vertically, horizontally, or diagonally wins the game.
"""

import numpy as np
import pygame
import sys

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7

# Initialize pygame
pygame.init()

# Initialize font
myfont = pygame.font.SysFont("monospace", 75)

def create_board():
    """Create an empty game board."""
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    """Drop a game piece into the board."""
    board[row][col] = piece

def is_valid_location(board, col):
    """Check if a column is a valid location for a move."""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    """Find the next available row in a column."""
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    """Check if a player has won the game."""
    # Check horizontal, vertical, and diagonal locations for winning move
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if np.all(board[r, c:c + 4] == piece):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if np.all(board[r:r + 4, c] == piece):
                return True
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if np.all([board[r + i][c + i] == piece for i in range(4)]):
                return True
            if np.all([board[r + 3 - i][c + i] == piece for i in range(4)]):
                return True
    return False

def draw_board(screen, board):
    """Draw the game board."""
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Set up the game window
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)

# Draw initial game board
board = create_board()
draw_board(screen, board)

# Initialize game variables
game_over = False
turn = 0

while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn + 1)

                if winning_move(board, turn + 1):
                    label_color = RED if turn == 0 else YELLOW
                    label = myfont.render(f"Player {turn + 1} wins!!", 1, label_color)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(4000)
                    game_over = True

            draw_board(screen, board)

            turn += 1
            turn %= 2
