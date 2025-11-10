from enum import Enum
from typing import Iterator, Tuple, List, Optional, Type
from src import players as p


class PlayerType(Enum):
    """Enum representing different player types in the game, including human and various AI difficulty levels.

    Each member is a tuple of:
    - key (str): Difficulty identifier.
    - description (str): Human-readable label.
    - player_class (type): Corresponding player class implementation."""

    HUMAN = ("0", "", p.HumanPlayer)
    EASY = ("1", "Easy (Random)", p.RandomAIPlayer)
    MEDIUM = ("2", "Medium (Checks for wins)", p.WinningMoveAIPlayer)
    HARD = ("3", "Hard (Checks for wins and blocks)", p.StrategicAIPlayer)
    IMPOSSIBLE = ("4", "Impossible (Perfect play)", p.MinimaxAIPlayer)

    @classmethod
    def get_ai_options(cls) -> Iterator[Tuple[str, str]]:
        """Yields all AI player options excluding the human player.

        Returns:
            Iterator[Tuple[str, str]]: Pairs of difficulty key and description for AI
            players."""
        for member in cls:
            if member != cls.HUMAN:
                key, description, _ = member.value
                yield key, description

    @classmethod
    def get_keys(cls) -> List[int]:
        """Returns all difficulty keys as integers, including the human player.

        Returns:
            List[int]: List of integer keys for all player types."""
        keys = []
        for member in cls:
            key, _, _ = member.value
            keys.append(int(key))
        return keys

    @classmethod
    def get_min_difficulty_key(cls) -> int:
        """Returns the lowest difficulty key among AI players.

        Returns:
            int: Minimum AI difficulty key (excluding human)."""
        return min(cls.get_keys()[1:])

    @classmethod
    def get_max_difficulty_key(cls) -> int:
        """Returns the highest difficulty key among AI players.

        Returns:
            int: Maximum AI difficulty key (excluding human)."""
        return max(cls.get_keys()[1:])

    @classmethod
    def get_player_class_by_key(cls, key: str) -> Optional[p.AbstractPlayer]:
        """Returns the player class associated with a given difficulty key.

        Args:
            key (str): Difficulty identifier.

        Returns:
            type: Corresponding player class, or None if not found."""
        for member in cls:
            if member.value[0] == key:
                return member.value[2]
        return None
