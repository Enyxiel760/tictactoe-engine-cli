"""CLI controller for Tic Tac Toe.

Provides a command-line interface implementation of the AbstractController, managing game setup, the
main loop, and end-of-game handling.
"""

import time

from src import views
from src.controllers import AbstractController
from src.players import AbstractAIPlayer


class CLIController(AbstractController):
    """Command-line controller for Tic Tac Toe.

    Uses a CLIView to interact with the user and orchestrates the game lifecycle.
    """

    def __init__(self):
        """Initialize the CLIController."""
        self.view = views.CLIView()

    def run(self) -> None:
        """Run the full game lifecycle.

        Orchestrates setup, the gameplay loop, and end-of-game handling. This method is the primary
        entry point invoked by main.py.
        """
        if not self.setup_game():
            return  # Exit if setup failed (e.g. bad config)

        self._play_game()
        self._handle_game_over()

    def _play_game(self):
        """Execute the main game loop.

        Alternates turns between players until the game concludes. Handles move validation, board
        updates, and player switching. Displays game state and prompts for input on each turn.
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

            # Artificial delay for AI players to improve UX
            if isinstance(current_player, AbstractAIPlayer):
                self.view.display_message(f"{current_player.name} is thinking...")
                time.sleep(2)

            # Get Move
            move = current_player.get_move()
            while not self.engine.is_valid_move(move):
                self.view.display_error("Invalid move. Can only place marker on empty spots.")
                move = current_player.get_move()

            self.engine.make_move(move)
            self.engine.switch_player()

    def _handle_game_over(self):
        """Finalize the game.

        Renders the final board state and announces the winner.
        """
        self.view.display_game_state()

        _, winner_marker = self.engine.check_game_status()
        winner_name = self.engine.get_winner_name(winner_marker)

        self.view.display_winner(winner_name)
