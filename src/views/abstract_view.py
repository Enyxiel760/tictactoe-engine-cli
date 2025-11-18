from abc import ABC, abstractmethod
from src.core import GameEngine


class AbstractView(ABC):
    """Defines the contract for all View implementations (CLI, GUI, etc.).
    Centralizes engine dependency injection and enforces public methods
    required by the Controller (main.py)."""

    _game: "GameEngine"  # Set via set_engine()

    def set_engine(self, engine: "GameEngine") -> None:
        """Implements the required dependency injection for all subclasses.

        Called by the Controller after the GameEngine has been instantiated.

        Args:
            engine (GameEngine): The game engine instance to bind."""
        self._game = engine

    @abstractmethod
    def get_game_config(self) -> dict[str, str]:
        """Abstract method to collect all necessary game setup data (names, markers, difficulty).

        The implementing subclass MUST return dict[str, str]: A dictionary containing:
                - "p1_name": Name of Player 1.
                - "p1_marker": Marker chosen by Player 1 ("X" or "O").
                - "p2_type": Difficulty key for Player 2 ("0" for human, otherwise AI key).
                - "p2_name": Name of Player 2 ("Bot" if AI, otherwise user-provided)."""
        pass

    @abstractmethod
    def display_game_state(self) -> None:
        """Abstract method to display the current state of the board.

        This method is called by the Controller during the game loop and takes no direct arguments.
        The implementation must internally fetch the board state from self._game."""
        pass

    @abstractmethod
    def display_message(self, message: str) -> None:
        """General info for the user"""
        pass

    @abstractmethod
    def display_error(self, message: str) -> None:
        """Warning/Error feedback"""
        pass

    @abstractmethod
    def display_winner(self, winner_name: str) -> None:
        """End of game announcement"""
        pass
