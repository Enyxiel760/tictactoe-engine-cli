from src.controllers import AbstractController
from src import views


class CLIController(AbstractController):

    def __init__(self):
        """
        Initializes the CLIController with a CLI-based view and prepares the game engine placeholder.

        Attributes:
            view (CLIView): The command-line interface view for user interaction.
            engine (GameEngine | None): The core game engine, instantiated during setup.
        """
        self.view = views.CLIView()

    def run(self) -> None:
        """
        Orchestrates the full game lifecycle: setup, gameplay loop, and end-of-game handling.

        This method is the primary entry point invoked by main.py. It ensures the game is properly
        configured before entering the main loop, and gracefully handles termination.
        """
        if not self.setup_game():
            return  # Exit if setup failed (e.g. bad config)

        self._play_game()
        self._handle_game_over()

    def _play_game(self):
        """
        Executes the main game loop, alternating turns between players until the game concludes.

        Handles move validation, board updates, and player switching. Displays game state
        and prompts for input on each turn.
        """
        self.view.display_message("\n--- Game Starting! ---\n")

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
        """
        Finalizes the game by rendering the board and announcing the winner.

        Retrieves the winning marker from the engine and delegates winner display to the view.
        """
        self.view.display_game_state()

        _, winner_marker = self.engine.check_game_status()
        winner_name = self.engine.get_winner_name(winner_marker)

        self.view.display_winner(winner_name)
