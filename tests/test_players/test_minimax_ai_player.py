"""Unit tests for the MinimaxAIPlayer.

This module verifies the behavior of the MinimaxAIPlayer, specifically ensuring that the AI
correctly evaluates board states to identify winning moves, blocking moves, forks, and forced draws.
"""

import unittest

from src.core import GameEngine
from src.players import MinimaxAIPlayer


class TestMinimaxAIPlayer(unittest.TestCase):
    """Unit tests for the MinimaxAIPlayer._calculate_move method.

    These tests verify that the AI correctly selects moves based on full-board evaluation
    using the minimax algorithm. The AI should prioritize winning moves, block opponent wins,
    and choose optimal paths that lead to victory or draw when no win is possible.
    """

    @classmethod
    def setUpClass(cls):
        """Initializes test fixtures for MinimaxAIPlayer and GameEngine.

        This setup creates two AI players and injects them into a GameEngine instance.
        It also prepares board states to test scenarios including immediate wins, blocks,
        forks, and forced draws.
        """
        cls.player1 = MinimaxAIPlayer(name="Test1", marker="O")
        cls.player2 = MinimaxAIPlayer(name="Test2", marker="X")
        cls.engine = GameEngine(cls.player1, cls.player2)
        cls.player1.set_engine(cls.engine)
        cls.player2.set_engine(cls.engine)

        # Board where O (Player 1) can win immediately at (0, 0)
        cls.immediate_win_board = [
            [None, "X", "X"],
            ["O", None, "O"],
            ["O", "X", None],
        ]

        # Board where X (Opponent) wins at (0, 0), so O must block there
        cls.immediate_block_board = [
            [None, None, "O"],
            ["X", None, None],
            ["X", "O", "X"],
        ]

        # Scenarios for forks (advanced strategy)
        cls.forked_win_board = [
            ["O", None, None],
            [None, "O", None],
            [None, None, "X"],
        ]
        cls.forked_block_board = [
            ["X", None, None],
            [None, "O", None],
            [None, None, "X"],
        ]
        cls.forced_draw_board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def test__calculate_move_identifies_immediate_win(self):
        """Tests that _calculate_move selects a winning move when one is available.

        This test verifies that the AI correctly identifies and selects a move that
        results in an immediate win.
        """
        expected_move = (0, 0)
        actual_move = self.player1._calculate_move(self.immediate_win_board)
        self.assertEqual(expected_move, actual_move)

    def test__calculate_move_identifies_immediate_block(self):
        """Tests that _calculate_move selects a blocking move when the opponent has a win.

        This test ensures the AI evaluates the opponent's threat and chooses a move that
        prevents an immediate loss.
        """
        expected_move = (0, 0)
        actual_move = self.player1._calculate_move(self.immediate_block_board)
        self.assertEqual(expected_move, actual_move)

    def test__calculate_move_identifies_forked_win(self):
        """Tests that _calculate_move selects a move that leads to a forked win opportunity.

        This test checks whether the AI can identify a move that creates multiple
        future winning paths.
        """
        expected_move = (0, 1)
        actual_move = self.player1._calculate_move(self.forked_win_board)
        self.assertEqual(expected_move, actual_move)

    def test__calculate_move_identifies_forked_block(self):
        """Tests that _calculate_move selects a move that blocks the opponent's forked win.

        This test ensures the AI can detect and prevent the opponent from creating
        multiple simultaneous threats.
        """
        expected_move = (0, 1)
        actual_move = self.player1._calculate_move(self.forked_block_board)
        self.assertEqual(expected_move, actual_move)

    def test__calculate_move_forces_draw(self):
        """Tests that _calculate_move selects an optimal move (draw) when no win is possible.

        This test verifies that the AI avoids losing paths and chooses moves that
        result in a draw when optimal play prevents either side from winning.
        """
        expected_move = (0, 0)
        actual_move = self.player1._calculate_move(self.forced_draw_board)
        self.assertEqual(expected_move, actual_move)
