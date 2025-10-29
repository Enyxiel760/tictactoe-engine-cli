from textwrap import dedent

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

def new_board():
    board = [
             [None, None, None],
             [None, None, None],
             [None, None, None]
            ]
    return board

def prettify_board(board):
    """Builds and returns a prettier string representation of the board."""
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

def render(board):
    print(prettify_board(board))

def show_board_positions():
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

def get_move():
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

def make_move(symbol, move, board):
    row, col = move
    new_board = []

    # Create a copy of the board to avoid mutation
    for line in board:
        new_board.append(line.copy())

    new_board[row][col] = symbol

    return new_board

def get_winner(board):
    for line in WINNING_LINE_POSITIONS:
        line_values = [board[row][col] for row, col in line]

        val1, val2, val3 = line_values

        if val1 == val2 == val3 and val1 is not None:
            return val1
    return None

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True
    
def is_valid_move(move, board):
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