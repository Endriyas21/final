import copy

class MiniMax:
    def __init__(self, max_depth=4):
        """
        Initialize the MiniMax algorithm with a specified maximum depth.

        Args:
            max_depth (int): The maximum depth for the MiniMax algorithm.
        """
        self.max_depth = max_depth

    def alphabeta(self, board, screen, alpha, beta, depth, player):
        """
        Perform the Alpha-Beta pruning algorithm to find the best move.

        Args:
            board (Board): The current game board.
            screen (pygame.Surface): The screen to display the game.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.
            depth (int): The current depth of the search.
            player (str): The current player ('X' or 'O').

        Returns:
            list: The best move and its evaluation score.
        """
        best_move = self.initialize_best_move(player)
        available_cells = board.get_empty_sqrs()

        if self.is_terminal(board, screen):
            return self.terminal_score(board, screen)

        if depth == self.max_depth:
            return [-1, self.evaluate(board)]

        for (row, col) in available_cells:
            simulated_board = self.simulate(board, row, col, player)
            score = self.alphabeta(simulated_board, screen, alpha, beta, depth + 1, self.switch(player))
            score[0] = (row, col)

            print(f"Depth: {depth}, Player: {player}, Move: {(row, col)}, Score: {score[1]}")  # Debug

            best_move, alpha, beta = self.update_best_move(player, score, best_move, alpha, beta)
            if beta <= alpha:
                break

        return best_move

    def initialize_best_move(self, player):
        """
        Initialize the best move based on the player.

        Args:
            player (str): The current player ('X' or 'O').

        Returns:
            list: The initial best move and its evaluation score.
        """
        return [-1, float("-inf")] if player == 'X' else [-1, float("inf")]

    def is_terminal(self, board, screen):
        """
        Check if the current board state is terminal.

        Args:
            board (Board): The current game board.
            screen (pygame.Surface): The screen to display the game.

        Returns:
            bool: True if the board state is terminal, False otherwise.
        """
        return board.final_state(screen) in [1, 2] or board.isfull()

    def terminal_score(self, board, screen):
        """
        Get the terminal score for the current board state.

        Args:
            board (Board): The current game board.
            screen (pygame.Surface): The screen to display the game.

        Returns:
            list: The terminal score.
        """
        state = board.final_state(screen)
        return [-1, float('inf')] if state == 1 else [-1, float('-inf')] if state == 2 else [-1, 0]

    def simulate(self, board, row, col, player):
        """
        Simulate a move on the board.

        Args:
            board (Board): The current game board.
            row (int): The row of the move.
            col (int): The column of the move.
            player (str): The current player ('X' or 'O').

        Returns:
            Board: The simulated board after the move.
        """
        simulated_board = copy.deepcopy(board)
        simulated_board.mark_sqr(row, col, 1 if player == 'X' else 2)
        return simulated_board

    def switch(self, player):
        """
        Switch the player.

        Args:
            player (str): The current player ('X' or 'O').

        Returns:
            str: The switched player.
        """
        return 'O' if player == 'X' else 'X'

    def update_best_move(self, player, score, best_move, alpha, beta):
        """
        Update the best move based on the current score.

        Args:
            player (str): The current player ('X' or 'O').
            score (list): The current score.
            best_move (list): The current best move.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.

        Returns:
            tuple: The updated best move, alpha, and beta values.
        """
        if player == 'X':
            if score[1] > best_move[1]:
                best_move = score
            alpha = max(alpha, score[1])
        else:
            if score[1] < best_move[1]:
                best_move = score
            beta = min(beta, score[1])
        return best_move, alpha, beta

    def evaluate(self, board):
        """
        Evaluate the current board state.

        Args:
            board (Board): The current game board.

        Returns:
            int: The evaluation score of the board.
        """
        size = board.size
        x_counts, o_counts = self.initialize_counts(size)

        self.count_lines(board, size, x_counts, o_counts)
        self.count_diagonals(board, size, x_counts, o_counts)

        x_score = sum(4 * k * v for k, v in x_counts.items())
        o_score = sum(4 * k * v for k, v in o_counts.items())

        return x_score - o_score

    def initialize_counts(self, size):
        """
        Initialize the counts for X and O.

        Args:
            size (int): The size of the board.

        Returns:
            tuple: The initialized counts for X and O.
        """
        return dict.fromkeys(range(size + 1), 0), dict.fromkeys(range(size + 1), 0)

    def count_lines(self, board, size, x_counts, o_counts):
        """
        Count the lines for X and O.

        Args:
            board (Board): The current game board.
            size (int): The size of the board.
            x_counts (dict): The counts for X.
            o_counts (dict): The counts for O.
        """
        for row in range(size):
            row_values = board.squares[row]
            if 2 not in row_values:
                x_counts[row_values.tolist().count(1)] += 1
            if 1 not in row_values:
                o_counts[row_values.tolist().count(2)] += 1

        for col in range(size):
            col_values = board.squares[:, col]
            if 2 not in col_values:
                x_counts[col_values.tolist().count(1)] += 1
            if 1 not in col_values:
                o_counts[col_values.tolist().count(2)] += 1

    def count_diagonals(self, board, size, x_counts, o_counts):
        """
        Count the diagonals for X and O.

        Args:
            board (Board): The current game board.
            size (int): The size of the board.
            x_counts (dict): The counts for X.
            o_counts (dict): The counts for O.
        """
        main_diag = [board.squares[i][i] for i in range(size)]
        anti_diag = [board.squares[i][size - 1 - i] for i in range(size)]

        if 2 not in main_diag:
            x_counts[main_diag.count(1)] += 1
        if 1 not in main_diag:
            o_counts[main_diag.count(2)] += 1

        if 2 not in anti_diag:
            x_counts[anti_diag.count(1)] += 1
        if 1 not in anti_diag:
            o_counts[anti_diag.count(2)] += 1

class AI:
    def __init__(self, level=1, player=2, max_depth=4):
        """
        Initialize the AI with a specified level, player, and maximum depth.

        Args:
            level (int): The level of the AI.
            player (int): The player number (1 or 2).
            max_depth (int): The maximum depth for the MiniMax algorithm.
        """
        self.level = level
        self.player = player
        self.max_depth = max_depth
        self.minimax = MiniMax(max_depth)

    def eval(self, main_board, screen):
        """
        Evaluate the best move for the AI.

        Args:
            main_board (Board): The current game board.
            screen (pygame.Surface): The screen to display the game.

        Returns:
            tuple: The best move for the AI.
        """
        if main_board.size == 3:
            self.minimax.max_depth = 5

        move, evaluation = self.minimax.alphabeta(main_board, screen, -float('inf'), float('inf'), 0, 'X' if self.player == 1 else 'O')

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {evaluation}')
        return move