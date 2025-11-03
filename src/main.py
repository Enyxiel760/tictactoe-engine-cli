from engine import *

if __name__ == "__main__":
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

        board = make_move(current_player, move, board)
        render(board)

        winner = get_winner(board)
        if winner is not None:
            print(f"{winner} won the round, congratulations!")
            break
        elif is_board_full(board):
            print("No winners this time, better luck next time!")
            break

        current_player, other_player = other_player, current_player
