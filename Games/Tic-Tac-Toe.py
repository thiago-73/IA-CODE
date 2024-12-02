import pygame
import sys
import random

# Introduction:
# This is a simple Tic-Tac-Toe game where the player competes against an AI.
# The game uses the Minimax algorithm for the AI to make optimal moves.
# The player plays as 'X' and the AI plays as 'O'. The game runs on a 3x3 grid.
# The game ends when there is a winner or a draw, and it restarts automatically.

# Initialize Pygame
pygame.init()

# Set up the window dimensions and create the screen
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe with AI")

# Colors
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (242, 85, 96)
O_COLOR = (28, 170, 156)

# Grid setup
LINE_WIDTH = 15
GRID_SIZE = 3
cell_size = WIDTH // GRID_SIZE

# Font for displaying text
font = pygame.font.Font(None, 40)

# Function to draw the grid lines on the screen
def draw_grid():
    # Draw horizontal lines
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * cell_size), (WIDTH, row * cell_size), LINE_WIDTH)
    
    # Draw vertical lines
    for col in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (col * cell_size, 0), (col * cell_size, HEIGHT), LINE_WIDTH)

# Function to draw 'X' and 'O' in the cells
def draw_move(player, row, col):
    if player == 'X':
        color = X_COLOR
        # Draw X (cross lines)
        pygame.draw.line(screen, color, (col * cell_size + 20, row * cell_size + 20), 
                         (col * cell_size + cell_size - 20, row * cell_size + cell_size - 20), LINE_WIDTH)
        pygame.draw.line(screen, color, (col * cell_size + 20, row * cell_size + cell_size - 20), 
                         (col * cell_size + cell_size - 20, row * cell_size + 20), LINE_WIDTH)
    elif player == 'O':
        color = O_COLOR
        # Draw O (circle)
        pygame.draw.circle(screen, color, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), 
                           cell_size // 2 - 20, LINE_WIDTH)

# Minimax algorithm for AI's decision-making
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return -1  # Player wins
    elif winner == 'O':
        return 1   # AI wins
    elif winner == 'Draw':
        return 0   # Draw

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
        return min_eval

# Function to determine the best move for the AI
def best_move(board):
    best_val = float('-inf')
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_val = minimax(board, 0, False)
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

# Check for winner or draw
def check_winner(board):
    # Possible winning combinations
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    # Check for a winner (either 'X' or 'O')
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != ' ':
            return board[pos[0]]  # Return the winner ('X' or 'O')
    
    # Check if the board is full (draw)
    if ' ' not in board:
        return 'Draw'
    
    return None  # No winner yet

# Main game loop to manage the game flow
def play_game():
    board = [' ' for _ in range(9)]  # Empty board
    turn = 'X'  # Player starts first
    
    while True:
        screen.fill(WHITE)  # Fill the screen with white color
        draw_grid()  # Draw the grid

        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Close the game if the window is closed
            
            # Player's turn (click to place 'X')
            if turn == 'X' and event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = pos[1] // cell_size, pos[0] // cell_size
                index = row * GRID_SIZE + col
                if board[index] == ' ':
                    board[index] = 'X'
                    turn = 'O'  # Switch turn to AI

        # AI's turn (make a move using the best_move function)
        if turn == 'O':
            move = best_move(board)
            board[move] = 'O'
            turn = 'X'  # Switch turn to player

        # Draw all the moves on the board
        for i in range(3):
            for j in range(3):
                draw_move(board[i*3+j], i, j)

        # Check if there is a winner or a draw
        winner = check_winner(board)
        if winner:
            if winner == 'X':
                print("You win!")
            elif winner == 'O':
                print("AI wins!")
            else:
                print("It's a draw!")
            pygame.time.wait(2000)  # Wait for 2 seconds before restarting the game
            play_game()  # Restart the game

        pygame.display.update()  # Update the display

# Run the game
if __name__ == "__main__":
    play_game()  # Start the game
