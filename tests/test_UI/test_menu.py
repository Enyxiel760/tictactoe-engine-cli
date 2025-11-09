import unittest
from unittest.mock import patch
from src.UI.menu import *


class TestMenuConstants(unittest.TestCase):
    """Unit tests for constant values defined in the menu module.

    Ensures that MIN_DIFFICULTY and MAX_DIFFICULTY correctly reflect the numeric bounds of
    AI_DIFFICULTIES."""

    def test_ai_difficulty_bounds(self):
        """Verify that MIN_DIFFICULTY and MAX_DIFFICULTY match the minimum and maximum keys
        in AI_DIFFICULTIES."""
        keys = list(map(int, AI_DIFFICULTIES.keys()))
        self.assertEqual(MIN_DIFFICULTY, min(keys))
        self.assertEqual(MAX_DIFFICULTY, max(keys))


@patch("builtins.input")
class TestMenu(unittest.TestCase):
    """Unit tests for interactive methods in the Menu class.
    Simulates user input to validate input handling and return values."""

    def test_get_human_name(self, mock_input):
        """Simulate empty input followed by a valid name.
        Assert that get_human_name returns the non-empty string."""
        mock_input.side_effect = ["", "Alice"]
        result = Menu.get_human_name()
        self.assertEqual(result, "Alice")

    def test_choose_marker(self, mock_input):
        """Simulate invalid marker input followed by a valid choice.
        Assert that choose_marker returns the uppercase valid marker."""
        mock_input.side_effect = ["z", "x"]
        result = Menu.choose_marker()
        self.assertEqual(result, "X")

    def test_choose_ai_difficulty(self, mock_input):
        """Simulate out-of-range difficulty inputs followed by a valid key.
        Assert that choose_ai_difficulty returns the valid difficulty key."""
        mock_input.side_effect = ["0", "5", "2"]
        result = Menu.choose_ai_difficulty()
        self.assertEqual(result, "2")
