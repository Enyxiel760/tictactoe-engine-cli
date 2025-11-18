from abc import ABC, abstractmethod
from src.core import GameEngine
from src.views import AbstractView
from src.core.player_factory import get_player_instances
from src import players


class AbstractController(ABC):
    """The blueprint for all game controllers (CLI, GUI, Web, etc.).
    Responsible for the game lifecycle."""

    view: AbstractView
    engine: GameEngine | None = None

    @abstractmethod
    def run(self) -> None:
        """Starts the main control loop for the game."""
        pass

    def setup_game(self) -> bool:
        """
        Prepares the game environment by collecting configuration, instantiating players,
        initializing the game engine, and injecting dependencies.

        Returns:
            bool: True if setup succeeds; False if any step fails (e.g. invalid config or player creation).
        """
        try:
            setup_data = self.view.get_game_config()
        except Exception as e:
            self.view.display_error(
                f"\nFATAL ERROR: Failed to get game configuration. Error: {e}"
            )
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
