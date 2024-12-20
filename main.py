import pygame
import sys
from game import Game
from constants import *

def render_text(screen, text, font_size, position, color=(255, 255, 255)):
    """
    Render text on the screen.
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_input_box(screen, input_text):
    """
    Draw the input box for board size.
    """
    screen.fill(BG_COLOR)
    render_text(screen, "Enter Board Size", 74, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
    input_box = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 40)
    pygame.draw.rect(screen, (255, 255, 255), input_box)  # White input box
    render_text(screen, input_text, 36, (input_box.x + 5, input_box.y + 5), color=(0, 0, 0))  # Black text
    pygame.display.flip()
    return input_box

def handle_input_events(input_text):
    """
    Handle input events for board size.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    size = int(input_text)
                    if size < 3:
                        raise ValueError("Size must be 3 or greater")
                    return size
                except ValueError:
                    return ''
            elif event.key == pygame.K_BACKSPACE:
                return input_text[:-1]
            else:
                return input_text + event.unicode
    return input_text

def get_board_size(screen):
    """
    Get the board size from user input.
    """
    input_text = ''
    while True:
        input_text = handle_input_events(input_text)
        if isinstance(input_text, int):
            return input_text
        draw_input_box(screen, input_text)

def handle_game_events(game, board, ai):
    """
    Handle game events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            handle_keydown_events(event, game, board, ai)
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_events(event, game, board, ai)

def handle_keydown_events(event, game, board, ai):
    """
    Handle keydown events.
    """
    key_actions = {
        pygame.K_g: game.change_gamemode,
        pygame.K_r: lambda: reset_game(game, board, ai),
        pygame.K_0: lambda: set_ai_level(ai, 0),
        pygame.K_1: lambda: set_ai_level(ai, 1)
    }
    action = key_actions.get(event.key)
    if action:
        action()

def handle_mouse_events(event, game, board, ai):
    """
    Handle mouse events.
    """
    pos = event.pos
    row = pos[1] // SQUARE_SIZE
    col = pos[0] // SQUARE_SIZE
    if board.empty_sqr(row, col) and game.running:
        game.make_move(row, col)
        if game.isover():
            game.running = False

def reset_game(game, board, ai):
    """
    Reset the game.
    """
    game.reset()
    board = game.board
    ai = game.ai
    game.running = True

def set_ai_level(ai, level):
    """
    Set the AI level.
    """
    ai.level = level

def main():
    """
    Main function to run the game.
    """
    global SQUARE_SIZE, CIRCLE_RADIUS, screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('TIC TAC TOE AI')

    size = get_board_size(screen)

    global BOARD_ROWS, BOARD_COLS
    BOARD_ROWS = size
    BOARD_COLS = size
    SQUARE_SIZE = WIDTH // BOARD_COLS
    CIRCLE_RADIUS = SQUARE_SIZE // 3

    game = Game(size, screen)
    board = game.board
    ai = game.ai

    while True:
        handle_game_events(game, board, ai)
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board, screen)
            game.make_move(row, col)
            if game.isover():
                game.running = False
        pygame.display.update()

if __name__ == "__main__":
    main()