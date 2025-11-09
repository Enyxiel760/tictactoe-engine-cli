from textwrap import dedent
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.players import AbstractPlayer

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


class GameEngine:
    """Manages the state and rules of the game."""

    def __init__(self, player_x: "AbstractPlayer", player_o: "AbstractPlayer"):
        self.board = self._new_board()
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = player_x

    # --- Helpers ---

    def get_board_state(self) -> List[List[Optional[str]]]:
        """Provides the current, read-only board state.
        Used by the AI player to request the board when calculating a move."""
        # Return a copy to prevent external modification
        return [row[:] for row in self.board]

    def switch_player(self) -> None:
        """Switches the current player to the other player"""
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    # --- Core Game Logic ---

    def _new_board(self) -> List[List[Optional[str]]]:
        """Creates a new, empty 3x3 Tic-Tac-Tow board.

        Returns:
            List[List[Optional[str]]]: A 3x3 list of lists where all cells are initialized to
            None."""
        return [[None, None, None], [None, None, None], [None, None, None]]

    def prettify_board(self) -> str:
        """Converts the 2D board structure into a formatted string for display.

        Cells containing None are visually rendered as an empty space (" ").

        Returns:
            str: The multi-line string representation of the board grid"""
        pos = [cell for row in self.board for cell in row]
        pretty_board = dedent(
            f"""\
        -------------
        | {pos[0] if pos[0] else " "} | {pos[1] if pos[1] else " "} | {pos[2] if pos[2] else " "} |
        -------------
        | {pos[3] if pos[3] else " "} | {pos[4] if pos[4] else " "} | {pos[5] if pos[5] else " "} |
        -------------
        | {pos[6] if pos[6] else " "} | {pos[7] if pos[7] else " "} | {pos[8] if pos[8] else " "} |
        -------------
        """
        )
        return pretty_board

    def render(self) -> None:
        """Prints the current state fo the game board to the console.

        It calls prettify_board() to get the formatted string before printing."""
        print(self.prettify_board())

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

    def get_winner(self, board_state=None) -> Optional[str]:
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

        for line in WINNING_LINE_POSITIONS:
            line_values = [board_state[row][col] for row, col in line]

            val1, val2, val3 = line_values

            if val1 == val2 == val3 and val1 is not None:
                return val1
        return None

    def is_board_full(self, board_state=None) -> bool:
        """Checks the game board to see iof all positions are occupied.

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
