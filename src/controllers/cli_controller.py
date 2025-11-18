from src.controllers.abstract_controller import AbstractController
from src.core.engine import GameEngine
from src import views, players
from src.core.player_factory import get_player_instances


class CLIController(AbstractController):
    def __init__(self):
        self.view = None
        self.engine = None

    def run(self) -> None:
        """The main entry point called by main.py"""
        # 1. Setup Phase
        if not self._setup_game():
            return  # Exit if setup failed (e.g. bad config)

        # 2. Game Loop Phase
        self._play_game()

        # 3. End Phase
        self._handle_game_over()

    def _setup_game(self) -> bool:
        """Handles View creation, Config, Factory, and DI."""
        # 1. Instantiate View
        self.view = views.cli_view()

        # 2. Get Config
        try:
            setup_data = self.view.get_game_config()
        except Exception as e:
            self.view.display_error(
                f"\nFATAL ERROR: Failed to get game configuration. Error: {e}"
            )
            return False

        # 3. Create Players
        try:
            player_x, player_o = get_player_instances(setup_data)
        except Exception as e:
            self.view.display_error(
                f"\nFATAL ERROR: Failed to create players from config. Error: {e}"
            )
            return False

        # 4. Instantiate Engine
        self.engine = GameEngine(player_x, player_o)

        # 5. Inject Dependencies
        self.view.set_engine(self.engine)
        for player in (player_x, player_o):
            if not isinstance(player, players.HumanPlayer):
                player.set_engine(self.engine)

        return True

    def _play_game(self):
        """The main while loop."""
        print("\n--- Game Starting! ---\n")

        while True:
            # Check Status
            is_over, _ = self.engine.check_game_status()
            if is_over:
                break

            current_player = self.engine.get_current_player()

            # Display State
            self.view.display_message(
                f"\n--- It's {current_player.name}'s turn ({current_player.marker}). ---"
            )
            self.view.display_game_state()

            # Get Move
            move = current_player.get_move()
            while not self.engine.is_valid_move(move):
                self.view.display_error(
                    "Invalid move. Can only place marker on empty spots."
                )
                move = current_player.get_move()

            self.engine.make_move(move)
            self.engine.switch_player()

    def _handle_game_over(self):
        """Final rendering and winner announcement."""
        # Render final board
        self.view.display_game_state()

        # Determine winner
        _, winner_marker = self.engine.check_game_status()
        winner_name = self.engine.get_winner_name(winner_marker)

        self.view.display_winner(winner_name)
