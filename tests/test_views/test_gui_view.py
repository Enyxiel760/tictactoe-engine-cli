import unittest
from unittest.mock import MagicMock, patch
from src.views import GUIView
from src.core import GameState


class TestHandleClick(unittest.TestCase):
    """Tests that GUIView delegates click events to the controller."""

    def setUp(self):
        """Sets up GUIView with a mocked controller."""
        self.mock_controller = MagicMock()
        self.view = GUIView(MagicMock())
        self.view.set_controller(self.mock_controller)

    def test_handle_click_calls_controller(self):
        """Verifies that clicking on an empty spot calls the controller with correct coordinates."""
        self.view.handle_click(1, 2)
        self.mock_controller.handle_move.assert_called_once_with(1, 2)


class TestShowFrames(unittest.TestCase):
    """Unit tests for GUIView.show_frame behavior.

    Verifies that frame creation methods are invoked only once per state,
    and that subsequent calls reuse the cached frame instance.
    """

    def setUp(self):
        """Initializes a GUIView instance with a mocked Tkinter root."""
        self.view = GUIView(MagicMock())

    @patch("src.views.gui_view.GUIView._create_welcome_frame", return_value=MagicMock())
    def test_show_frame(self, mock_func):
        """Tests that show_frame creates a frame once and reuses it thereafter.

        Steps:
            1. Clear the frames cache and rebuild views_map to point to the patched method.
            2. Call show_frame for WELCOME_SCREEN and assert the creator was invoked.
            3. Call show_frame again and verify the cached frame is reused.
        """
        self.view.frames = {}
        self.view._setup_view_manager()

        # First call should invoke the creator
        self.view.show_frame(GameState.WELCOME_SCREEN)
        mock_func.assert_called_once()

        # Second call should reuse cached frame
        self.view.show_frame(GameState.WELCOME_SCREEN)
        self.assertIn(GameState.WELCOME_SCREEN, self.view.frames)

        # Verify the cached frame is the same instance
        frame1 = self.view.frames[GameState.WELCOME_SCREEN]
        self.view.show_frame(GameState.WELCOME_SCREEN)
        frame2 = self.view.frames[GameState.WELCOME_SCREEN]
        self.assertIs(frame1, frame2)


class TestPlayerCreationView(unittest.TestCase):
    """Tests for GUIView's player creation submission handling."""

    def setUp(self):
        self.mock_controller = MagicMock()
        self.view = GUIView(MagicMock())
        self.view.set_controller(self.mock_controller)
        self.view._p1_name_var = MagicMock()
        self.view._p1_name_var.get.return_value = "Alice"

    def test_handle_player_creation_submit_delegates_to_controller(self):
        """Verifies that the view passes the entered name to the controller."""
        self.view.handle_player_creation_submit()
        self.mock_controller.handle_player_creation_submit.assert_called_once_with(
            "Alice"
        )
