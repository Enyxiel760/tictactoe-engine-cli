import unittest
from unittest.mock import patch
from textwrap import dedent
from src.players.abstract_player import AbstractPlayer
from src.UI import CLIView
from src.engine import GameEngine
from src.core import PlayerType


class DummyPlayer(AbstractPlayer):
    """A concrete player class used only for testing the GameEngine.
    It complies with the full AbstractPlayer contract."""

    def get_move(self):
        return (0, 0)


@patch("builtins.input")
class TestCLIView(unittest.TestCase):
    """Unit tests for interactive methods in the Menu class.
    Simulates user input to validate input handling and return values."""

    def setUp(self):
        self.player_x = DummyPlayer("XPlayer", marker="X")
        self.player_o = DummyPlayer("OPlayer", marker="O")
        self.game = GameEngine(self.player_x, self.player_o)
        self.view = CLIView()

    def test_get_human_name(self, mock_input):
        """Simulate empty input followed by a valid name.
        Assert that get_human_name returns the non-empty string."""
        mock_input.side_effect = ["", "Alice"]
        result = self.view._get_human_name()
        self.assertEqual(result, "Alice")

    def test_choose_marker(self, mock_input):
        """Simulate invalid marker input followed by a valid choice.
        Assert that choose_marker returns the uppercase valid marker."""
        mock_input.side_effect = ["z", "x"]
        result = self.view._choose_marker()
        self.assertEqual(result, "X")

    @patch.object(PlayerType, "get_max_difficulty_key")
    @patch.object(PlayerType, "get_min_difficulty_key")
    def test_choose_ai_difficulty(self, mock_min_key, mock_max_key, mock_input):
        """Simulate out-of-range difficulty inputs followed by a valid key.
        Assert that choose_ai_difficulty returns the valid difficulty key."""
        mock_input.side_effect = ["0", "5", "2"]
        result = self.view._choose_ai_difficulty()
        self.assertEqual(result, "2")
        mock_min_key.assert_called()
        mock_max_key.assert_called()


@patch.object(CLIView, "_choose_ai_difficulty")
@patch.object(CLIView, "_choose_play_mode")
@patch.object(CLIView, "_choose_marker")
@patch.object(CLIView, "_get_human_name")
class TestGetGameConfig(unittest.TestCase):
    """Unit tests for CLIView.get_game_config using patched input methods.

    Validates correct configuration output for both single-player and two-player modes,
    ensuring player names, markers, and AI difficulty are correctly assigned."""

    def setUp(self):
        self.player_x = DummyPlayer("XPlayer", marker="X")
        self.player_o = DummyPlayer("OPlayer", marker="O")
        self.game = GameEngine(self.player_x, self.player_o)
        self.view = CLIView()

    def test_get_game_config_1player(
        self, mock_name, mock_marker, mock_mode, mock_difficulty
    ):
        """Simulates a single-player setup with AI difficulty.

        Asserts that the configuration dictionary correctly reflects the human player's name,
        chosen marker, and AI difficulty level."""
        mock_name.return_value = "Alice"
        mock_marker.return_value = "O"
        mock_mode.return_value = "ai"
        mock_difficulty.return_value = "4"
        result = self.view.get_game_config()
        self.assertEqual(result["p1_name"], "Alice")
        self.assertEqual(result["p1_marker"], "O")
        self.assertEqual(result["p2_type"], "4")
        self.assertEqual(result["p2_name"], "Bot")
        mock_name.assert_called_once()

    def test_get_game_config_2player(
        self, mock_name, mock_marker, mock_mode, mock_difficulty
    ):
        """Simulates a two-player setup with two human names.

        Asserts that the configuration dictionary correctly reflects both player names,
        chosen marker, and default AI type for human opponents."""
        mock_name.side_effect = ["Fred", "Alice"]
        mock_marker.return_value = "X"
        mock_mode.return_value = "human"
        result = self.view.get_game_config()
        self.assertEqual(result["p1_name"], "Fred")
        self.assertEqual(result["p1_marker"], "X")
        self.assertEqual(result["p2_type"], "0")
        self.assertEqual(result["p2_name"], "Alice")
        self.assertEqual(mock_name.call_count, 2)


class TestPrettifyBoard(unittest.TestCase):
    """Tests the prettify_board method's formatting on empty and fully occupied boards."""

    def setUp(self):
        self.player_x = DummyPlayer("XPlayer", marker="X")
        self.player_o = DummyPlayer("OPlayer", marker="O")
        self.game = GameEngine(self.player_x, self.player_o)
        self.view = CLIView()
        self.view.set_engine(self.game)

    def test_prettify_empty_board(self):
        """Test that an empty board is formatted correctly, converting all None values to spaces (' ')."""
        pretty_board = self.view.prettify_board()

        expected_board = dedent(
            """\
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
            |   |   |   |
            -------------
        """
        )
        self.assertEqual(pretty_board, expected_board)

    def test_prettify_full_board(self):
        """Tests that a fully occupied board with 'X' and 'O' symbols is formatted correctly."""
        self.game.board = [["X", "O", "O"], ["O", "O", "X"], ["X", "X", "O"]]

        expected_board = dedent(
            """\
            -------------
            | X | O | O |
            -------------
            | O | O | X |
            -------------
            | X | X | O |
            -------------
        """
        )
        pretty_board = self.view.prettify_board()
        self.assertEqual(pretty_board, expected_board)
