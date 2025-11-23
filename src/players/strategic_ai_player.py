"""Strategic AI player for Tic Tac Toe.

Defines the StrategicAIPlayer class, which implements a medium-difficulty strategy that prioritizes
winning immediately or blocking the opponent before making random moves.
"""

from random import choice

from .abstract_ai_player import AbstractAIPlayer


class StrategicAIPlayer(AbstractAIPlayer):
    """Represents an AI player that prioritizes winning or blocking moves before selecting randomly.

    This class extends `AbstractAIPlayer` with a strategy that:
    1. Checks for any move that would result in an immediate win.
    2. Checks for any move that would block the opponent from winning on their next turn.
    3. If neither is found, selects randomly from the remaining valid positions.
    """

    def _find_critical_move(
        self,
        moves: list[tuple[int, int]] | None,
        board_state: list[list[str | None]],
    ) -> tuple[int, int] | None:
        """Identifies a move that either wins the game immediately or blocks the opponent.

        This method prioritizes winning moves: it simulates placing the AI's marker on each
        candidate position and returns the first move that results in a win. If no winning move is
        found, it checks whether placing the opponent's marker would result in their win — and
        stores the first such blocking move as a fallback.

        Args:
            moves: List of available (row, column) positions.
            board_state: Current board state as a 2D list.

        Returns:
            tuple[int, int] | None: A winning move if available; otherwise, the first blocking move;
            returns None if neither is found.
        """
        opponent_marker = "X" if self.marker == "O" else "O"
        blocking_move = None

        for move in moves:
            row, col = move
            # 1. Check for immediate win
            temp_state = self._game.get_board_copy(board_state)
            temp_state[row][col] = self.marker
            if self._game.get_winner(temp_state):
                return move

            # 2. Check for blocking move (only if we haven't found one yet)
            # We reuse the specific cell in temp_state to test the opponent's potential win
            if blocking_move is None:
                temp_state[row][col] = opponent_marker
                if self._game.get_winner(temp_state):
                    blocking_move = move

        return blocking_move

    def _calculate_move(self, board_state: list[list[str | None]]) -> tuple[int, int]:
        """Determines the AI's next move using a strategic priority order.

        This method:
        1. Collects all empty positions on the board.
        2. Uses `_find_critical_move` to check for a winning or blocking move.
        3. If none is found, selects randomly from the remaining valid options.

        Args:
            board_state: A 2D list representing the current game board.

        Returns:
            tuple[int, int]: The (row, column) coordinates of the selected move.
        """
        moves = []
        for i, row in enumerate(board_state):
            for j, cell in enumerate(row):
                if cell is None:
                    moves.append((i, j))

        winning_or_blocking_move = self._find_critical_move(moves, board_state)

        if winning_or_blocking_move:
            return winning_or_blocking_move
        else:
            return choice(moves)
