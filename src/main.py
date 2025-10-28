from textwrap import dedent

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

board = new_board()


"""
#loop through turns until game over
loop forever:
    #TODO
    current_player = ???

    #print trhe current borad state
    render(board)

    #get the move from current player
    move = get_move()

    #make the move on the board
    make_move(board, current_player, move)

    #work out if theirs a winner
    winner = get_winner(board)

    #if there is a winner, exit loop
    if winner is not none:
        print "winner is" winner
        break

    #if no winner and board full
    if is_board_full(board):
        print "draw"
        break

#repeat until game over
    """