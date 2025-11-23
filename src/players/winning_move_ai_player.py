"""Winning Move AI player for Tic Tac Toe.

Defines the WinningMoveAIPlayer class, which implements a medium-difficulty strategy that checks for
immediate wins before making random moves.
"""

from random import choice

from .abstract_ai_player import AbstractAIPlayer


class WinningMoveAIPlayer(AbstractAIPlayer):
    """Represents an AI player that prioritizes immediate winning moves before selecting randomly.

    This class extends `AbstractAIPlayer` by implementing a strategy that checks for any move
    that would result in a win on the current turn. If no such move exists, it selects randomly
    from the remaining valid options.
    """

    def _find_winning_move(
        self,
        moves: list[tuple[int, int]],
        board_state: list[list[str | None]],
    ) -> tuple[int, int] | None:
        """Scans a list of candidate moves to identify any that result in an immediate win.

        For each available move, this method simulates placing the AI's marker on a copy of the
        current board and checks if it results in a win using the game engine's win detection logic.

        Args:
            moves: A list of (row, column) tuples representing available positions on the board.
            board_state: The current game board as a 2D list, where each cell contains a player
                symbol or None if unoccupied.

        Returns:
            tuple[int, int] | None: The first move found that results in a win, or None if no
            winning move is available.
        """
        for move in moves:
            row, col = move
            temp_state = self._game.get_board_copy(board_state)
            temp_state[row][col] = self.marker
            if self._game.get_winner(temp_state):
                return move
        return None

    def _calculate_move(self, board_state: list[list[str | None]]) -> tuple[int, int]:
        """Determines the AI's next move by first checking for a winning opportunity.

        This method compiles a list of all empty positions on the board. It then checks whether
        any of these moves would result in an immediate win using `_find_winning_move`. If a winning
        move is found, it is selected. Otherwise, a move is chosen at random from the remaining
        options.

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

        winning_move = self._find_winning_move(moves, board_state)

        if winning_move:
            return winning_move
        else:
            return choice(moves)
