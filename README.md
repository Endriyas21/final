

# Tic Tac Toe AI

This project is a Tic Tac Toe game with an AI opponent implemented using the Minimax algorithm with alpha-beta pruning. The game is built using Python and Pygame.

## Features

- Play Tic Tac Toe against an AI opponent.
- Adjustable board size.
- AI uses the Minimax algorithm with alpha-beta pruning for optimal moves.
- Simple and intuitive user interface.

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/tic-tac-toe-ai.git
   cd tic-tac-toe-ai
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the game:**

   ```sh
   python main.py
   ```

2. **Enter the board size** when prompted.

3. **Play the game** by clicking on the squares to make your move. The AI will respond with its move.

## Project Structure

- main.py: The main entry point for the game.
- game.py: Contains the Game class that manages the game logic.
- board.py: Contains the Board class that manages the board state.
- ai.py: Contains the AI and MiniMax classes that implement the AI logic.
- constants.py: Contains constants used throughout the project.
- test.py: Contains unit tests for the AI.
  
## How It Works

### Minimax Algorithm

The AI uses the Minimax algorithm with alpha-beta pruning to determine the best move. The algorithm evaluates all possible moves and selects the one that maximizes the AI's chances of winning while minimizing the player's chances.

### Board Representation

The board is represented as a 2D NumPy array. Each cell can be empty (0), occupied by player X (1), or occupied by player O (2).

### Game Flow

1. The player makes a move by clicking on a square.
2. The game updates the board and checks if the game is over.
3. If the game is not over, the AI makes its move.
4. The game repeats steps 2-3 until the game is over.




