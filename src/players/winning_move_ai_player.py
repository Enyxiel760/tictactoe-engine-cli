from typing import List, Optional, Tuple, TYPE_CHECKING
from .abstract_ai_player import AbstractAIPlayer
from random import choice


class WinningMoveAIPlayer(AbstractAIPlayer):
    """Represents an AI player that prioritizes immediate winning moves before selecting randomly.

    This class extends `AbstractAIPlayer` by implementing a strategy that checks for any move
    that would result in a win on the current turn. If no such move exists, it selects randomly
    from the remaining valid options. The GameEngine instance is injected via a setter after
    initialization, enabling access to game state and win detection."""

    def _find_winning_move(
        self,
        moves: Optional[List[Tuple[int, int]]],
        board_state: List[List[Optional[str]]],
    ) -> Optional[Tuple[int, int]]:
        """Scans a list of candidate moves to identify any that result in an immediate win.

        For each available move, this method simulates placing the AI's marker on a copy of the
        current board and checks if it results in a win using the game engine's win detection logic.

        Args:
            moves (Optional[List[Tuple[int, int]]]): A list of (row, column) tuples representing
                available positions on the board.
            board_state (List[List[Optional[str]]]): The current game board as a 2D list, where each
                cell contains a player symbol or None if unoccupied.

        Returns:
            Optional[Tuple[int, int]]: The first move found that results in a win, or None if no
            winning move is available."""

        for move in moves:
            temp_state = [row.copy() for row in board_state]
            temp_state[move[0]][move[1]] = self.marker
            if self._game.get_winner(temp_state):
                return move
        return None

    def _calculate_move(
        self, board_state: List[List[Optional[str]]]
    ) -> Tuple[int, int]:
        """Determines the AI's next move by first checking for a winning opportunity.

        This method compiles a list of all empty positions on the board. It then checks whether
        any of these moves would result in an immediate win using `_find_winning_move`. If a winning
        move is found, it is selected. Otherwise, a move is chosen at random from the remaining options.

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
        winning_move = self._find_winning_move(moves, board_state)
        if winning_move:
            return winning_move
        else:
            return choice(moves)
