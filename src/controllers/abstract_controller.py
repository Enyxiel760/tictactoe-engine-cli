"""Abstract controller definitions for Tic Tac Toe.

This module defines the AbstractController base class, which provides the blueprint for all
controller implementations (CLI, GUI, Web, etc.).
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src import players
from src.core import GameEngine
from src.core.player_factory import get_player_instances

if TYPE_CHECKING:
    from src.views import AbstractView


class AbstractController(ABC):
    """The blueprint for all game controllers (CLI, GUI, Web, etc.).

    Responsible for the game lifecycle.

    Attributes:
        view: The view component associated with this controller.
        engine: The game engine instance.
    """

    view: "AbstractView"
    engine: GameEngine | None = None

    @abstractmethod
    def run(self) -> None:
        """Starts the main control loop for the game."""
        pass

    def setup_game(self) -> bool:
        """Prepares the game environment.

        Collects configuration, instantiates players, initializes the game engine, and injects
        dependencies.

        Returns:
            bool: True if setup succeeds; False if any step fails.
        """
        try:
            setup_data = self.view.get_game_config()
        except Exception as e:
            self.view.display_error(f"\nFATAL ERROR: Failed to get game configuration. Error: {e}")
            return False

        try:
            player_x, player_o = get_player_instances(setup_data)
        except Exception as e:
            self.view.display_error(
                f"\nFATAL ERROR: Failed to create players from config. Error: {e}"
            )
            return False

        self.engine = GameEngine(player_x, player_o)
        self.view.set_engine(self.engine)

        for player in (player_x, player_o):
            if not isinstance(player, players.HumanPlayer):
                player.set_engine(self.engine)

        return True
