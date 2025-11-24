"""Unit tests for the GUIController.

This module verifies the functionality of the GUIController, including move handling, screen
transitions, player creation, and AI configuration.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.controllers import GUIController
from src.core import GameState
from src.players import AbstractAIPlayer, HumanPlayer


class TestGUIControllerBase(unittest.TestCase):
    """Base class to handle common setup, specifically preventing Tkinter window spawning."""

    def setUp(self):
        """Sets up the test environment by patching Tkinter and initializing the controller."""
        self.patcher_tk = patch("src.controllers.gui_controller.tk.Tk")
        self.mock_tk = self.patcher_tk.start()

        self.controller = GUIController()
        self.controller.view = MagicMock()
        self.controller.engine = MagicMock()

    def tearDown(self):
        """Stops the Tkinter patcher."""
        self.patcher_tk.stop()


class TestHandleMove(TestGUIControllerBase):
    """Tests GUIController's response to valid and invalid player moves."""

    def test_handle_move_ignored_if_ai_turn(self):
        """Ensures handle_move does nothing if it is not a HumanPlayer's turn."""
        ai_player = MagicMock(spec=AbstractAIPlayer)
        self.controller.engine.get_current_player.return_value = ai_player

        self.controller.handle_move(1, 1)

        self.controller.engine.is_valid_move.assert_not_called()
        self.controller.engine.make_move.assert_not_called()

    def test_handle_move_invalid_move(self):
        """Should display error and skip game state update on invalid move."""
        # Must be Human for handle_move to proceed
        self.controller.engine.get_current_player.return_value = MagicMock(spec=HumanPlayer)
        self.controller.engine.is_valid_move.return_value = False

        self.controller.handle_move(1, 1)

        self.controller.view.display_error.assert_called_once_with(
            "Invalid move. Can only place marker on empty spots."
        )
        self.controller.engine.make_move.assert_not_called()

    @patch.object(GUIController, "_handle_post_move")
    def test_handle_move_valid_executes_logic(self, mock_post_move):
        """Should execute move, update view, and delegate to post_move on valid input."""
        self.controller.engine.get_current_player.return_value = MagicMock(spec=HumanPlayer)
        self.controller.engine.is_valid_move.return_value = True

        self.controller.handle_move(1, 1)

        self.controller.engine.make_move.assert_called_once_with((1, 1))
        self.controller.view.display_game_state.assert_called_once()
        # Verify delegation occurs
        mock_post_move.assert_called_once()


class TestWelcomeStart(TestGUIControllerBase):
    """Unit tests for GUIController.handle_welcome_start."""

    def test_welcome_event_triggers_player_creation(self):
        """Verifies that handle_welcome_start shows the player creation screen."""
        self.controller.handle_welcome_start()
        self.controller.view.show_frame.assert_called_once_with(GameState.Frame.PLAYER_CREATION)


class TestPlayerCreationController(TestGUIControllerBase):
    """Tests for GUIController's player creation submission handling."""

    def test_handle_player_creation_submit_stores_name_and_shows_menu(self):
        """Verifies that the controller stores the player name and transitions to the main menu."""
        self.controller.handle_player_creation_submit("Alice")

        self.assertEqual(self.controller._profile_data["p1_name"], "Alice")
        self.controller.view.show_frame.assert_called_once_with(GameState.Frame.MAIN_MENU)


class TestOnePlayerSelect(TestGUIControllerBase):
    """Unit tests for GUIController.handle_1p_select."""

    def test_handle_1p_select_shows_ai_overlay(self):
        """Ensures handle_1p_select calls the view's _show_overlay with the AI_SELECTION state."""
        self.controller.view._show_overlay = MagicMock()
        self.controller.handle_1p_select()
        self.controller.view._show_overlay.assert_called_once_with(GameState.Overlay.AI_SELECTION)


class TestAIConfigSubmission(TestGUIControllerBase):
    """Unit tests for GUIController.handle_ai_config_submission."""

    def setUp(self):
        """Sets up the controller with sample profile data and mocks the launch method."""
        super().setUp()
        self.controller._profile_data = {"p1_name": "Alice"}
        self.controller._launch_game = MagicMock()

    @patch("src.controllers.gui_controller.random.choice", return_value=True)
    def test_ai_config_submission_sets_config_and_launches(self, _):
        """Ensures that AI config submission sets config correctly and triggers launch."""
        self.controller.handle_ai_config_submission("2")

        config = self.controller._current_game_config
        self.assertEqual(config["p1_name"], "Alice")
        self.assertEqual(config["p1_marker"], "X")
        self.assertEqual(config["p2_type"], "2")
        self.assertEqual(config["p2_name"], "Bot")

        self.controller._launch_game.assert_called_once()


# --- Tests for Launch & Game Loop Logic ---


class TestLaunchGame(TestGUIControllerBase):
    """Tests the initialization and startup sequence of the game loop."""

    @patch.object(GUIController, "setup_game", return_value=True)
    @patch.object(GUIController, "_advance_turn")
    def test_launch_game_success(self, mock_advance, mock_setup):
        """Verifies that a successful setup triggers view transition and the first turn."""
        self.controller._launch_game()

        self.controller.view.show_frame.assert_called_once_with(GameState.Frame.GAMEPLAY)
        self.controller.view.display_game_state.assert_called_once()
        mock_advance.assert_called_once()

    @patch.object(GUIController, "setup_game", return_value=False)
    @patch.object(GUIController, "_advance_turn")
    def test_launch_game_failure_aborts(self, mock_advance, mock_setup):
        """Verifies that if setup fails, the game does not transition or start the turn loop."""
        self.controller._launch_game()

        self.controller.view.show_frame.assert_not_called()
        self.controller.view.display_game_state.assert_not_called()
        mock_advance.assert_not_called()


class TestAdvanceTurn(TestGUIControllerBase):
    """Tests the logic for determining the next action based on the current player type."""

    def test_advance_turn_human_waits_for_input(self):
        """Verifies that if it is a Human's turn, the controller waits (no scheduled tasks)."""
        human = MagicMock(spec=HumanPlayer)
        human.name = "Alice"
        human.marker = "X"
        self.controller.engine.get_current_player.return_value = human

        self.controller._advance_turn()

        self.controller.view.display_message.assert_called_with("Alice's Turn (X)")
        self.mock_tk.return_value.after.assert_not_called()

    def test_advance_turn_ai_schedules_execution(self):
        """Verifies that if it is an AI's turn, the move execution is scheduled via Tkinter."""
        ai = MagicMock(spec=AbstractAIPlayer)
        ai.name = "Bot"
        ai.marker = "O"
        self.controller.engine.get_current_player.return_value = ai

        self.controller._advance_turn()

        self.controller.view.display_message.assert_called_with("Bot's Turn (O)")
        self.mock_tk.return_value.after.assert_called_once_with(
            100, self.controller._process_ai_move
        )


class TestProcessAIMove(TestGUIControllerBase):
    """Tests the execution of the AI's move logic."""

    @patch.object(GUIController, "_handle_post_move")
    def test_process_ai_move_executes_correctly(self, mock_post_move):
        """Verifies AI calculates move, engine applies it, and post-move logic runs."""
        ai_player = MagicMock(spec=AbstractAIPlayer)
        expected_move = (0, 0)
        ai_player.get_move.return_value = expected_move
        self.controller.engine.get_current_player.return_value = ai_player

        self.controller._process_ai_move()

        ai_player.get_move.assert_called_once()
        self.controller.engine.make_move.assert_called_once_with(expected_move)
        self.controller.view.display_game_state.assert_called_once()
        mock_post_move.assert_called_once()


class TestHandlePostMove(TestGUIControllerBase):
    """Tests the common logic executed after any move (Human or AI)."""

    @patch.object(GUIController, "_advance_turn")
    def test_handle_post_move_game_over(self, mock_advance):
        """Verifies that if the game is over, the winner is displayed and the turn loop stops."""
        self.controller.engine.check_game_status.return_value = (True, "X")
        self.controller.engine.get_winner_name.return_value = "Alice"

        self.controller._handle_post_move()

        self.controller.view.display_winner.assert_called_once_with("Alice")
        self.controller.engine.switch_player.assert_not_called()
        mock_advance.assert_not_called()

    @patch.object(GUIController, "_advance_turn")
    def test_handle_post_move_continue_game(self, mock_advance):
        """Verifies that if the game continues, players are switched and the next turn starts."""
        self.controller.engine.check_game_status.return_value = (False, None)

        self.controller._handle_post_move()

        self.controller.engine.switch_player.assert_called_once()
        mock_advance.assert_called_once()
