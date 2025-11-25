"""Unit tests for the GUIView class.

This module validates the behavior of the graphical user interface view, ensuring that:
- Frames and widgets are created correctly.
- Game state updates are reflected in the UI (board buttons).
- Status messages and error handling update the status label.
- User interactions are delegated to the controller.
"""

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

        self.mock_frame = self.patcher_frame.start()
        self.mock_button = self.patcher_button.start()
        self.mock_label = self.patcher_label.start()

        # Each Button call returns a fresh mock with its own .config
        def make_button(*args, **kwargs):
            btn = MagicMock()
            btn.config = MagicMock()
            return btn

        self.mock_button.side_effect = make_button

        # Initialize GUIView with a fake master
        self.mock_master = MagicMock()
        self.view = GUIView(self.mock_master)

        # Attach controller and engine mocks
        self.mock_controller = MagicMock()
        self.view.set_controller(self.mock_controller)
        self.mock_engine = MagicMock()
        self.view.set_engine(self.mock_engine)

    def tearDown(self):
        """Stops the Tkinter widgets."""
        self.patcher_frame.stop()
        self.patcher_button.stop()
        self.patcher_label.stop()


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


class TestHandleClick(TestGUIViewBase):
    """Tests interaction delegation."""

    def test_delegates_to_controller(self):
        """Tests that clicking a board button delegates to controller.handle_move."""
        self.view._create_gameplay_frame()

        # Simulate a click action
        self.view.handle_click(0, 1)

        self.mock_controller.handle_move.assert_called_once_with(0, 1)


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
