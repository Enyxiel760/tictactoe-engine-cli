from src.controllers import AbstractController
from src import views
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

    def run(self) -> None:
        """Starts the GUI event loop after successful game setup.

        If setup fails (e.g., due to invalid configuration), the loop is not started.
        """
        if not self.setup_game():
            return  # Exit if setup failed. (e.g. bad config)
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
