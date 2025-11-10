import unittest
from src.core import PlayerType
from src.players import AbstractAIPlayer


class TestPlayerTypeEnum(unittest.TestCase):

    def setUp(self):
        # Get all keys as integers for comprehensive checking
        self.all_int_keys = PlayerType.get_keys()
        self.ai_options = list(PlayerType.get_ai_options())
        # Determine the Human key dynamically
        self.human_key_int = int(PlayerType.HUMAN.key)

    @property
    def ai_keys(self):
        """Returns all integer keys excluding the human player."""
        return [key for key in self.all_int_keys if key != self.human_key_int]

    def test_human_key_is_included(self):
        """Ensures the HUMAN key is present in the full key list."""
        self.assertIn(self.human_key_int, self.all_int_keys)

    def test_ai_options_exclude_human(self):
        """Ensures AI options exclude the HUMAN player and match expected count."""
        # Note: Breaks if a key is added but proves filtering works
        self.assertEqual(len(self.ai_options), len(self.all_int_keys) - 1)

    def test_all_ai_options_map_to_ai_classes(self):
        """Ensures every AI option key maps to a valid subclass of AbstractAIPlayer.

        This test guards against enum misconfiguration by verifying that all keys yielded
        by `get_ai_options()` resolve to classes that inherit from AbstractAIPlayer."""
        for key, _ in self.ai_options:
            cls = PlayerType.get_player_class_by_key(key)
            self.assertTrue(issubclass(cls, AbstractAIPlayer))

    def test_min_difficulty_matches_lowest_ai_key(self):
        """Confirms that get_min_difficulty_key returns the lowest AI difficulty key."""
        self.assertEqual(PlayerType.get_min_difficulty_key(), min(self.ai_keys))

    def test_max_difficulty_matches_highest_ai_key(self):
        """Confirms that get_max_difficulty_key returns the highest AI difficulty key."""
        self.assertEqual(PlayerType.get_max_difficulty_key(), max(self.ai_keys))

    def test_get_player_class_by_key(self):
        """Validates that get_player_class_by_key returns the correct AI player class."""
        max_ai_key_str = str(PlayerType.get_max_difficulty_key())
        player_class = PlayerType.get_player_class_by_key(max_ai_key_str)
        self.assertTrue(issubclass(player_class, AbstractAIPlayer))

        # Note: This assert should be updated if the top key changes.
        self.assertEqual(player_class.__name__, "MinimaxAIPlayer")
