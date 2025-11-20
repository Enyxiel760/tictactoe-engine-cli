import unittest
from unittest.mock import MagicMock
from src.views import GUIView


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
