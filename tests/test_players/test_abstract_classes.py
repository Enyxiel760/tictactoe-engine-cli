import unittest
from src.players import AbstractPlayer


class IncompletePlayer(AbstractPlayer):
    """Fails to implement get_move to test abstract enforcement"""


class CompletePlayer(AbstractPlayer):
    """Minimally complete subclass to verify."""

    def get_move(self):
        return (0, 0)


class TestAbstractPlayerContract(unittest.TestCase):

    def test_abstract_player_enforce_get_move(self):
        """Tests that attempting to instantiate an incomplete subclass raises TypeError."""
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            IncompletePlayer(name="Fail", marker="F")

    def test_abstract_player_initialization(self):
        """Tests that the abstract player correctly handles initialization parameters."""
        player = CompletePlayer(name="Test", marker="X")
        self.assertEqual(player.name, "Test")
        self.assertEqual(player.marker, "X")
