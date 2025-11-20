from src.controllers import GUIController
from src.core import GameState
from unittest.mock import MagicMock, patch
import unittest


class TestHandleMove(unittest.TestCase):
    """Tests GUIController's response to valid and invalid player moves."""

    def setUp(self):
        """Sets up a GUIController with mocked engine and view."""
        self.controller = GUIController()
        self.controller.view = MagicMock()
        self.controller.engine = MagicMock()

    def test_handle_move_invalid_move(self):
        """Should display error and skip game state update on invalid move."""
        self.controller.engine.is_valid_move.return_value = False
        self.controller.handle_move(1, 1)
        self.controller.view.display_error.assert_called_once_with(
            "Invalid move. Can only place marker on empty spots."
        )
        self.controller.engine.make_move.assert_not_called()
        self.controller.engine.switch_player.assert_not_called()
        self.controller.view.display_game_state.assert_not_called()

    def test_handle_move_valid_continue(self):
        """Should update game state and switch player on valid move."""
        self.controller.engine.is_valid_move.return_value = True
        self.controller.engine.check_game_status.return_value = (False, "X")
        self.controller.handle_move(1, 1)
        self.controller.engine.make_move.assert_called_once_with((1, 1))
        self.controller.view.display_game_state.assert_called_once()
        self.controller.engine.switch_player.assert_called_once()


class TestWelcomeStart(unittest.TestCase):
    """Unit tests for GUIController.handle_welcome_start.

    Verifies that the controller correctly transitions from the welcome
    screen to the player creation screen by delegating to the view.
    """

    def setUp(self):
        """Initializes a GUIController with a mocked view."""
        self.controller = GUIController()
        self.controller.view = MagicMock()

    def test_welcome_event_triggers_player_creation(self):
        """Verifies that handle_welcome_start shows the player creation screen."""
        self.controller.view.show_frame = MagicMock()
        self.controller.handle_welcome_start()
        self.controller.view.show_frame.assert_called_once_with(
            GameState.PLAYER_CREATION
        )
