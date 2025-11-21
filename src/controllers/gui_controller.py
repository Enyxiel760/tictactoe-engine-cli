from src.controllers import AbstractController
from src import views
from src.core import GameState
import tkinter as tk


class GUIController(AbstractController):
    """GUI-based controller for managing Tic-Tac-Toe gameplay.

    This class bridges the GUI view and the game engine, handling user interactions
    and coordinating game state updates.
    """

    def __init__(self):
        """Initializes the GUI controller with a Tkinter root and GUI view.

        Sets up the view and binds the controller to it.
        """
        self.root = tk.Tk()
        self.view = views.GUIView(self.root)
        self.view.set_controller(self)
        # Stores the current player profile data in a structured way (for future expansion)
        self._profile_data = {}

    def run(self) -> None:
        """Starts the GUI application.

        Displays the welcome screen and enters the Tkinter main event loop.
        """
        self.view.show_frame(GameState.Frame.WELCOME_SCREEN)
        self.root.mainloop()

    def handle_move(self, row: int, col: int) -> None:
        """Processes a move received from the GUI and updates the game state.

        Validates the move, applies it to the engine, checks for game completion,
        and updates the view accordingly. If the move is invalid, an error message is displayed.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        """
        if self.engine.is_valid_move((row, col)):
            self.engine.make_move((row, col))

            is_over, winner_marker = self.engine.check_game_status()
            self.view.display_game_state()

            if is_over:
                winner_name = self.engine.get_winner_name(winner_marker)
                self.view.display_winner(winner_name)
                # end game logic - lock board/switch to game over state.
            else:
                self.engine.switch_player()

        else:
            self.view.display_error(
                "Invalid move. Can only place marker on empty spots."
            )
            return

    def handle_welcome_start(self) -> None:
        """Handles the welcome screen input event.

        Transitions the application from the welcome screen to the player creation screen.
        """
        self.view.show_frame(GameState.Frame.PLAYER_CREATION)

    def handle_player_creation_submit(self, player_name: str) -> None:
        """Processes the submitted player profile and transitions to the main menu.

        Stores the provided Player 1 name in the profile data dictionary and
        instructs the view to display the main menu screen.

        Args:
            player_name (str): The name entered for Player 1.
        """
        self._profile_data["p1_name"] = player_name
        self.view.show_frame(GameState.Frame.MAIN_MENU)

    def handle_1p_select(self):
        pass

    def handle_2p_select(self):
        pass


if __name__ == "__main__":
    controller = GUIController()
    controller.run()
