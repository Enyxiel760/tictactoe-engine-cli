from typing import List, Optional, Tuple, TYPE_CHECKING
from abc import abstractmethod
from .abstract_player import AbstractPlayer

if TYPE_CHECKING:
    from src.engine import GameEngine


class AbstractAIPlayer(AbstractPlayer):
    """Intermediate base class for all computer-controlled players.

    This class uses setter injection to acquire the GameEngine instance after initialization and
    provides the implemented 'get_move' method for the top-level contract"""

    _game: "GameEngine"

    def set_engine(self, engine: "GameEngine"):
        """Public method to inject the GameEngine instance after the Player has been created
        to avoid circular dependency between the classes."""
        self._game = engine

    @abstractmethod
    def _calculate_move(
        self, board_state: List[List[Optional[str]]]
    ) -> Tuple[int, int]:
        """Abstract method for the AI's core decision making logic.

        Concrete subclasses will implement this differently according to the given AI's algorithmic
        strategy. Must implement this to return the chosen 0-indexed (row, col) coordinates.
        """
        pass

    def get_move(self) -> Tuple[int, int]:
        """Implements the required get_move() method by requesting the current board state from
        the GameEngine and dlegating the decision to _calculate_move.

        Note: This relies on set_engine() having been called previously."""
        current_board = self._game.get_board_state()
        return self._calculate_move(current_board)
