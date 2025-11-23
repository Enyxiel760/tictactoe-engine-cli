"""Unit tests for the CLIController.

This module validates the specific behavior of the Command-Line Interface controller, including the
main game loop, move validation retry logic, and interaction with the view and engine.
"""

import unittest
from unittest.mock import MagicMock

from src.controllers import CLIController
from src.players import HumanPlayer


class TestCLIController(unittest.TestCase):
    """Test suite for CLIController logic."""

    def setUp(self):
        """Initialize the controller with mocked dependencies."""
        self.controller = CLIController()
        self.controller.view = MagicMock()
        self.controller.engine = MagicMock()

    def test_game_loop_handles_invalid_move(self):
        """Verify the controller loops until a valid move is found.

        Scenario:
            1. Player sends an invalid move (e.g., 1).
            2. Engine reports it as invalid.
            3. View displays an error message.
            4. Player sends a valid move (e.g., 2).
            5. Engine accepts the move.
        """
        # Setup Mock Player
        mock_player = MagicMock(spec=HumanPlayer)
        mock_player.name = "TestBot"
        mock_player.marker = "X"
        # Returns 1 (bad), then 2 (good)
        mock_player.get_move.side_effect = [1, 2]

        self.controller.engine.get_current_player.return_value = mock_player

        # Define validation logic: 1 is invalid, 2 is valid
        def is_valid_side_effect(move):
            return move == 2

        self.controller.engine.is_valid_move.side_effect = is_valid_side_effect

        # Control the game loop:
        # 1. False -> Loop continues (Start of turn)
        # 2. True -> Loop breaks (End of turn/Game Over logic trigger)
        self.controller.engine.check_game_status.side_effect = [
            (False, None),
            (True, "X"),
        ]

        # Execute private method _play_game directly for isolation
        self.controller._play_game()

        # Assertions
        self.controller.view.display_error.assert_called_with(
            "Invalid move. Can only place marker on empty spots."
        )

        self.assertEqual(mock_player.get_move.call_count, 2)
        self.controller.engine.make_move.assert_called_once_with(2)
        self.controller.engine.switch_player.assert_called_once()

        # display_game_state is called once per loop iteration before the move
        self.controller.view.display_game_state.assert_called_once()

        # display_message is called twice: "Game Starting" + "Player's Turn"
        self.assertEqual(self.controller.view.display_message.call_count, 2)

        # Verify the last call was the turn announcement
        self.controller.view.display_message.assert_called_with(
            "\n--- It's TestBot's turn (X). ---"
        )
