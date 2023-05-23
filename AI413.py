import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from functools import partial

# Function to print the Tic Tac Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Function to check for a winner
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

# Check if the board is full
def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Implement the Minimax algorithm
def minimax(board, depth, maximizing_player):
    winner = check_winner(board)
    if winner == 'X':
        return -1 * depth
    elif winner == 'O':
        return 1 * depth
    elif winner is None and is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    eval = minimax(board, depth - 1, False)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    eval = minimax(board, depth - 1, True)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to disable all buttons after game is over
def disable_buttons(buttons):
    for row in buttons:
        for button in row:
            button.config(state='disabled')

# Function to handle player move in GUI version
def player_move_gui(board, row, col, buttons, window):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state='disabled')
        winner = check_winner(board)
        if winner or is_board_full(board):
            window.title(f"{winner if winner else 'No one'} wins!")
            disable_buttons(buttons)
            return

        computer_move_gui(board, buttons, window)

# Function to handle computer move in GUI version
def computer_move_gui(board, buttons, window):
    best_move = None
    best_score = float('-inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 9, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    board[best_move[0]][best_move[1]] = 'O'
    buttons[best_move[0]][best_move[1]].config(text='O', state='disabled')
    winner = check_winner(board)
    if winner or is_board_full(board):
        window.title(f"{winner if winner else 'No one'} wins!")
        disable_buttons(buttons)
        return


# New function for button command
def button_command(board, row, col, buttons, window):
    player_move_gui(board, row, col, buttons, window)

def main_gui():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    buttons = [[None for _ in range(3)] for _ in range(3)]
    window = tk.Tk()
    window.title("Tic Tac Toe")

    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(window, text=' ', width=7, height=3, command=partial(button_command, board, row, col, buttons, window))
            buttons[row][col].grid(row=row, column=col, padx=2, pady=2, ipadx=10, ipady=10)

    window.mainloop()

if __name__ == "_main_":
    main_gui()