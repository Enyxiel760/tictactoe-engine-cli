import unittest
from unittest.mock import patch
from src.core.player_factory import get_player_instances
from src.players import HumanPlayer, AbstractPlayer
from src.core import PlayerType


class MockAIPlayer(AbstractPlayer):
    """A mock class to ensure the factory correctly returns the AI type."""

    def get_move(self):
        return (0, 0)


@patch.object(PlayerType, "get_player_class_by_key", return_value=MockAIPlayer)
class TestPlayerFactory(unittest.TestCase):

    # --- Helper Method to Structure Inputs ---
    def get_setup_data(
        self, p1_name: str, p1_marker: str, p2_name: str, p2_type: str
    ) -> dict:
        """Returns setup data for a game configuration, used by the player factory.

        Args:
            p1_name (str): Name of player 1.
            p1_marker (str): Marker for player 1 ("X" or "O").
            p2_name (str): Name of player 2.
            p2_type (str): Difficulty key for player 2 (e.g., "0" for human, "4" for Minimax AI).

        Returns:
            dict[str, str]: Dictionary formatted for use with get_player_instances()."""
        return {
            "p1_name": p1_name,
            "p1_marker": p1_marker,
            "p2_name": p2_name,
            "p2_type": p2_type,
        }

    def test_factory_creates_p1_x_vs_ai_o(self, mock_get_class):
        """Verifies P1 chooses 'X' and AI is correctly created as 'O'."""
        data = self.get_setup_data("Alice", "X", "Bot", PlayerType.IMPOSSIBLE.key)
        p_x, p_o = get_player_instances(data)

        self.assertIsInstance(p_x, HumanPlayer)
        self.assertIsInstance(p_o, MockAIPlayer)
        self.assertEqual(p_x.marker, "X")
        self.assertEqual(p_o.marker, "O")
        mock_get_class.assert_called_once_with(PlayerType.IMPOSSIBLE.key)

    def test_factory_creates_ai_x_vs_p1_o(self, mock_get_class):
        """Verifies P1 chooses 'O' and players are swapped to return (X, O)."""
        data = self.get_setup_data("Alice", "O", "Bot", PlayerType.IMPOSSIBLE.key)
        p_x, p_o = get_player_instances(data)

        self.assertIsInstance(p_x, MockAIPlayer)
        self.assertIsInstance(p_o, HumanPlayer)
        self.assertEqual(p_x.marker, "X")
        self.assertEqual(p_o.marker, "O")
        mock_get_class.assert_called_once_with(PlayerType.IMPOSSIBLE.key)

    def test_factory_creates_p1_x_vs_p2_o(self, mock_get_class):
        """Verifies two HumanPlayer objects are created in 2-player mode."""
        data = self.get_setup_data("Fred", "X", "Barney", PlayerType.HUMAN.key)
        p_x, p_o = get_player_instances(data)

        self.assertIsInstance(p_x, HumanPlayer)
        self.assertIsInstance(p_o, HumanPlayer)
        self.assertEqual(p_x.name, "Fred")
        self.assertEqual(p_o.name, "Barney")
        self.assertEqual(p_x.marker, "X")
        self.assertEqual(p_o.marker, "O")
        mock_get_class.assert_not_called()
