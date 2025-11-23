"""Abstract AI player definition for Tic Tac Toe.

Defines the base class for all computer-controlled players, handling engine injection and
delegating move calculation to concrete strategy implementations.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING

from .abstract_player import AbstractPlayer

if TYPE_CHECKING:
    from src.core.engine import GameEngine


class AbstractAIPlayer(AbstractPlayer):
    """Intermediate base class for all computer-controlled players.

    This class uses setter injection to acquire the GameEngine instance after initialization and
    enforces the implementation of a move calculation strategy.

    Attributes:
        _game: The injected GameEngine instance used to query board state.
    """

    _game: "GameEngine | None" = None

    def set_engine(self, engine: "GameEngine") -> None:
        """Injects the GameEngine instance into the player.

        This allows the AI to query the game state (e.g., board positions) to calculate moves,
        avoiding circular dependencies during initialization.

        Args:
            engine: The active GameEngine instance.
        """
        self._game = engine

    @abstractmethod
    def _calculate_move(self, board_state: list[list[str | None]]) -> tuple[int, int]:
        """Calculates the best move based on the current board state.

        Concrete subclasses must implement this method to define their specific algorithmic
        strategy.

        Args:
            board_state: A 3x3 list of lists representing the current board.

        Returns:
            tuple[int, int]: The calculated (row, col) coordinates for the move.
        """
        pass

    def get_move(self) -> tuple[int, int]:
        """Retrieves the AI's chosen move.

        Requests the current board state from the engine and delegates decision-making to the
        _calculate_move implementation.

        Returns:
            tuple[int, int]: The (row, col) coordinates of the move.

        Raises:
            RuntimeError: If the game engine has not been injected via set_engine().
        """
        current_board = self._game.get_board_state()
        return self._calculate_move(current_board)
