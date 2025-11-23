"""Abstract view definition for Tic Tac Toe.

Defines the contract for all View implementations (CLI, GUI, etc.), enforcing a common interface
for game configuration, state display, and user feedback.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import GameEngine


class AbstractView(ABC):
    """Defines the contract for all View implementations (CLI, GUI, etc.).

    Centralizes engine dependency injection and enforces public methods required by the
    Controller.

    Attributes:
        _game: The game engine instance, injected via set_engine().
    """

    _game: "GameEngine | None" = None

    def set_engine(self, engine: "GameEngine") -> None:
        """Implements the required dependency injection for all subclasses.

        Called by the Controller after the GameEngine has been instantiated.

        Args:
            engine: The game engine instance to bind.
        """
        self._game = engine

    @abstractmethod
    def get_game_config(self) -> dict[str, str]:
        """Collects all necessary game setup data (names, markers, difficulty).

        Returns:
            dict[str, str]: A dictionary containing:
                - "p1_name": Name of Player 1.
                - "p1_marker": Marker chosen by Player 1 ("X" or "O").
                - "p2_type": Difficulty key for Player 2 ("0" for human, otherwise AI key).
                - "p2_name": Name of Player 2 ("Bot" if AI, otherwise user-provided).
        """
        pass

    @abstractmethod
    def display_game_state(self) -> None:
        """Displays the current state of the board.

        This method is called by the Controller during the game loop. The implementation must
        internally fetch the board state from `self._game`.
        """
        pass

    @abstractmethod
    def display_message(self, message: str) -> None:
        """Displays a general informational message to the user.

        Args:
            message: The message string to display.
        """
        pass

    @abstractmethod
    def display_error(self, message: str) -> None:
        """Displays a warning or error message to the user.

        Args:
            message: The error description to display.
        """
        pass

    @abstractmethod
    def display_winner(self, winner_name: str | None) -> None:
        """Announces the result of the game.

        Args:
            winner_name: The name of the winner, or None if the game ended in a draw.
        """
        pass
