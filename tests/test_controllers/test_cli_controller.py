import unittest
from unittest.mock import MagicMock
from src.controllers import CLIController
from src.players import HumanPlayer


class TestCLIController(unittest.TestCase):
    def setUp(self):
        self.controller = CLIController()
        self.controller.view = MagicMock()
        self.controller.engine = MagicMock()

    def test_game_loop_handles_invalid_move(self):
        """
        Verify the controller loops until a valid move is found.
        Scenario:
        1. Player sends Invalid Move
        2. Engine says 'False' (invalid)
        3. View displays error
        4. Player sends Valid Move
        5. Engine says 'True' (valid)
        """
        mock_player = MagicMock(spec=HumanPlayer)
        mock_player.name = "TestBot"
        mock_player.marker = "X"
        mock_player.get_move.side_effect = [1, 2]  # Returns 1 (bad), then 2 (good)

        self.controller.engine.get_current_player.return_value = mock_player

        # Define validation logic: 1 is invalid, 2 is valid
        def is_valid_side_effect(move):
            return move == 2

        self.controller.engine.is_valid_move.side_effect = is_valid_side_effect

        # We break the loop after one successful turn for testing purposes
        # by making check_game_status return True (Game Over) on the second call
        self.controller.engine.check_game_status.side_effect = [
            (False, None),  # Start of loop
            (True, "X"),  # End of loop
        ]

        self.controller._play_game()

        self.controller.view.display_error.assert_called_with(
            "Invalid move. Can only place marker on empty spots."
        )

        self.assertEqual(mock_player.get_move.call_count, 2)
        self.controller.engine.make_move.assert_called_once_with(2)
        self.controller.engine.switch_player.assert_called_once()
        self.controller.view.display_game_state.assert_called_once()
        self.assertEqual(self.controller.view.display_message.call_count, 2)
        self.controller.view.display_message.assert_called_with(
            "\n--- It's TestBot's turn (X). ---"
        )
