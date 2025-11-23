"""GUI view implementation for Tic Tac Toe.

Provides a Tkinter-based graphical interface, managing screen transitions, input handling, and
rendering of the game state.
"""

import tkinter as tk
from typing import TYPE_CHECKING

from src.core import GameState, PlayerType
from src.views import AbstractView

if TYPE_CHECKING:
    from src.controllers import GUIController

ORIGIN = {"row": 0, "column": 0}


class GUIView(AbstractView):
    """GUI-based view for rendering Tic-Tac-Toe screens and handling user interactions.

    This class manages the layout and transitions between different game states, delegates input
    events to the controller, and provides methods for updating the GUI.

    Attributes:
        root: The root Tkinter window.
        container: The main frame acting as a container for all view frames.
        frames: A dictionary mapping GameState enums to instantiated frames.
        board_buttons: A 3x3 list of button widgets representing the game grid.
        status_label: A label widget for displaying game status and turn information.
    """

    def __init__(self, master: tk.Tk):
        """Initializes the GUI view and sets up the root container.

        Creates the main layout frame, configures grid weights, and prepares the view manager
        for handling state-based screen transitions.

        Args:
            master: The root Tkinter window.
        """
        self.root = master
        self.root.title("Tic-Tac-Toe")

        self.board_buttons: list[list[tk.Button]] = []
        self.status_label: tk.Label | None = None
        self._controller: GUIController

        self.container = tk.Frame(self.root)
        self.frames: dict[GameState.Frame, tk.Frame] = {}
        self.container.grid(**ORIGIN, sticky="nsew")

        # Configure the root and container to expand
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

    def set_controller(self, controller: "GUIController") -> None:
        """Injects the controller reference for handling input events and callbacks.

        Args:
            controller: The controller instance to bind to this view.
        """
        self._controller = controller

    # --- Frame Creation Methods ---

    def _create_welcome_frame(self) -> tk.Frame:
        """Creates the welcome screen with a canvas prompt and binds input events.

        Returns:
            tk.Frame: The frame containing the welcome canvas.
        """
        welcome_frame = tk.Frame(self.container, bg="black")

        welcome_canvas = tk.Canvas(welcome_frame, bg="black")
        welcome_canvas.pack(expand=True, fill="both")

        welcome_canvas.create_text(
            200,
            150,
            text="- Press any key to start -",
            fill="white",
            font=("Arial", 24),
            tag="start_text",
        )

        # Bind events to trigger the transition
        welcome_frame.bind("<Key>", self.handle_welcome_event)
        welcome_canvas.bind("<Button-1>", self.handle_welcome_event)

        return welcome_frame

    def _create_newplayer_frame(self) -> tk.Frame:
        """Creates the player creation screen for entering Player 1's profile.

        Returns:
            tk.Frame: The frame containing the player creation UI elements.
        """
        creation_frame = tk.Frame(self.container, bg="blue")
        name = tk.StringVar(value="Player 1")

        tk.Label(creation_frame, text="Player Name: ").grid(**ORIGIN, sticky="w")
        tk.Entry(creation_frame, textvariable=name).grid(row=0, column=1, sticky="ew")

        tk.Button(
            creation_frame,
            text="Save Profile and Continue",
            command=lambda: self._controller.handle_player_creation_submit(name.get()),
        ).grid(row=1, column=0, columnspan=2, sticky="ew")

        return creation_frame

    def _create_menu_frame(self) -> tk.Frame:
        menu_frame = tk.Frame(self.container, bg="red")

        tk.Label(menu_frame, text="Select Game Mode", font=("Arial", 16)).pack(pady=5)

        tk.Button(
            menu_frame,
            text="1 Player (vs AI)",
            width=20,
            command=self._controller.handle_1p_select,
        ).pack(pady=5)

        tk.Button(
            menu_frame,
            text="2 Player (Human)",
            width=20,
            command=self._controller.handle_2p_select,
        ).pack(pady=5)

        return menu_frame

    def _create_gameplay_frame(self) -> tk.Frame:
        """Creates the main gameplay screen with the board and status bar.

        Returns:
            tk.Frame: The gameplay frame.
        """
        pass

    def _create_game_over_frame(self) -> tk.Frame:
        """Creates a game over frame.

        Returns:
            tk.Frame: The game over frame.
        """
        pass

    # --- Overlay Creation Methods ---

    def _create_ai_select_overlay(self) -> tk.Frame:
        """Creates the AI difficulty selection overlay.

        Returns:
            tk.Frame: The AI selection overlay frame.
        """
        overlay_frame = tk.Frame(self.container, padx=20, pady=20, bg="#202020")

        tk.Label(
            overlay_frame,
            text="Choose Opponent Difficulty:",
            font=("Arial", 12),
            fg="white",
            bg="#202020",
        ).pack(pady=10)

        for key, description in PlayerType.get_ai_options():
            tk.Button(
                overlay_frame,
                text=description,
                command=lambda k=key: self._controller.handle_ai_config_submission(k),
            ).pack(pady=5, padx=20)

        return overlay_frame

    # --- Navigation & Event Handling ---

    def show_frame(self, state: GameState.Frame) -> None:
        """Displays the requested screen based on the current GameState.Frame.

        If the frame has not been created yet, it invokes the corresponding factory method.

        Args:
            state: The game state enum corresponding to the frame to display.
        """
        if state not in self.frames:
            # Dynamically call the creation function defined in the Enum metadata
            creation_method = getattr(self, state.creation_func)
            frame_instance = creation_method()
            self.frames[state] = frame_instance
            frame_instance.grid(**ORIGIN, sticky="nsew", in_=self.container)

        frame = self.frames[state]
        frame.tkraise()
        frame.focus_force()

    def _show_overlay(self, overlay: GameState.Overlay) -> None:
        """Displays an overlay frame on top of the current content.

        Args:
            overlay: The game state enum corresponding to the overlay to display.
        """
        creation_method = getattr(self, overlay.creation_func)
        overlay_frame = creation_method()

        overlay_frame.grid(**ORIGIN, sticky="nsew", in_=self.container)
        overlay_frame.tkraise()
        overlay_frame.focus_set()

    def handle_welcome_event(self, event: tk.Event) -> None:
        """Handles input events from the welcome screen and delegates to the controller.

        Args:
            event: The input event triggering the transition.
        """
        self._controller.handle_welcome_start()

    def handle_click(self, row: int, col: int) -> None:
        """Handles a board button click and delegates the move to the controller.

        Args:
            row (int): The row index of the clicked button.
            col (int): The column index of the clicked button.
        """
        self._controller.handle_move(row, col)

    # --- AbstractView Implementation ---

    def get_game_config(self) -> dict[str, str]:
        """Retrieves the current game configuration.

        Returns:
            dict[str, str]: The configuration dictionary from the controller.
        """
        return self._controller._current_game_config

    def display_game_state(self) -> None:
        """Abstract method to display the current state of the board.

        This method is called by the Controller during the game loop and takes no direct arguments.
        The implementation must internally fetch the board state from self._game.
        """
        pass

    def display_message(self, message: str) -> None:
        """Displays general info for the user via a popup.

        Args:
            message: The message string to display.
        """
        pass

    def display_error(self, message: str) -> None:
        """Displays warning or error feedback via a popup.

        Args:
            message: The error message to display.
        """
        pass

    def display_winner(self, winner_name: str | None) -> None:
        """Announces the end of the game.

        Args:
            winner_name: The name of the winner, or None if it is a draw.
        """
        pass

    # --- TODO:  refactor into create_gameplay_frame ---
    def _build_board(self, master: tk.Widget) -> None:
        """Create and place the 3x3 grid of game buttons.

        Args:
            master (tk.Widget): The parent widget that will contain the buttons.
        """
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    master,
                    text=" ",
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    command=lambda r=row, c=col: self.handle_click(r, c),
                )
                button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                button_row.append(button)
            self.board_buttons.append(button_row)

    # --- TODO:  refactor into create_gameplay_frame ---
    def _build_status_bar(self, master: tk.Widget) -> None:
        """Create and place a status bar below the game board.

        Args:
            master (tk.Widget): The parent widget that will contain the status label.
        """
        self.status_label = tk.Label(
            master, text="Welcome!, Player X's turn", font=("Arial", 12), anchor="w"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)
