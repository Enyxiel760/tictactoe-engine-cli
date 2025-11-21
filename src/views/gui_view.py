from src.views import AbstractView
from src.core import GameState
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers import GUIController


class GUIView(AbstractView):
    """GUI-based view for rendering Tic-Tac-Toe screens and handling user interactions.

    This class manages the layout and transitions between different game states,
    delegates input events to the controller, and provides methods for updating the GUI.
    """

    def __init__(self, master):
        """Initializes the GUI view and sets up the root container.

        Creates the main layout frame, configures grid weights, and prepares the view manager
        for handling state-based screen transitions.
        """

        self.root = master
        self.root.title("Tic-Tac-Toe")

        self.board_buttons = []
        self._controller: "GUIController"

        self.container = tk.Frame(self.root)
        self.frames = {}  # Holds map of State -> Frame instance
        self.container.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

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

        welcome_frame.bind("<Key>", self.handle_welcome_event)
        welcome_canvas.bind("<Button-1>", self.handle_welcome_event)
        welcome_frame.focus_set()

        return welcome_frame

    def handle_welcome_event(self, event) -> None:
        """Handles input events from the welcome screen and delegates to the controller.

        Args:
            event (tk.Event): The keypress or mouse click event triggering the transition.
        """
        self._controller.handle_welcome_start()

    def _create_newplayer_frame(self):
        """Creates the player creation screen for entering Player 1's profile.

        This frame provides:
            - A text entry field bound to a StringVar for Player 1's name.
            - A label describing the input field.
            - A button to save the profile and continue, which delegates to
              handle_player_creation_submit.

        The frame is configured to expand within the root container and uses
        grid layout with column weight for responsive resizing.

        Returns:
            tk.Frame: The frame containing the player creation UI elements.
        """
        creation_frame = tk.Frame(self.container, bg="blue")
        creation_frame.grid(row=0, column=0, sticky="nsew")
        creation_frame.grid_columnconfigure(0, weight=1)

        self._p1_name_var = tk.StringVar(value="Player 1")
        row_index = 0

        tk.Label(creation_frame, text="Player Name: ").grid(
            row=row_index, column=0, sticky="w"
        )
        tk.Entry(creation_frame, textvariable=self._p1_name_var).grid(
            row=row_index, column=1, sticky="ew"
        )
        row_index += 1

        tk.Button(
            creation_frame,
            text="Save Profile and Continue",
            command=self.handle_player_creation_submit,
        ).grid(row=row_index, column=0, columnspan=2, sticky="ew")

        return creation_frame

    def handle_player_creation_submit(self):
        """Handles submission of the player creation form.

        Retrieves the entered Player 1 name from the bound StringVar and
        delegates the submission logic to the controller.

        This method acts as the bridge between the GUI input field and the
        controller's player creation workflow.
        """
        player_name = self._p1_name_var.get()
        self._controller.handle_player_creation_submit(player_name)

    def _create_menu_frame(self):
        menu_frame = tk.Frame(self.container, bg="red")
        menu_frame.grid(row=0, column=0, sticky="nsew")
        menu_frame.grid_columnconfigure(0, weight=1)

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

        menu_frame.focus_set()
        return menu_frame

    def _create_gameplay_frame(self):
        pass

    def _create_game_over_frame(self):
        pass

    def show_frame(self, state: GameState.Frame):
        """Displays the requested screen based on the current GameState.

        If the frame has not been created yet, it invokes the corresponding factory method,
        grids the frame into the container, and raises it to the front.

        Args:
            state_enum (GameState): The game state to display.
        """
        if state not in self.frames:
            frame_instance = getattr(self, state.creation_func)()
            self.frames[state] = frame_instance
            frame_instance.grid(row=0, column=0, sticky="nsew", in_=self.container)

        frame = self.frames[state]
        frame.tkraise()
        frame.focus_force()

    def set_controller(self, controller: "GUIController") -> None:
        """Injects the controller reference for handling input events and callbacks.

        Args:
            controller (GUIController): The controller instance to bind to this view.
        """
        self._controller = controller

    def handle_click(self, row: int, col: int) -> None:
        """Handles a board button click and delegates the move to the controller.

        Args:
            row (int): The row index of the clicked button.
            col (int): The column index of the clicked button.
        """
        self._controller.handle_move(row, col)

    # --- TODO:  refactor into create_gameplay_frame ---
    def _build_board(self, master) -> None:
        """Creates and places the 3x3 grid of game buttons.

        Args:
            master (tk.Widget): The parent widget to contain the buttons.
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
    def _build_status_bar(self, master) -> None:
        """Creates and places a status bar below the game board.

        Args:
            master (tk.Widget): The parent widget to contain the status label.
        """

        self.status_label = tk.Label(
            master, text="Welcome!, Player X's turn", font=("Arial", 12), anchor="w"
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
