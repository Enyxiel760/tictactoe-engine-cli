from src.views import AbstractView
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers import GUIController


class GUIView(AbstractView):

    def __init__(self, master):
        self.root = master
        self.root.title("Tic-Tac-Toe")
        self.board_buttons = []
        self.status_label = None
        self._build_board()
        self._build_status_bar()
        self._controller: "GUIController"

    def set_controller(self, controller: "GUIController") -> None:
        """Injects the Controller reference for handling input callbacks."""
        self._controller = controller

    def handle_click(self, row: int, col: int) -> None:
        """Receives input from the button click and delegates it to the Controller."""
        self._controller.handle_move(row, col)

    def _build_board(self) -> None:
        """Creates and places the 9 game buttons"""
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    self.root,
                    text=" ",
                    width=4,
                    height=2,
                    font=("Ariel", 24),
                    command=lambda r=row, c=col: self.handle_click(r, c),
                )
                button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                button_row.append(button)
            self.board_buttons.append(button_row)

    def _build_status_bar(self) -> None:
        """Creates and places a status bar at row3 col0"""
        self.status_label = tk.Label(
            self.root, text="Welcome!, Player X's turn", font=("Ariel", 12), anchor="w"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)

    def get_game_config(self) -> dict[str, str]:
        """Abstract method to collect all necessary game setup data (names, markers, difficulty).

        The implementing subclass MUST return dict[str, str]: A dictionary containing:
                - "p1_name": Name of Player 1.
                - "p1_marker": Marker chosen by Player 1 ("X" or "O").
                - "p2_type": Difficulty key for Player 2 ("0" for human, otherwise AI key).
                - "p2_name": Name of Player 2 ("Bot" if AI, otherwise user-provided)."""
        pass

    def display_game_state(self) -> None:
        """Abstract method to display the current state of the board.

        This method is called by the Controller during the game loop and takes no direct arguments.
        The implementation must internally fetch the board state from self._game."""
        pass

    def display_message(self, message: str) -> None:
        """General info for the user"""
        pass

    def display_error(self, message: str) -> None:
        """Warning/Error feedback"""
        pass

    def display_winner(self, winner_name: str) -> None:
        """End of game announcement"""
        pass


if __name__ == "__main__":
    root = tk.Tk()
    view = GUIView(root)
    root.mainloop()
