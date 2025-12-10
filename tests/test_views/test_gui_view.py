"""Unit tests for the GUIView class.

This module validates the behavior of the graphical user interface view, ensuring that:
- Frames and widgets are created correctly.
- Game state updates are reflected in the UI (board buttons).
- Status messages and error handling update the status label.
- User interactions are delegated to the controller.
"""

import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

from src.core import GameState
from src.views import GUIView


class TestGUIViewBase(unittest.TestCase):
    """Base class for GUIView tests to handle common setup and mocking."""

    def setUp(self):
        """Sets up the test environment by patching Tkinter widgets and initializing the view."""
        self.patcher_frame = patch("src.views.gui_view.tk.Frame")
        self.patcher_button = patch("src.views.gui_view.tk.Button")
        self.patcher_label = patch("src.views.gui_view.tk.Label")
        self.patcher_entry = patch("src.views.gui_view.tk.Entry")
        self.patcher_stringvar = patch("src.views.gui_view.tk.StringVar")
        self.patcher_canvas = patch("src.views.gui_view.tk.Canvas")

        self.mock_frame = self.patcher_frame.start()
        self.mock_button = self.patcher_button.start()
        self.mock_label = self.patcher_label.start()
        self.mock_entry = self.patcher_entry.start()
        self.mock_stringvar = self.patcher_stringvar.start()
        self.mock_canvas = self.patcher_canvas.start()

        # Ensure each widget creation returns a distinct mock
        self.mock_button.side_effect = lambda *args, **kwargs: MagicMock()
        self.mock_label.side_effect = lambda *args, **kwargs: MagicMock()
        self.mock_frame.side_effect = lambda *args, **kwargs: MagicMock()
        self.mock_entry.side_effect = lambda *args, **kwargs: MagicMock()
        self.mock_stringvar.side_effect = lambda *args, **kwargs: MagicMock()
        self.mock_canvas.side_effect = lambda *args, **kwargs: MagicMock()

        self.mock_master = MagicMock()
        self.view = GUIView(self.mock_master)
        self.mock_controller = MagicMock()
        # Initialize attributes to prevent MagicMock auto-creation issues
        self.mock_controller._profile_data = {"p1_name": "Player 1"}
        self.mock_controller._current_game_config = {}
        self.view.set_controller(self.mock_controller)
        self.mock_engine = MagicMock()
        self.view.set_engine(self.mock_engine)

    def tearDown(self):
        """Stops the Tkinter widgets."""
        self.patcher_frame.stop()
        self.patcher_button.stop()
        self.patcher_label.stop()
        self.patcher_entry.stop()
        self.patcher_stringvar.stop()
        self.patcher_canvas.stop()


class TestInitialization(TestGUIViewBase):
    """Tests the initialization of the GUIView class."""

    def test_sets_window_title(self):
        """Tests that the window title is set correctly upon initialization."""
        self.mock_master.title.assert_called_with("Tic-Tac-Toe")

    def test_initializes_frames_dict(self):
        """Tests that the frames dictionary is initialized empty."""
        self.assertEqual(self.view.frames, {})

    def test_initializes_board_buttons(self):
        """Tests that the board_buttons attribute is initialized as an empty list."""
        self.assertEqual(self.view.board_buttons, [])


class TestSetController(TestGUIViewBase):
    """Tests controller injection."""

    def test_assigns_controller_reference(self):
        """Tests that set_controller correctly assigns the controller."""
        controller = MagicMock()
        self.view.set_controller(controller)
        self.assertIs(self.view._controller, controller)


class TestCreateWelcomeFrame(TestGUIViewBase):
    """Tests welcome frame creation logic and event binding."""

    @patch("src.views.gui_view.tk.Canvas")
    def test_create_canvas_with_text(self, mock_canvas):
        """Tests that _create_welcome_frame creates a canvas with welcome text."""
        self.view._create_welcome_frame()

        canvas = mock_canvas.return_value
        canvas.create_text.assert_called()

    def test_binds_keyboard_event(self):
        """Tests that welcome frame binds keyboard events."""
        # The frame mock returned by _create_welcome_frame
        frame = self.view._create_welcome_frame()
        frame.bind.assert_called()


class TestCreateNewPlayerFrame(TestGUIViewBase):
    """Tests player creation frame logic."""

    def test_creates_entry_field(self):
        """Tests that _create_new_player_frame creates an entry field for player name."""
        self.view._create_newplayer_frame()
        self.mock_entry.assert_called_once()

    def test_submit_button_triggers_controller(self):
        """Tests that the Submit button delegates to controller."""
        self.view._create_newplayer_frame()

        # Find the button's command (it's the last button created in this method)
        submit_button_call = self.mock_button.call_args_list[-1]
        _, kwargs = submit_button_call
        command = kwargs.get("command")

        # Simulate button click
        if command:
            command()
            self.mock_controller.handle_player_creation_submit.assert_called()


class TestCreateMenuFrame(TestGUIViewBase):
    """Tests menu frame creation logic."""

    def test_creates_mode_selection_buttons(self):
        """Tests that _create_menu_frame creates mode selection buttons."""
        self.view._create_menu_frame()

        # Should create at least two buttons for mode selection
        self.assertTrue(self.mock_button.call_count >= 2)

    def test_one_player_button_triggers_controller(self):
        """Tests that the One Player button delegates to controller."""
        self.view._create_menu_frame()

        # First button should be Player 1
        _, kwargs = self.mock_button.call_args_list[0]
        command = kwargs.get("command")

        # Simulate button click
        self.assertEqual(command, self.mock_controller.handle_1p_select)

    def test_two_player_button_triggers_controller(self):
        """Tests that 2P button delegates to controller."""
        self.view._create_menu_frame()

        # Second button should be Player 2
        _, kwargs = self.mock_button.call_args_list[1]
        command = kwargs.get("command")

        self.assertEqual(command, self.mock_controller.handle_2p_select)


class TestCreateGameplayFrame(TestGUIViewBase):
    """Tests the initialization logic of the gameplay frame."""

    def test_initializes_widgets(self):
        """Tests that _create_gameplay_frame builds the board grid and status label."""
        frame = self.view._create_gameplay_frame()

        self.mock_frame.assert_called()
        self.assertIsNotNone(frame)

        # Verify 3x3 grid creation
        self.assertEqual(len(self.view.board_buttons), 3)
        for row in self.view.board_buttons:
            self.assertEqual(len(row), 3)
            for btn in row:
                self.assertIsInstance(btn, MagicMock)

        # Verify Status Label creation and initial text
        self.mock_label.assert_called()
        self.assertIsNotNone(self.view.status_label)

        _, kwargs = self.mock_label.call_args
        self.assertEqual(kwargs.get("text"), "Loading...")


class TestCreateAISelectOverlay(TestGUIViewBase):
    """Tests AI difficulty selection overlay."""

    @patch("src.core.PlayerType.get_ai_options")
    def test_creates_button_for_each_difficulty(self, mock_get_ai_options):
        """Tests that a button is created for each AI difficulty option."""
        mock_get_ai_options.return_value = [("EASY", "Easy"), ("HARD", "Hard")]

        self.view._create_ai_select_overlay()

        # Should create 2 buttons (one per difficulty)
        self.assertEqual(self.mock_button.call_count, 2)

    @patch("src.core.PlayerType.get_ai_options")
    def test_difficulty_button_triggers_controller(self, mock_get_ai_options):
        """Tests that clicking an AI difficulty button delegates to the controller."""
        mock_get_ai_options.return_value = [("EASY", "Easy")]

        self.view._create_ai_select_overlay()

        # Get the created button's command
        _, kwargs = self.mock_button.call_args_list[0]
        command = kwargs.get("command")

        # Simulate button click
        command()
        self.mock_controller.handle_ai_config_submission.assert_called_with("EASY")


class TestCreateTwoPlayerSetupOverlay(TestGUIViewBase):
    """Tests for the Two Player Setup Overlay creation and interactions."""

    def test_creates_widgets(self):
        """Verifies that the overlay initializes the necessary input widgets."""
        self.view._create_two_player_setup_overlay()

        self.mock_entry.assert_called()
        # Verify Buttons (4 markers + 1 start)
        self.assertTrue(self.mock_button.call_count >= 5)

    def test_start_button_triggers_submission(self):
        """Tests that the Start Game button delegates to the controller."""
        self.view._create_two_player_setup_overlay()
        start_button_call = self.mock_button.call_args_list[-1]
        _, kwargs = start_button_call
        command = kwargs.get("command")

        # Simulate Click
        command()

        self.mock_controller.handle_2p_config_submission.assert_called()

    def test_marker_toggle_logic(self):
        """Tests that clicking Player 1's 'O' button toggles the visual state."""
        # Setup: Capture button instances to inspect config calls
        created_buttons = []
        self.mock_button.side_effect = lambda *args, **kwargs: (
            created_buttons.append(mock := MagicMock()) or mock
        )

        self.view._create_two_player_setup_overlay()

        # Identify buttons based on creation order in `_create_two_player_setup_overlay`
        # Order: P1-X, P1-O, P2-X, P2-O, Start
        p1_x, p1_o = created_buttons[0], created_buttons[1]
        p2_x, p2_o = created_buttons[2], created_buttons[3]

        # Find the command bound to P1-O (to switch P1 to O)
        _, kwargs = self.mock_button.call_args_list[1]  # second button created (P1-O)
        command = kwargs["command"]

        # Execute Toggle (Select P1 as 'O')
        command()

        # Verify P1-O is now active (sunken)
        p1_o.config.assert_called_with(relief="sunken", bg="#606060", fg="white")
        # Verify P1-X is now inactive (raised)
        p1_x.config.assert_called_with(relief="raised", bg="#303030", fg="#888")

        # Verify P2-X is active (enforced opposite)
        p2_x.config.assert_called_with(relief="sunken", bg="#606060", fg="white")
        # Verify P2-O is inactive
        p2_o.config.assert_called_with(relief="raised", bg="#303030", fg="#888")


class TestShowFrame(TestGUIViewBase):
    """Tests frame navigation and caching logic."""

    def test_creates_and_caches(self):
        """Tests that show_frame creates a frame on first access and reuses it thereafter."""
        self.view.frames = {}

        # First call: Should create
        self.view.show_frame(GameState.Frame.GAMEPLAY)

        self.assertIn(GameState.Frame.GAMEPLAY, self.view.frames)
        self.view.frames[GameState.Frame.GAMEPLAY].grid.assert_called()

        # Second call: Should reuse
        cached_frame = self.view.frames[GameState.Frame.GAMEPLAY]
        self.view.show_frame(GameState.Frame.GAMEPLAY)

        self.assertIs(self.view.frames[GameState.Frame.GAMEPLAY], cached_frame)
        cached_frame.tkraise.assert_called()


class TestShowOverlay(TestGUIViewBase):
    """Tests overlay display logic."""

    def test_overlays_frame(self):
        """Tests that show_overlay creates and displays the overlay frame."""
        mock_overlay = MagicMock()
        mock_overlay.creation_func = "_create_ai_select_overlay"

        with patch.object(self.view, mock_overlay.creation_func, return_value=MagicMock()) as mk:
            self.view._show_overlay(mock_overlay)
            mk.assert_called_once()


class TestHandleWelcomeEvent(TestGUIViewBase):
    """Tests welcome screen event handling."""

    def test_delegates_to_controller(self):
        """Tests that handle_welcome_event delegates to controller."""
        mock_event = MagicMock()
        self.view.handle_welcome_event(mock_event)
        self.mock_controller.handle_welcome_start.assert_called_once()


class TestHandleClick(TestGUIViewBase):
    """Tests interaction delegation."""

    def test_delegates_to_controller(self):
        """Tests that clicking a board button delegates to controller.handle_move."""
        self.view._create_gameplay_frame()

        # Simulate a click action
        self.view.handle_click(0, 1)

        self.mock_controller.handle_move.assert_called_once_with(0, 1)


class TestGetGameConfig(TestGUIViewBase):
    """Tests game configuration retrieval."""

    def test_returns_controller_config(self):
        """Tests that get_game_config retrieves configuration from the controller."""
        expected_config = {"mode": "2P", "p1_marker": "X"}
        self.mock_controller._current_game_config = expected_config

        result = self.view.get_game_config()

        self.assertEqual(result, expected_config)


class TestDisplayGameState(TestGUIViewBase):
    """Tests the visual updates of the game board."""

    def test_updates_board(self):
        """Tests that display_game_state updates button text based on the engine's board."""
        self.view._create_gameplay_frame()

        mock_board = [
            ["X", None, None],
            [None, "O", None],
            [None, None, None],
        ]
        self.mock_engine.get_board_state.return_value = mock_board

        self.view.display_game_state()

        # Check specific button updates
        self.view.board_buttons[0][0].config.assert_called_with(text="X")
        self.view.board_buttons[1][1].config.assert_called_with(text="O")
        self.view.board_buttons[0][1].config.assert_called_with(text=" ")

    def test_handles_empty_board(self):
        """Tests that display_game_state handles an empty board correctly."""
        self.view._create_gameplay_frame()

        mock_board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.mock_engine.get_board_state.return_value = mock_board

        self.view.display_game_state()

        # All buttons should show space
        for row in self.view.board_buttons:
            for btn in row:
                btn.config.assert_called_with(text=" ")


class TestDisplayMessage(TestGUIViewBase):
    """Tests general status message updates."""

    def test_updates_status_label(self):
        """Tests that display_message updates the status label text and color."""
        self.view._create_gameplay_frame()

        self.view.display_message("Player X's Turn")

        self.view.status_label.config.assert_called_with(text="Player X's Turn", fg="black")


class TestDisplayError(TestGUIViewBase):
    """Tests error message feedback."""

    def test_formatting(self):
        """Tests that display_error adds a warning icon and sets color to red."""
        self.view._create_gameplay_frame()

        self.view.display_error("Invalid Move")

        self.view.status_label.config.assert_called_with(text="⚠️ Invalid Move", fg="red")


class TestDisplayWinner(TestGUIViewBase):
    """Tests game over announcements."""

    def setUp(self):
        """Initializes the gameplay frame before tests, ensuring buttons and status label exist."""
        super().setUp()
        self.view._create_gameplay_frame()

    def test_formatting_winner(self):
        """Tests formatting for a decisive win."""
        self.view.display_winner("Alice")
        self.view.status_label.config.assert_called_with(text="🎉 Winner: Alice! 🎉", fg="green")

    def test_formatting_draw(self):
        """Tests formatting for a draw."""
        self.view.display_winner(None)
        self.view.status_label.config.assert_called_with(text="🤝 It's a draw! 🤝", fg="blue")


class TestStatusLabelGuards(TestGUIViewBase):
    """Tests that display methods handle missing status_label gracefully."""

    def test_display_message_without_label(self):
        """Tests that display_message does not raise an error if status_label is None."""
        self.view.status_label = None
        try:
            self.view.display_message("Test")
        except Exception as e:
            self.fail(f"display_message raised an exception unexpectedly: {e}")

    def test_display_error_without_label(self):
        """Tests that display_error does not raise an error if status_label is None."""
        self.view.status_label = None
        try:
            self.view.display_error("Test")
        except Exception as e:
            self.fail(f"display_error raised an exception unexpectedly: {e}")

    def test_display_winner_without_label(self):
        """Tests that display_winner does not raise an error if status_label is None."""
        self.view.status_label = None
        try:
            self.view.display_winner("Alice")
        except Exception as e:
            self.fail(f"display_winner raised an exception unexpectedly: {e}")

            class TestCreateWelcomeFrame(TestGUIViewBase):
                """Tests welcome frame creation logic and event binding."""

                def test_create_canvas_with_text(self):
                    """Tests that _create_welcome_frame creates a canvas with welcome text."""
                    self.view._create_welcome_frame()

                    canvas = self.mock_canvas.call_args_list[-1]
                    _, kwargs = canvas
                    self.assertIn("width", kwargs)
                    self.assertIn("height", kwargs)

                def test_binds_keyboard_event(self):
                    """Tests that welcome frame binds keyboard events."""
                    frame = self.view._create_welcome_frame()
                    frame.bind.assert_called()

                def test_frame_background_color(self):
                    """Tests that the welcome frame has a black background."""
                    self.view._create_welcome_frame()

                    _, kwargs = self.mock_frame.call_args_list[-1]
                    self.assertEqual(kwargs.get("bg"), "black")

                def test_canvas_created_with_black_background(self):
                    """Tests that the canvas is created with a black background."""
                    self.view._create_welcome_frame()

                    canvas_call = self.mock_canvas.call_args_list[-1]
                    _, kwargs = canvas_call
                    self.assertEqual(kwargs.get("bg"), "black")

                def test_canvas_text_content(self):
                    """Tests that the canvas contains the correct welcome text."""
                    frame = self.view._create_welcome_frame()

                    # Verify frame.bind was called for keyboard event
                    frame.bind.assert_any_call("<Key>", self.view.handle_welcome_event)

                def test_binds_click_event(self):
                    """Tests that welcome frame binds click events to canvas."""
                    self.view._create_welcome_frame()

                    # Verify canvas.bind was called for click event
                    canvas_instance = self.mock_canvas.return_value
                    canvas_instance.bind.assert_called_with(
                        "<Button-1>", self.view.handle_welcome_event
                    )

                def test_returns_frame_instance(self):
                    """Tests that _create_welcome_frame returns a Frame instance."""
                    result = self.view._create_welcome_frame()

                    self.assertIsNotNone(result)
                    self.assertIsInstance(result, tk.Frame)

                def test_canvas_packed_with_expand_and_fill(self):
                    """Tests that the canvas is packed with expand and fill options."""
                    self.view._create_welcome_frame()

                    canvas_instance = self.mock_canvas.return_value
                    canvas_instance.pack.assert_called_with(expand=True, fill="both")

                def test_both_keyboard_and_click_bound_to_same_handler(self):
                    """Tests that keyboard and click events delegate to handle_welcome_event."""
                    frame = self.view._create_welcome_frame()

                    # Check frame.bind calls
                    frame.bind.assert_any_call("<Key>", self.view.handle_welcome_event)

                    # Check canvas.bind calls
                    canvas_instance = self.mock_canvas.return_value
                    canvas_instance.bind.assert_called_with(
                        "<Button-1>", self.view.handle_welcome_event
                    )
