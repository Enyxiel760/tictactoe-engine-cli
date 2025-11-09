from typing import List, Optional, Tuple
from .abstract_ai_player import AbstractAIPlayer


class MinimaxAIPlayer(AbstractAIPlayer):
    """Represents an AI player that uses the minimax algorithm to select optimal moves.

    This class extends `AbstractAIPlayer` by implementing a recursive minimax strategy
    to evaluate all possible future game states. It selects the move that maximizes its
    chances of winning while minimizing the opponent's opportunities. The GameEngine
    instance is injected via a setter after initialization to enable win and draw detection.
    """

    def _minimax_score(
        self, board_state: List[List[Optional[str]]], current_player_marker: str
    ) -> int:
        """Recursively evaluates the score of a board state using the minimax algorithm.

        This method simulates all possible future moves from the given board state,
        alternating turns between the AI and its opponent. It assigns scores to terminal
        states (+10 for AI win, -10 for opponent win, 0 for draw) and propagates those
        scores back up the recursive call stack to determine the optimal move.

        Args:
            board_state (List[List[Optional[str]]]): A 2D list representing the current game board.
            current_player_marker (str): The marker ('X' or 'O') of the player whose turn it is.

        Returns:
            int: The minimax score of the board state from the perspective of the AI."""
        # Base case: check for terminal state
        winner = self._game.get_winner(board_state)
        if winner == self.marker:  # Self won
            return 10
        elif winner:  # Opponent won
            return -10
        elif self._game.is_board_full(board_state):  # Draw
            return 0

        # Evaluate child states
        scores = []
        for i in range(len(board_state)):
            for j in range(len(board_state)):
                if board_state[i][j] is None:
                    temp_board = [row.copy() for row in board_state]
                    temp_board[i][j] = current_player_marker
                    opponent_marker = "X" if current_player_marker == "O" else "O"

                    # Recursively call for the next players turn
                    score = self._minimax_score(temp_board, opponent_marker)
                    scores.append(score)

        # Return max or min based on current player: Self = highest, opponent = lowest
        if current_player_marker == self.marker:
            return max(scores)
        else:
            return min(scores)

    def _calculate_move(
        self, board_state: List[List[Optional[str]]]
    ) -> Tuple[int, int]:
        """Determines the AI's next move using the minimax algorithm.

        This method evaluates all legal moves by simulating each one and scoring the
        resulting board state using `_minimax_score`. It selects the move with the
        highest score, representing the most favorable outcome for the AI.

        Args:
            board_state (List[List[Optional[str]]]): A 2D list representing the current game board,
                where each cell contains a player symbol or None if unoccupied.

        Returns:
            Tuple[int, int]: The (row, column) coordinates of the selected move."""
        moves = []
        scores = []
        opponent_marker = "X" if self.marker == "O" else "O"

        for i in range(len(board_state)):
            for j in range(len(board_state[i])):
                if board_state[i][j] is None:
                    move = (i, j)
                    temp_board = [row.copy() for row in board_state]
                    temp_board[i][j] = self.marker
                    score = self._minimax_score(temp_board, opponent_marker)
                    moves.append(move)
                    scores.append(score)
        return moves[scores.index(max(scores))]
