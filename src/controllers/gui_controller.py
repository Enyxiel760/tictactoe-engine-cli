"""GUI controller for Tic Tac Toe.

Provides a Tkinter-based interface that bridges the GUI view and the game engine, handling user
interactions and coordinating game state updates.
"""

import random
import tkinter as tk
from typing import Any

from src import views
from src.controllers import AbstractController
from src.core import GameState


class GUIController(AbstractController):
    """GUI-based controller for managing Tic-Tac-Toe gameplay.

    This class bridges the GUI view and the game engine, handling user interactions and coordinating
    game state updates.

    Attributes:
        root: The main Tkinter window.
        view: The GUI view instance.
        _profile_data: Temporary storage for player profile information.
        _current_game_config: Configuration dictionary used to initialize the game.
    """

    def __init__(self):
        """Initializes the GUI controller with a Tkinter root and GUI view.

        Sets up the view and binds the controller to it.
        """
        self.root = tk.Tk()
        self.view = views.GUIView(self.root)
        self.view.set_controller(self)

        # Stores the current player profile data in a structured way (for future expansion)
        self._profile_data: dict[str, Any] = {}
        self._current_game_config: dict[str, Any] = {}

    def run(self) -> None:
        """Starts the GUI application.

        Displays the welcome screen and enters the Tkinter main event loop.
        """
        self.view.show_frame(GameState.Frame.WELCOME_SCREEN)
        self.root.mainloop()

    def handle_move(self, row: int, col: int) -> None:
        """Processes a move received from the GUI and updates the game state.

        Validates the move, applies it to the engine, checks for game completion, and updates the
        view accordingly. If the move is invalid, an error message is displayed.

        Args:
            row: The row index of the move.
            col: The column index of the move.
        """
        if self.engine is None:
            self.view.display_error("Game engine is not initialized.")
            return

        move = (row, col)

        if self.engine.is_valid_move(move):
            self.engine.make_move(move)

            is_over, winner_marker = self.engine.check_game_status()
            self.view.display_game_state()

            if is_over:
                winner_name = self.engine.get_winner_name(winner_marker)
                self.view.display_winner(winner_name)
                # Future: Add logic to lock board or show game over screen
            else:
                self.engine.switch_player()

        else:
            self.view.display_error("Invalid move. Can only place marker on empty spots.")

    def handle_welcome_start(self) -> None:
        """Handles the welcome screen input event.

        Transitions the application from the welcome screen to the player creation screen.
        """
        self.view.show_frame(GameState.Frame.PLAYER_CREATION)

    def handle_player_creation_submit(self, player_name: str) -> None:
        """Processes the submitted player profile and transitions to the main menu.

        Stores the provided Player 1 name in the profile data dictionary and instructs the view to
        display the main menu screen.

        Args:
            player_name: The name entered for Player 1.
        """
        self._profile_data["p1_name"] = player_name
        self.view.show_frame(GameState.Frame.MAIN_MENU)

    def handle_1p_select(self) -> None:
        """Handles the 1-player menu input event.

        Transitions the application from the main menu to the ai selection screen.
        """
        self.view._show_overlay(GameState.Overlay.AI_SELECTION)

    def handle_ai_config_submission(self, difficulty_key: str) -> None:
        """Stores the necessary config, randomizes markers, and launches the game.

        Args:
            difficulty_key: The difficulty level selected for the AI (e.g., 'easy', 'hard').
        """
        if random.choice([True, False]):
            p1_marker = "X"
        else:
            p1_marker = "O"

        # Store the configuration state for the final factory assembly
        self._current_game_config = {
            "p1_name": self._profile_data.get("p1_name"),
            "p1_marker": p1_marker,
            "p2_type": difficulty_key,
            "p2_name": "Bot",
        }

        self._launch_game()

    def handle_2p_select(self) -> None:
        """Handle the 2-player menu input event.

        Transitions the application from the main menu to the player creation screen.
        """
        # TODO: Implement 2-player setup logic
        pass


if __name__ == "__main__":
    controller = GUIController()
    controller.run()
