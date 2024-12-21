import unittest
from ai import AI, MiniMax
import numpy as np

class MockBoard:
    def __init__(self, size):
        self.size = size
        self.squares = np.zeros((size, size))
        self.marked_sqrs = 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.empty_sqr(row, col)]

    def isfull(self):
        return self.marked_sqrs == self.size * self.size

    def final_state(self, screen=None, show=False):
        for col in range(self.size):
            if all(self.squares[row][col] == self.squares[0][col] != 0 for row in range(self.size)):
                return self.squares[0][col]
        for row in range(self.size):
            if all(self.squares[row][col] == self.squares[row][0] != 0 for col in range(self.size)):
                return self.squares[row][0]
        if all(self.squares[i][i] == self.squares[0][0] != 0 for i in range(self.size)):
            return self.squares[0][0]
        if all(self.squares[i][self.size - 1 - i] == self.squares[0][self.size - 1] != 0 for i in range(self.size)):
            return self.squares[0][self.size - 1]
        return 0

class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = MockBoard(3)
        self.ai = AI(level=1, player=2, max_depth=4)

    def test_ai_initial_move(self):
        """Test if the AI makes a valid initial move."""
        move = self.ai.eval(self.board, None)
        self.assertIn(move, self.board.get_empty_sqrs())

    def test_ai_winning_move(self):
        """Test if the AI makes a winning move when it has the opportunity."""
        self.board.mark_sqr(0, 0, 2)
        self.board.mark_sqr(0, 1, 2)
        move = self.ai.eval(self.board, None)
        self.assertEqual(move, (0, 2))

    def test_ai_draw_move(self):
        """Test if the AI makes a move that results in a draw."""
        self.board.mark_sqr(0, 0, 1)
        self.board.mark_sqr(0, 1, 2)
        self.board.mark_sqr(0, 2, 1)
        self.board.mark_sqr(1, 0, 2)
        self.board.mark_sqr(1, 1, 1)
        self.board.mark_sqr(1, 2, 2)
        self.board.mark_sqr(2, 0, 2)
        self.board.mark_sqr(2, 1, 1)
        move = self.ai.eval(self.board, None)
        self.assertEqual(move, (2, 2))

if __name__ == '__main__':
    unittest.main()