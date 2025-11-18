import unittest
from unittest.mock import patch
from src.players.winning_move_ai_player import WinningMoveAIPlayer
from src.core.engine import GameEngine


class TestWinningMoveAIPlayer(unittest.TestCase):
    """Unit tests for the WinningMoveAIPlayer._calculate_move method.
    These tests verify that the AI correctly prioritizes winning moves when available,
    and falls back to random selection among valid positions when no immediate win is possible.
    """

    @classmethod
    def setUpClass(cls):
        """Initializes test fixtures for WinningMoveAIPlayer and GameEngine.

        This setup creates two AI players and injects them into a GameEngine instance. It
        also prepares board states for testing both winning and non-winning scenarios. Instantiating
        WinningMoveAIPlayer implicitly validates its compliance with the AbstractAIPlayer interface,
        raising a TypeError if any required methods are missing."""
        cls.player1 = WinningMoveAIPlayer(name="Test1", marker="O")
        cls.player2 = WinningMoveAIPlayer(name="Test2", marker="X")
        cls.engine = GameEngine(cls.player1, cls.player2)
        cls.player1.set_engine(cls.engine)
        cls.player2.set_engine(cls.engine)
        cls.winning_board = [[None, None, "X"], ["O", None, "O"], ["O", "X", None]]
        cls.non_winning_board = [
            [None, None, "X"],
            [None, None, None],
            ["O", "X", None],
        ]

    def test__calculate_move_has_winner(self):
        """Tests that _calculate_move selects a winning move when one is available.

        This test verifies that the AI correctly identifies a move that would result in
        an immediate win and selects it over any random alternatives."""
        expected_move = (0, 0)
        actual_move = self.player1._calculate_move(self.winning_board)
        self.assertEqual(expected_move, actual_move)

    @patch("src.players.winning_move_ai_player.choice")
    def test__calculate_move_has_no_winner(self, mock_choice):
        """Tests that _calculate_move falls back to random selection when no winning move exists.

        This test confirms that:
        - All valid (None) positions are identified.
        - The AI passes the correct list of valid moves to random.choice.
        - The fallback mechanism is triggered only when no winning move is found."""
        expected_moves = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 2)]
        self.player1._calculate_move(self.non_winning_board)
        mock_choice.assert_called_with(expected_moves)
