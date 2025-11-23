"""Unit tests for the AbstractView base class.

This module verifies the contract enforcement of the AbstractView class, ensuring that
subclasses must implement required methods and that the dependency injection mechanism works.
"""

import unittest

from src.views import AbstractView


class MockEngine:
    """Mock engine used to test AbstractView's set_engine method."""

    pass


class MockIncompleteView(AbstractView):
    """Subclass that deliberately fails to enforce the abstract contract."""

    pass


class MockCompleteView(AbstractView):
    """Minimal concrete implementation to test instantiation."""

    def get_game_config(self):
        """Stub implementation."""
        pass

    def display_game_state(self):
        """Stub implementation."""
        pass

    def display_message(self, message: str):
        """Stub implementation."""
        pass

    def display_error(self, message: str):
        """Stub implementation."""
        pass

    def display_winner(self, winner_name: str):
        """Stub implementation."""
        pass


class TestAbstractView(unittest.TestCase):
    """Unit tests for the AbstractView interface contract."""

    def setUp(self):
        """Initialize test fixtures."""
        self.mock_engine = MockEngine()

    def test_abstract_methods_are_enforced(self):
        """Tests that attempting to instantiate an incomplete subclass raises TypeError.

        Note:
            While testing language features is generally redundant, this test confirms that
            the abstract inheritance structure is correctly defined.
        """
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            MockIncompleteView()

    def test_set_engine_is_inherited_and_works(self):
        """Tests that the concrete class correctly inherits and executes set_engine."""
        view = MockCompleteView()

        view.set_engine(self.mock_engine)

        self.assertIs(view._game, self.mock_engine)
