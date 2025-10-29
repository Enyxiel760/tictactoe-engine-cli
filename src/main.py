from textwrap import dedent
from typing import List, Optional, Tuple

WINNING_LINE_POSITIONS = [
    [(0, 0), (0, 1), (0, 2)],  # row 1
    [(1, 0), (1, 1), (1, 2)],  # row 2
    [(2, 0), (2, 1), (2, 2)],  # row 3
    [(0, 0), (1, 0), (2, 0)],  # col 1
    [(0, 1), (1, 1), (2, 1)],  # col 2
    [(0, 2), (1, 2), (2, 2)],  # col 3
    [(0, 0), (1, 1), (2, 2)],  # diag 1
    [(0, 2), (1, 1), (2, 0)],  # diag 2
] 

def new_board() -> List[List[Optional[str]]]:
    """Creates a new, empty 3x3 Tic-Tac-Tow board.
    
    Returns:
        List[List[Optional[str]]]: A 3x3 list of lists where all cells are initialized to None."""
    
    board = [
             [None, None, None],
             [None, None, None],
             [None, None, None]
            ]
    return board

def prettify_board(board: List[List[Optional[str]]]) -> str:
    """Converts the 2D board structure into a formatted string for display.
    
    Cells containing None are visdually rendered as an empty space (" ").
    
    Args:
        board (List[List[Optional[str]]]): The current state of the game board.
    
    Returns:
        str: The multi-line string representation of the board grid"""

    p1, p2, p3, p4, p5, p6, p7, p8, p9 = [cell for row in board for cell in row]
    pretty_board = dedent(f"""\
    -------------
    | {p1 if p1 else " "} | {p2 if p2 else " "} | {p3 if p3 else " "} |
    -------------
    | {p4 if p4 else " "} | {p5 if p5 else " "} | {p6 if p6 else " "} |
    -------------
    | {p7 if p7 else " "} | {p8 if p8 else " "} | {p9 if p9 else " "} |
    -------------
    """)
    return pretty_board

def render(board: List[List[Optional[str]]]) -> None:
    """Prints the current state fo the game board to the console.
    
    It calls prettify_board() to get the formatted string before printing.
    
    Args:
        board (List[List[Optional[str]]]): The current state of the game board."""
    
    print(prettify_board(board))

def show_board_positions():
    """Displays a numerical guide for the Tic-Tac-Toe board positions(1-9).
    
    This static guide helps the user understand how their number input maps to the game board."""
    
    board_positions = dedent(f"""\
    -------------
    | 1 | 2 | 3 |
    -------------
    | 4 | 5 | 6 |
    -------------
    | 7 | 8 | 9 |
    -------------
    """)
    print(board_positions)

def get_move() -> Tuple[int, int]:
    """Prompts the current player for their move (1-9) and validates the input.
    
    This function loops indefinitely, handling non-numeric input and out-of-range
    numbers until a valid move number (1 through 9) is entered. It then converts
    the 1-indexed input into  0-indexed (row, column) coordinates.
    
    Returns:
        Tuple[int, int]: The 0-indexed (row, column) coordinates for the move."""
    
    move = None
    while True:
        try:
            move = input("Choose where to place next (1-9): ")
            move = int(move)

            if move in range (1, 10):
                move -= 1 # account for zero-indexing
                row = move // 3
                col = move % 3
                return (row , col)
            else:
                print("Invalid move. Please enter a number between 1 and 9.")
        
        except ValueError:
            # The int() function failed (e.g. a non-numerical value was entered)
            print("Invalid input. Please enter a number between 1 and 9")

def make_move(symbol: str, move: Tuple[int, int], board: List[List[Optional[str]]]) ->  List[List[Optional[str]]]:
    """Create a deep copy of the board and palces the player's symbol in the given position.
    
    The original board state is preserved. This function assumes the move is valid and the position is empty.
    
    Args:
        symbol (str): The player's marker ('X' or 'O').
        move (Tuple[int, int]): The 0-indexed (row, col) coordinates for the move.
        board (List[List[Optional[str]]]): The current state of the game board.
    
    Returns:
        List[List[Optional[str]]]: A new board instance with the move placed."""
    
    row, col = move
    new_board = []

    # Create a copy of the board to avoid mutation
    for line in board:
        new_board.append(line.copy())

    new_board[row][col] = symbol

    return new_board

def get_winner(board: List[List[Optional[str]]]) -> Optional[str]:
    """Checks the board for a winning condition.
    
    It iterates through all 8 possible winning lines to determine if one player has
    three identical, non-None symbols in a row.
    
    Args:
        board (List[List[Optional[str]]]): The current state of the game board.
        
    Returns:
        Optional[str]: The winning player's symbol ('X' or 'O') if a winner is found,
                       otherwise returns None"""
    
    for line in WINNING_LINE_POSITIONS:
        line_values = [board[row][col] for row, col in line]

        val1, val2, val3 = line_values

        if val1 == val2 == val3 and val1 is not None:
            return val1
    return None

def is_board_full(board: List[List[Optional[str]]]) -> bool:
    """Checks the game board to see iof all positions are occupied.
    
    It efficiently returns False as soon as it finds an empty space (None).
    
    Args:
        board (List[List[Optional[str]]]): The current state of the game board.

    Returns:
        bool: True if the board is full,
              False if at least one empty spot remains."""
    
    for row in board:
        if None in row:
            return False
    return True
    
def is_valid_move(move: Tuple[int, int], board: List[List[Optional[str]]]) -> bool:
    """Checks if a requested move position is currently empty (valid).
    
    A move is valid if the cell at the given coordinatres holds the value 'None'.
    
    Args:
        move (Tuple[int, int]): The 0-indexed (row, col) coordinates for the move.
        board (List[List[Optional[str]]]): The current state of the game board.
    
    Returns:
        bool: True if the cell is empty (valid to place a symbol),
              False otherwise."""
    
    row, col = move
    return board[row][col] is None

if __name__ == '__main__':
    board = new_board()
    print("Board positions are numbered 1-9 like so:")
    show_board_positions()
    current_player = "X"
    other_player = "O"

    while True:
        while True:
            move = get_move()
            if is_valid_move(move, board):
                break
            else:
                print("\nPlease select a valid position:")
                render(board)

        board = make_move(current_player , move, board)
        render(board)

        winner = get_winner(board)
        if winner is not None:
            print(f"{winner} won the round, congratulations!")
            break
        elif is_board_full(board):
            print("No winners this time, better luck next time!")
            break
        
        current_player, other_player = other_player, current_player