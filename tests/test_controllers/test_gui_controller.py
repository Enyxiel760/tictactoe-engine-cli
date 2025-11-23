"""Unit tests for the GUIController.

This module verifies the functionality of the GUIController, including move handling, screen
transitions, player creation, and AI configuration.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.controllers import GUIController
from src.core import GameState


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

    Verifies that the controller correctly transitions from the welcome screen to the player
    creation screen by delegating to the view.
    """

    def setUp(self):
        """Initializes a GUIController with a mocked view."""
        self.controller = GUIController()
        self.controller.view = MagicMock()

    def test_welcome_event_triggers_player_creation(self):
        """Verifies that handle_welcome_start shows the player creation screen."""
        self.controller.view.show_frame = MagicMock()
        self.controller.handle_welcome_start()
        self.controller.view.show_frame.assert_called_once_with(GameState.Frame.PLAYER_CREATION)


class TestPlayerCreationController(unittest.TestCase):
    """Tests for GUIController's player creation submission handling."""

    def setUp(self):
        """Initializes a GUIController with a mocked view."""
        self.controller = GUIController()
        self.controller.view = MagicMock()
        self.controller._profile_data = {}

    def test_handle_player_creation_submit_stores_name_and_shows_menu(self):
        """Verifies that the controller stores the player name and transitions to the main menu."""
        self.controller.handle_player_creation_submit("Alice")

        # Profile data should contain the submitted name
        self.assertEqual(self.controller._profile_data["p1_name"], "Alice")

        # View should transition to the main menu
        self.controller.view.show_frame.assert_called_once_with(GameState.Frame.MAIN_MENU)


class TestOnePlayerSelect(unittest.TestCase):
    """Unit tests for GUIController.handle_1p_select.

    Verifies that selecting the one-player option correctly triggers the AI selection overlay by
    delegating to the view.
    """

    def setUp(self):
        """Initializes a GUIController with a mocked view."""
        self.controller = GUIController()
        self.controller.view = MagicMock()

    def test_handle_1p_select_shows_ai_overlay(self):
        """Ensures handle_1p_select calls the view's _show_overlay with the AI_SELECTION state."""
        self.controller.view._show_overlay = MagicMock()
        self.controller.handle_1p_select()
        self.controller.view._show_overlay.assert_called_once_with(GameState.Overlay.AI_SELECTION)


class TestAIConfigSubmission(unittest.TestCase):
    """Unit tests for GUIController.handle_ai_config_submission.

    Verifies that AI configuration submission stores the correct setup data in the controller and
    triggers game launch.
    """

    def setUp(self):
        """Initializes a GUIController with mocked view and launch method."""
        self.controller = GUIController()
        self.controller.view = MagicMock()
        self.controller._profile_data = {"p1_name": "Alice"}
        self.controller._launch_game = MagicMock()

    @patch("src.controllers.gui_controller.random.choice", return_value=True)
    def test_ai_config_submission_sets_config_and_launches(self, _):
        """Ensures that handle_ai_config_submission populates the game configuration.

        Verifies that it sets Player 1's name, randomized marker, Player 2's type and name,and then
        calls _launch_game.
        """
        self.controller.handle_ai_config_submission("2")  # difficulty key
        config = self.controller._current_game_config

        self.assertEqual(config["p1_name"], "Alice")
        self.assertEqual(config["p1_marker"], "X")  # forced by mock_choice
        self.assertEqual(config["p2_type"], "2")
        self.assertEqual(config["p2_name"], "Bot")

        self.controller._launch_game.assert_called_once()
