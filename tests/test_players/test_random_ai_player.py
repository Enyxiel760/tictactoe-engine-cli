import unittest
from unittest.mock import patch
from src.players.random_ai_player import RandomAIPlayer


class MockEngine:
    """Provides a dummy GameEngine instance for testing RandomAIPlayer"""

    def get_board_state(self):
        # Always return a specific state for predictable testing
        return [[None, None, "X"], ["O", None, "O"], ["O", "X", None]]


@patch("src.players.random_ai_player.choice")
class TestRandomAIPlayer(unittest.TestCase):
    """Tests the RandomAIPlayer._calculate_move method's implementation."""

    @classmethod
    def setUpClass(self):
        """Instantiate RandomAIPlayer for use in tests.
        This also implicitly validates the abstract base class contract:
        if RandomAIPlayer fails to implement any required abstract methods,
        instantiation will raise a TypeError here."""
        self.player = RandomAIPlayer(name="Test", marker="X")
        self.engine = MockEngine()

    def test__calculate_move(self, mock_choice):
        """Unit test for random_ai_player._calculate_move to verify correct move selection logic.

        This test ensures that:
        - All valid (i.e., None) positions on the board are correctly identified.
        - The coordinates of those valid positions are accurately collected into a list.
        - The list of valid moves is passed to the random.choice function as expected.

        By asserting that mock_choice is called with the exact list of valid moves,
        this test guarantees that the move selection mechanism is both accurate and
        constrained to legal board positions."""
        expected_moves = [(0, 0), (0, 1), (1, 1), (2, 2)]
        self.player._calculate_move(self.engine.get_board_state())
        mock_choice.assert_called_with(expected_moves)
