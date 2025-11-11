from typing import List, Optional, Tuple
from .abstract_ai_player import AbstractAIPlayer
from random import choice


class StrategicAIPlayer(AbstractAIPlayer):
    """Represents an AI player that prioritizes winning or blocking moves before selecting randomly.

    This class extends `AbstractAIPlayer` with a strategy that:
    - First checks for any move that would result in an immediate win.
    - Then checks for any move that would block the opponent from winning on their next turn.
    - If neither is found, it selects randomly from the remaining valid positions.

    The GameEngine instance is injected via a setter after initialization, enabling access to
    game state and win detection logic."""

    def _find_critical_move(
        self,
        moves: Optional[List[Tuple[int, int]]],
        board_state: List[List[Optional[str]]],
    ) -> Optional[Tuple[int, int]]:
        """Identifies a move that either wins the game immediately or blocks the opponent from winning.

        This method prioritizes winning moves: it simulates placing the AI's marker on each candidate
        position and returns the first move that results in a win. If no winning move is found, it
        checks whether placing the opponent's marker would result in their win — and stores the first
        such blocking move as a fallback. Only one blocking move is retained, and only returned if no
        winning move is available.

        Args:
            moves (Optional[List[Tuple[int, int]]]): List of available (row, column) positions.
            board_state (List[List[Optional[str]]]): Current board state as a 2D list.

        Returns:
            Optional[Tuple[int, int]]: A winning move if available; otherwise, the first blocking move;
            returns None if neither is found."""
        opponent_marker = "X" if self.marker == "O" else "O"
        blocking_move = None
        # Check for a win
        for move in moves:
            temp_state = [row.copy() for row in board_state]
            temp_state[move[0]][move[1]] = self.marker
            if self._game.get_winner(temp_state):
                return move
            # Check for a block
            if blocking_move is None:
                temp_state[move[0]][move[1]] = opponent_marker
                if self._game.get_winner(temp_state):
                    blocking_move = move  # Lower priority, just stores it.

        return blocking_move if blocking_move else None

    def _calculate_move(
        self, board_state: List[List[Optional[str]]]
    ) -> Tuple[int, int]:
        """Determines the AI's next move using a strategic priority order.

        This method:
        - Collects all empty positions on the board.
        - Uses `_find_critical_move` to check for a winning or blocking move.
        - If none is found, selects randomly from the remaining valid options.

        Args:
            board_state (List[List[Optional[str]]]): A 2D list representing the current game board,
                where each cell contains a player symbol or None if unoccupied.

        Returns:
            Tuple[int, int]: The (row, column) coordinates of the selected move."""
        moves = []

        for i in range(len(board_state)):
            for j in range(len(board_state[i])):
                if board_state[i][j] is None:
                    moves.append((i, j))
        winning_move = self._find_critical_move(moves, board_state)

        if winning_move:
            return winning_move
        else:
            return choice(moves)
