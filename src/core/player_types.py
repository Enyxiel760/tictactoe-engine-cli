"""Player type definitions for Tic Tac Toe.

Provides metadata and an enumeration of available player types, including human and AI opponents at
varying difficulty levels.
"""

from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum

from src import players as p


@dataclass(frozen=True)
class PlayerMeta:
    """Metadata describing a player type.

    Attributes:
        key: Difficulty identifier used in configuration.
        description: Human-readable label for the player type.
        player_type: The player class implementing this type.
    """

    key: str
    description: str
    player_type: type[p.AbstractPlayer]


class PlayerType(Enum):
    """Enumeration of player types.

    Includes human players and AI opponents with varying difficulty levels. Each member stores a
    PlayerMeta object containing a key, description, and the corresponding player class.
    """

    HUMAN = PlayerMeta("0", "", p.HumanPlayer)
    EASY = PlayerMeta("1", "Easy (Random)", p.RandomAIPlayer)
    MEDIUM = PlayerMeta("2", "Medium (Checks for wins)", p.WinningMoveAIPlayer)
    HARD = PlayerMeta("3", "Hard (Checks for wins and blocks)", p.StrategicAIPlayer)
    IMPOSSIBLE = PlayerMeta("4", "Impossible (Perfect play)", p.MinimaxAIPlayer)

    @property
    def key(self):
        """Return the difficulty key for this player type."""
        return self.value.key

    @property
    def description(self):
        """Return the human-readable description for this player type."""
        return self.value.description

    @property
    def player_type(self):
        """Return the player class associated with this player type."""
        return self.value.player_type

    @classmethod
    def get_ai_options(cls) -> Iterator[tuple[str, str]]:
        """Yield all AI player options.

        Excludes the human player and returns pairs of difficulty key and description for each AI
        type.

        Returns:
            Iterator[tuple[str, str]]: Key-description pairs for AI players.
        """
        for member in cls:
            if member != cls.HUMAN:
                yield member.key, member.description

    @classmethod
    def get_keys(cls) -> list[int]:
        """Return all difficulty keys as integers.

        Includes the human player.

        Returns:
            list[int]: Integer keys for all player types.
        """
        return [int(member.key) for member in cls]

    @classmethod
    def get_min_difficulty_key(cls) -> int:
        """Return the lowest AI difficulty key.

        Excludes the human player.

        Returns:
            int: Minimum AI difficulty key.
        """
        return min(cls.get_keys()[1:])

    @classmethod
    def get_max_difficulty_key(cls) -> int:
        """Return the highest AI difficulty key.

        Excludes the human player.

        Returns:
            int: Maximum AI difficulty key.
        """
        return max(cls.get_keys()[1:])

    @classmethod
    def get_player_class_by_key(cls, key: str) -> type[p.AbstractPlayer] | None:
        """Return the player class for a given difficulty key.

        Args:
            key: Difficulty identifier.

        Returns:
            type[AbstractPlayer] | None: Corresponding player class, or None if not found.
        """
        for member in cls:
            if member.key == key:
                return member.player_type
        return None
