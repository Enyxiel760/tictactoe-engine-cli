"""Game engine for Tic Tac Toe.

Defines the GameEngine class, which manages the board state, enforces rules, and coordinates player
turns and win conditions.
"""

from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.players import AbstractPlayer


class GameEngine:
    """Manages the state and rules of Tic Tac Toe.

    Provides methods to manipulate the board, validate moves, switch players, and determine game
    outcomes.
    """

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
        """Initialize the game engine with two players.

        Creates a new empty board, assigns Player X and Player O, and sets the current player to
        Player X.

        Args:
            player_x: The player assigned the "X" marker.
            player_o: The player assigned the "O" marker.
        """
        self.board = self._new_board()
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = player_x

    # --- Helpers ---

    def get_board_state(self) -> list[list[str | None]]:
        """Return the current board state.

        Used by AI players to request the board when calculating a move.

        Returns:
            list[list[str | None]]: A 3x3 list of lists representing the board.
        """
        return self.board

    def get_board_copy(self, board_state: list[list[str | None]] | None) -> list[list[str | None]]:
        """Return a copy of the given or current board state.

        Args:
            board_state: A board to copy. If None, the internal board is copied.

        Returns:
            list[list[str | None]]: A deep copy of the board.
        """
        target = board_state if board_state is not None else self.board
        return [row.copy() for row in target]

    def switch_player(self) -> None:
        """Switches the current player to the other player."""
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def get_current_player(self) -> "AbstractPlayer":
        """Return the current player.

        Returns:
            AbstractPlayer: The player instance whose turn it is.
        """
        return self.current_player

    # --- Core Game Logic ---

    def _new_board(self) -> list[list[str | None]]:
        """Create a new empty 3x3 Tic Tac Toe board.

        Returns:
            list[list[str | None]]: A 3x3 list of lists initialized with None.
        """
        return [[None, None, None], [None, None, None], [None, None, None]]

    def show_board_positions(self) -> None:
        """Display a numerical guide for board positions (1-9).

        Helps the user understand how numeric input maps to board coordinates.
        """
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

    def make_move(self, move: tuple[int, int]) -> None:
        """Place the current player's marker at the given position.

        Args:
            move: The 0-indexed (row, col) coordinates for the move.
        """
        symbol = self.current_player.marker
        row, col = move
        self.board[row][col] = symbol

    def get_winner(self, board_state: list[list[str | None]] | None = None) -> str | None:
        """Determine if the board contains a winning line.

        Checks all predefined winning line combinations (rows, columns, diagonals). If a winning
        line is found, returns the corresponding marker.

        Args:
            board_state: A board to evaluate. If None,the internal board is used.

        Returns:
            str | None: The winning marker ("X" or "O") if found, else None.
        """
        if board_state is None:
            board_state = self.board

        for line in GameEngine.WINNING_LINE_POSITIONS:
            line_values = [board_state[row][col] for row, col in line]

            val1, val2, val3 = line_values

            if val1 == val2 == val3 and val1 is not None:
                return val1
        return None

    def is_board_full(self, board_state: list[list[str | None]] | None = None) -> bool:
        """Check if the board is full.

        Args:
            board_state: A board to evaluate. If None, the internal board is used.

        Returns:
            bool: True if all cells are occupied, False otherwise.
        """
        if board_state is None:
            board_state = self.board

        for row in board_state:
            if None in row:
                return False
        return True

    def is_valid_move(self, move: tuple[int, int]) -> bool:
        """Check if a move is valid.

        A move is valid if the target cell is empty (None). Assumes the coordinates are within the
        legal range (0-2).

        Args:
            move: The 0-indexed (row, col) coordinates.

        Returns:
            bool: True if the cell is empty, False otherwise.
        """
        row, col = move
        return self.board[row][col] is None

    def check_game_status(self) -> tuple[bool, str | None]:
        """Evaluate the current game state.

        Determines if the game is over due to a win or a full board.

        Returns:
            tuple[bool, str | None]:
                - bool: True if the game is over, False otherwise.
                - str | None: The winning marker ("X" or "O") if there is a winner, else None.
        """
        winner_marker = self.get_winner()
        is_full = self.is_board_full()
        is_over = (winner_marker is not None) or is_full
        return is_over, winner_marker

    def get_winner_name(self, winner_marker: str | None) -> str | None:
        """Retrieve the name of the winning player based on the marker.

        Args:
            winner_marker: The marker of the winning player ("X" or "O").

        Returns:
            str | None: The name of the winning player, or None if no winner.
        """
        if winner_marker is None:
            return None
        elif winner_marker == self.player_x.marker:
            return self.player_x.name
        elif winner_marker == self.player_o.marker:
            return self.player_o.name
