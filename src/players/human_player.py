from typing import Tuple
from .abstract_player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
    """Creates a human player object"""

    def get_move(self) -> Tuple[int, int]:
        """Prompts the current player for their move (1-9) and validates the input.

        This function loops indefinitely, handling non-numeric input and out-of-range
        numbers until a valid move number (1 through 9) is entered. It then converts
        the 1-indexed input into  0-indexed (row, column) coordinates.

        Returns:
            Tuple[int, int]: The 0-indexed (row, column) coordinates for the move."""

        while True:
            try:
                prompt = (
                    f"{self.name}, choose where to place your next {self.marker} (1-9)"
                )
                move_input = input(prompt)
                move = int(move_input)

                if move in range(1, 10):
                    move -= 1  # account for zero-indexing
                    row = move // 3
                    col = move % 3
                    return (row, col)
                else:
                    print("Invalid move. Please enter a number between 1 and 9.")

            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
