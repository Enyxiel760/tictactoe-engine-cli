"""Unit tests for the AbstractController.

This module verifies the functionality of the AbstractController, specifically focusing on game
setup, dependency injection, and the correct initialization of the game engine and players.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.controllers import AbstractController
from src.core.engine import GameEngine
from src.players import AbstractAIPlayer, HumanPlayer


class TestController(AbstractController):
    """A lightweight test double for AbstractController.

    Used to isolate controller logic during unit tests. This stub replaces the view with a
    MagicMock and disables runtime behavior in `run()`.
    """

    def __init__(self):
        """Initialize the test controller with a mock view."""
        self.view = MagicMock()

    def run(self):
        """Stubbed run method to satisfy AbstractController interface."""
        pass


class TestAbstractController(unittest.TestCase):
    """Unit tests for AbstractController setup logic using mocked dependencies.

    This test suite verifies that the controller correctly initializes the game engine and
    configures players when provided with valid configuration data and mocked player instances.
    """

    def setUp(self):
        """Initializes a test controller and mock player instances for use across test cases."""
        self.controller = TestController()
        self.mock_player_x = MagicMock(spec=HumanPlayer)
        self.mock_player_o = MagicMock(spec=AbstractAIPlayer)

    @patch("src.controllers.abstract_controller.get_player_instances")
    def test_setup_game_succeeds(self, mock_get_players):
        """Verifies that setup_game() succeeds when valid config and player instances are returned.

        This test ensures that the engine is instantiated, dependencies are injected into the view
        and AI players, and the setup method returns True.
        """
        mock_config = {"p1_name": "Test", "p1_marker": "X", "p2_type": "1"}
        self.controller.view.get_game_config.return_value = mock_config

        mock_player_return = (self.mock_player_x, self.mock_player_o)
        mock_get_players.return_value = mock_player_return

        result = self.controller.setup_game()

        self.assertTrue(result)
        self.assertIsInstance(self.controller.engine, GameEngine)
        self.controller.view.set_engine.assert_called_once_with(self.controller.engine)
        self.mock_player_o.set_engine.assert_called_once_with(self.controller.engine)
