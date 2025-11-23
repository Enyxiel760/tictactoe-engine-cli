"""Unit tests for the AbstractPlayer base class.

This module verifies the contract enforcement of the AbstractPlayer class, ensuring that
subclasses must implement required methods and that initialization logic functions correctly.
"""

import unittest

from src.players import AbstractPlayer


class IncompletePlayer(AbstractPlayer):
    """Fails to implement get_move to test abstract enforcement."""

    pass


class CompletePlayer(AbstractPlayer):
    """Minimally complete subclass to verify instantiation."""

    def get_move(self):
        """Stub implementation of the abstract method."""
        return (0, 0)


class TestAbstractPlayerContract(unittest.TestCase):
    """Unit tests for the AbstractPlayer interface contract."""

    def test_abstract_player_enforce_get_move(self):
        """Tests that attempting to instantiate an incomplete subclass raises TypeError.

        Note:
            While testing language features is generally redundant, this test confirms that
            the abstract inheritance structure is correctly defined.
        """
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            IncompletePlayer(name="Fail", marker="F")

    def test_abstract_player_initialization(self):
        """Tests that the abstract player correctly handles initialization parameters."""
        player = CompletePlayer(name="Test", marker="X")
        self.assertEqual(player.name, "Test")
        self.assertEqual(player.marker, "X")
