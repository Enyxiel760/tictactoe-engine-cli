import unittest
from src.views.abstract_view import AbstractView


class MockEngine:
    """Mock engine used to test AbstractView's set_engine method."""

    pass


class MockIncompleteView(AbstractView):
    """Subclass that deliberately fails to enforce the abstract contract."""

    pass


class MockCompleteView(AbstractView):
    """Minimal concrete implementation to test instantiation"""

    def get_game_config(self):
        pass

    def display_game_state(self):
        pass

    def display_message(self, message: str):
        pass

    def display_error(self, message: str):
        pass

    def display_winner(self, winner_name: str):
        pass


class TestAbstractView(unittest.TestCase):

    def setUp(self):
        self.mock_engine = MockEngine()

    def test_abstract_methods_are_enforced(self):
        """Tests that attempting to instantiate an incomplete subclass raises TypeError.

        Note:
        Whilst this is generally redundant (testing the language, not the logic).
        This test is retained here as an academic exercise."""

        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            MockIncompleteView()

    def test_set_engine_is_inherited_and_works(self):
        """Tests that the concrete class correctly inherits and executes the set_engine
        method provided by the AbstractView"""
        view = MockCompleteView()
        try:
            view.set_engine(self.mock_engine)
        except Exception as e:
            self.fail(f"set_engine raised an unexpected exception: {e}")
        self.assertIs(view._game, self.mock_engine)
