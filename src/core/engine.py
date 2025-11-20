from textwrap import dedent
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.players import AbstractPlayer


class GameEngine:
    """Manages the state and rules of the game."""

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

    def __init__(self, player_x: "AbstractPlayer", player_o: "AbstractPlayer"):
        self.board = self._new_board()
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = player_x

    # --- Helpers ---

    def get_board_state(self) -> List[List[Optional[str]]]:
        """Provides the current, read-only board state.
        Used by the AI player to request the board when calculating a move."""
        return self.board

    def switch_player(self) -> None:
        """Switches the current player to the other player"""
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def get_current_player(self) -> "AbstractPlayer":
        """Getter method to return self.current_player"""
        return self.current_player

    # --- Core Game Logic ---

    def _new_board(self) -> List[List[Optional[str]]]:
        """Creates a new, empty 3x3 Tic-Tac-Tow board.

        Returns:
            List[List[Optional[str]]]: A 3x3 list of lists where all cells are initialized to
            None."""
        return [[None, None, None], [None, None, None], [None, None, None]]

    def show_board_positions(self) -> None:
        """Displays a numerical guide for the Tic-Tac-Toe board positions(1-9).

        This static guide helps the user understand how their number input maps to the game
        board."""
        board_positions = dedent(
            """\
        -------------
        | 1 | 2 | 3 |
        -------------
        | 4 | 5 | 6 |
        -------------
        | 7 | 8 | 9 |
        -------------
        """
        )
        print(board_positions)

    def make_move(self, move: Tuple[int, int]) -> None:
        """Places the current player's symbol in the given position on the internal board.

        This method mutates the game's internal board state directly.

        Args:
            move (Tuple[int, int]): The 0-indexed (row, col) coordinates for the
            move."""
        symbol = self.current_player.marker
        row, col = move
        self.board[row][col] = symbol

    def get_winner(
        self, board_state: Optional[List[List[Optional[str]]]] = None
    ) -> Optional[str]:
        """Determines if the current or provided board state contains a winning line.

        This method checks all predefined winning line combinations (rows, columns, diagonals)
        to see if any contain three identical, non-None symbols. If a winning line is found,
        the corresponding player's symbol is returned.

        Args:
            board_state (Optional[List[List[Optional[str]]]]): A 2D list representing the game board.
                If None, the method uses the internal board state (`self.board`).

        Returns:
            Optional[str]: The symbol of the winning player ('X' or 'O') if a winning line is found;
                otherwise, returns None."""
        if board_state is None:
            board_state = self.board

        for line in GameEngine.WINNING_LINE_POSITIONS:
            line_values = [board_state[row][col] for row, col in line]

            val1, val2, val3 = line_values

            if val1 == val2 == val3 and val1 is not None:
                return val1
        return None

    def is_board_full(
        self, board_state: Optional[List[List[Optional[str]]]] = None
    ) -> bool:
        """Checks the game board to see if all positions are occupied.

        It efficiently returns False as soon as it finds an empty space (None).

        Returns:
            bool: True if the board is full,
                False if at least one empty spot remains."""
        if board_state is None:
            board_state = self.board

        for row in board_state:
            if None in row:
                return False
        return True

    def is_valid_move(self, move: Tuple[int, int]) -> bool:
        """Checks if a requested move position is currently empty (valid).

        This function assumes the 'move' coordinate (row, col) are already within the legal
        board range(0-2), as validate by the Player Object.

        A move is valid if the cell at the given coordinates holds the value 'None'.

        Args:
            move (Tuple[int, int]): The 0-indexed (row, col) coordinates for the move.

        Returns:
            bool: True if the cell is empty (valid to place a symbol),
                False otherwise."""
        row, col = move
        return self.board[row][col] is None

    def check_game_status(self) -> Tuple[bool, Optional[str]]:
        """Evaluates the current game state and determines if the game is over.

        This method checks for a winning condition or a full board to determine
        whether the game has concluded. It returns a tuple indicating the game-over
        status and the winning marker, if any.

        Returns:
            Tuple[bool, Optional[str]]:
                - bool: True if the game is over (win or draw), False otherwise.
                - Optional[str]: The winning marker ("X" or "O") if there is a winner,
                  else None."""
        winner_marker = self.get_winner()
        is_full = self.is_board_full()
        is_over = (winner_marker is not None) or is_full
        return is_over, winner_marker

    def get_winner_name(self, winner_marker: str) -> Optional[str]:
        """Resolves the name of the winning player based on their marker.

        Given a marker ("X" or "O"), this method returns the corresponding player's name.
        If no winner exists (i.e., marker is None), it returns None.

        Args:
            winner_marker (str): The marker of the winning player ("X" or "O").

        Returns:
            Optional[str]: The name of the winning player, or None if no winner."""
        if winner_marker is None:
            return None
        elif winner_marker == self.player_x.marker:
            return self.player_x.name
        elif winner_marker == self.player_o.marker:
            return self.player_o.name
