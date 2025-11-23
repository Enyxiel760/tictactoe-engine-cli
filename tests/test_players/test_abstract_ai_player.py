"""Unit tests for the AbstractAIPlayer base class.

This module verifies the behavior of the intermediate AI player class, specifically focusing on
dependency injection, abstract method enforcement, and the delegation of move calculation.
"""

import unittest

from src.players import AbstractAIPlayer


class MockEngine:
    """Provides a dummy GameEngine instance for testing dependency injection."""

    def get_board_state(self):
        """Always return a specific state for predictable testing."""
        return [["X", None, None], [None, None, None], [None, None, None]]


class IncompleteAIPlayer(AbstractAIPlayer):
    """Fails to implement _calculate_move to test contract enforcement."""

    pass


class CompleteAIPlayer(AbstractAIPlayer):
    """Minimally complete subclass used to test delegation."""

    # Stores the board state it actually received for inspection by tests
    received_board_state = None

    def _calculate_move(self, board_state):
        """Store the received state here for later test verification."""
        CompleteAIPlayer.received_board_state = board_state
        return (1, 1)


class TestAbstractAIPlayer(unittest.TestCase):
    """Test suite for AbstractAIPlayer logic."""

    def setUp(self):
        """Set up the mock dependencies and the AbstractAIPlayer instance once per test."""
        self.ai_player = CompleteAIPlayer(name="TestAI", marker="O")
        self.mock_engine = MockEngine()
        # Reset static variable before each test
        CompleteAIPlayer.received_board_state = None

    def test_abstract_enforces_calculate_move(self):
        """Tests that subclasses must implement the _calculate_move method.

        Note: While testing language features is generally redundant, this confirms the abstract
        inheritance structure is correctly defined.
        """
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            # Abstract classes cannot be instantiated if abstract methods are missing
            IncompleteAIPlayer(name="Fail", marker="F")

    def test_base_initialization_is_inherited(self):
        """Tests that AbstractAiPlayer corrently inherits and sets base attributes."""
        self.assertEqual(self.ai_player.name, "TestAI")
        self.assertEqual(self.ai_player.marker, "O")

    def test_set_engine_stores_dependency(self):
        """Tests the set_engine method corrrectly injects and stores the GameEngine reference."""
        self.ai_player.set_engine(self.mock_engine)
        self.assertIs(self.ai_player._game, self.mock_engine)

    def test_delegation_passes_correct_board_state(self):
        """Tests the data flow.

        Verifies that get_move calls the engine and passes the board state to the
        _calculate_move method.
        """
        self.ai_player.set_engine(self.mock_engine)
        self.ai_player.get_move()

        expected_board = self.mock_engine.get_board_state()
        self.assertEqual(CompleteAIPlayer.received_board_state, expected_board)

    def test_get_move_returns_calculated_result(self):
        """Tests that get_move returns the result of _calculate_move method."""
        self.ai_player.set_engine(self.mock_engine)
        move = self.ai_player.get_move()
        self.assertEqual(move, (1, 1))
