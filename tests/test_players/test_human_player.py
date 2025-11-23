"""Unit tests for the HumanPlayer class.

This module validates the input handling logic of the HumanPlayer, ensuring that invalid inputs
(non-numeric, out-of-range) are rejected and valid inputs are correctly converted to coordinates.
"""

import unittest
from unittest.mock import patch

from src.players import HumanPlayer


@patch("builtins.input")
class TestHumanPlayerGetMove(unittest.TestCase):
    """Tests the HumanPlayer.get_move method's input validation and coordinate conversion."""

    @classmethod
    def setUpClass(cls):
        """Initializes a HumanPlayer instance for testing."""
        cls.player = HumanPlayer(name="TestPlayer", marker="X")

    def test_get_move_non_numeric(self, mock_input):
        """Tests that the function handles non-numeric input.

        Scenario:
            1. User enters 'hello' (Invalid).
            2. User enters '5' (Valid).
        """
        mock_input.side_effect = ["hello", "5"]
        result = self.player.get_move()
        self.assertEqual(result, (1, 1))

    def test_get_move_valid_input(self, mock_input):
        """Tests the base case of receiving a single, valid numeric input.

        Input '8' should map to coordinates (2, 1).
        """
        mock_input.return_value = "8"
        result = self.player.get_move()
        self.assertEqual(result, (2, 1))

    def test_get_move_low_boundary(self, mock_input):
        """Tests the low boundary condition.

        Scenario:
            1. User enters '0' (Invalid, out of range).
            2. User enters '1' (Valid, first square).
        """
        mock_input.side_effect = ["0", "1"]
        result = self.player.get_move()
        self.assertEqual(result, (0, 0))

    def test_get_move_high_boundary(self, mock_input):
        """Tests the high boundary condition.

        Scenario:
            1. User enters '10' (Invalid, out of range).
            2. User enters '9' (Valid, last square).
        """
        mock_input.side_effect = ["10", "9"]
        result = self.player.get_move()
        self.assertEqual(result, (2, 2))
