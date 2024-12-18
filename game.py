import pygame
from board import Board
from ai import AI
from constants import *

class Game:
    def __init__(self, size, screen):
        """
        Initialize the game with board size and screen.
        """
        self.size = size
        self.screen = screen
        self.SQUARE_SIZE = WIDTH // size
        self.board = Board(size, self.SQUARE_SIZE)
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.CIRCLE_RADIUS = self.SQUARE_SIZE // 3
        self.show_lines()

    def show_lines(self):
        """
        Show the grid lines on the board.
        """
        self.screen.fill(BG_COLOR)
        self.draw_lines()

    def draw_lines(self):
        """
        Draw the grid lines.
        """
        [pygame.draw.line(self.screen, LINE_COLOR, (col * self.SQUARE_SIZE, 0), (col * self.SQUARE_SIZE, HEIGHT), LINE_WIDTH) for col in range(1, self.size)]
        [pygame.draw.line(self.screen, LINE_COLOR, (0, row * self.SQUARE_SIZE), (WIDTH, row * self.SQUARE_SIZE), LINE_WIDTH) for row in range(1, self.size)]

    def draw_cross(self, row, col):
        """
        Draw a cross (X) on the board.
        """
        positions = self.calculate_cross_positions(row, col)
        [pygame.draw.line(self.screen, CROSS_COLOR, start, end, CROSS_WIDTH) for start, end in positions]

    def calculate_cross_positions(self, row, col):
        """
        Calculate positions for drawing a cross.
        """
        start_desc = (col * self.SQUARE_SIZE + OFFSET, row * self.SQUARE_SIZE + OFFSET)
        end_desc = (col * self.SQUARE_SIZE + self.SQUARE_SIZE - OFFSET, row * self.SQUARE_SIZE + self.SQUARE_SIZE - OFFSET)
        start_asc = (col * self.SQUARE_SIZE + OFFSET, row * self.SQUARE_SIZE + self.SQUARE_SIZE - OFFSET)
        end_asc = (col * self.SQUARE_SIZE + self.SQUARE_SIZE - OFFSET, row * self.SQUARE_SIZE + OFFSET)
        return [(start_desc, end_desc), (start_asc, end_asc)]

    def draw_circle(self, row, col):
        """
        Draw a circle (O) on the board.
        """
        center = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
        pygame.draw.circle(self.screen, CIRC_COLOR, center, self.CIRCLE_RADIUS, CIRC_WIDTH)

    def draw_fig(self, row, col):
        """
        Draw the current player's figure (X or O).
        """
        draw_methods = {1: self.draw_cross, 2: self.draw_circle}
        draw_methods[self.player](row, col)

    def display_message(self, message):
        """
        Display a message on the screen.
        """
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def make_move(self, row, col):
        """
        Make a move on the board.
        """
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        """
        Switch to the next player.
        """
        self.player = 1 if self.player == 2 else 2

    def change_gamemode(self):
        """
        Change the game mode.
        """
        self.gamemode = 'ai' if self.gamemode == 'ai' else 'ai'

    def isover(self):
        """
        Check if the game is over.
        """
        result = self.board.final_state(self.screen, show=True)
        return self.check_game_over(result)

    def check_game_over(self, result):
        """
        Check the game over condition and display the result.
        """
        messages = {1: "Player X Wins!", 2: "Player O Wins!", 0: "Draw!"}
        if result != 0 or self.board.isfull():
            self.display_message(messages[result])
            return True
        return False

    def reset(self):
        """
        Reset the game.
        """
        self.__init__(self.size, self.screen)
# Some parts of the design were inspired by https://www.youtube.com/watch?v=LbTu0rwikwg&t=90s