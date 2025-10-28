def new_board():
    board = [
             [None, None, None],
             [None, None, None],
             [None, None, None]
            ]
    return board

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