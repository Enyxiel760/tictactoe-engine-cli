from typing import List, Optional, Tuple
from .abstract_ai_player import AbstractAIPlayer
from random import choice


class RandomAIPlayer(AbstractAIPlayer):
    """Represents a simple AI player that selects moves at random.

    This class implements the abstract interface defined in `AbstractAIPlayer` and fulfills the
    contract by providing a concrete `get_move` method. The GameEngine instance is injected via
    a setter after initialization, allowing the AI to interact with the game state."""

    def _calculate_move(
        self, board_state: List[List[Optional[str]]]
    ) -> Tuple[int, int]:
        """Determines the AI's next move based on the current board state.

        This method scans the board for all available (empty) positions and randomly selects one.
        It returns the chosen move as a tuple of zero-based (row, column) coordinates.

        Args:
            board_state (List[List[Optional[str]]]): A 2D list representing the game board,
                where each cell contains a player symbol or None if unoccupied.

        Returns:
            Tuple[int, int]: The (row, column) coordinates of the selected move."""
        moves = []
        for i in range(len(board_state)):
            for j in range(len(board_state[i])):
                if board_state[i][j] is None:
                    moves.append((i, j))
        return choice(moves)
