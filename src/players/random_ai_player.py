"""Random AI player for Tic Tac Toe.

Defines the RandomAIPlayer class, which implements a simple strategy of selecting random available
moves.
"""

from random import choice

from .abstract_ai_player import AbstractAIPlayer


class RandomAIPlayer(AbstractAIPlayer):
    """Represents a simple AI player that selects moves at random.

    This class implements the abstract interface defined in `AbstractAIPlayer` and fulfills the
    contract by providing a concrete `get_move` method.
    """

    def _calculate_move(self, board_state: list[list[str | None]]) -> tuple[int, int]:
        """Determines the AI's next move based on the current board state.

        This method scans the board for all available (empty) positions and randomly selects one.

        Args:
            board_state: A 2D list representing the game board, where each cell contains a player
                symbol or None if unoccupied.

        Returns:
            tuple[int, int]: The (row, column) coordinates of the selected move.
        """
        moves = []
        for i, row in enumerate(board_state):
            for j, cell in enumerate(row):
                if cell is None:
                    moves.append((i, j))

        return choice(moves)
