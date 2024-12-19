import numpy as np
import pygame
from constants import *

class Board:
    def __init__(self, size, square_size):
        """
        Initialize the board with a given size and square size.
        """
        self.size = size
        self.SQUARE_SIZE = square_size
        self.squares = np.zeros((size, size))
        self.marked_sqrs = 0

    def final_state(self, screen, show=False):
        """
        Check the final state of the board.
        """
        for col in range(self.size):
            if all(self.squares[row][col] == self.squares[0][col] != 0 for row in range(self.size)):
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, 20)
                    fPos = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        for row in range(self.size):
            if all(self.squares[row][col] == self.squares[row][0] != 0 for col in range(self.size)):
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        if all(self.squares[i][i] == self.squares[0][0] != 0 for i in range(self.size)):
            if show:
                color = CIRC_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][0]

        if all(self.squares[i][self.size - 1 - i] == self.squares[0][self.size - 1] != 0 for i in range(self.size)):
            if show:
                color = CIRC_COLOR if self.squares[0][self.size - 1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][self.size - 1]

        return 0

    def mark_sqr(self, row, col, player):
        """
        Mark a square with the player's move.
        """
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        """
        Check if a square is empty.
        """
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        """
        Get a list of empty squares.
        """
        empty_sqrs = []
        for row in range(self.size):
            for col in range(self.size):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        """
        Check if the board is full.
        """
        return self.marked_sqrs == self.size * self.size

    def isempty(self):
        """
        Check if the board is empty.
        """
        return self.marked_sqrs == 0