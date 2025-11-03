import unittest
from unittest.mock import patch
from src.players.human_player import HumanPlayer


@patch("builtins.input")
class TestHumanPlayerGetMove(unittest.TestCase):
    """Tests the HumanPlayer.get_move method's input validation (numeric and range) and coordinate conversion."""

    @classmethod
    def setUpClass(cls):
        cls.player = HumanPlayer(name="TestPlayer", marker="X")

    def test_get_move_non_numeric(self, mock_input):
        """Tests that the function handles non-numeric input ('hello') by looping once and then
        accepting the valid input '5'."""
        mock_input.side_effect = ["hello", "5"]
        result = self.player.get_move()
        self.assertEqual(result, (1, 1))

    def test_get_move_valid_input(self, mock_input):
        """Tests the base case of receiving a single, valid numeric input ('8') and verifying the correct
        coordinates (2, 1)."""
        mock_input.return_value = "8"
        result = self.player.get_move()
        self.assertEqual(result, (2, 1))

    def test_get_move_low_boundary(self, mock_input):
        """Tests the low boundary condition by rejecting '0' and then accepting the valid input '1'."""
        mock_input.side_effect = ["0", "1"]
        result = self.player.get_move()
        self.assertEqual(result, (0, 0))

    def test_get_move_high_boundary(self, mock_input):
        """Tests the high boundary condition by rejecting '10' and then accepting the valid input '9'."""
        mock_input.side_effect = ["10", "9"]
        result = self.player.get_move()
        self.assertEqual(result, (2, 2))
