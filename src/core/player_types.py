from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Tuple, List, Optional
from src import players as p


@dataclass(frozen=True)
class PlayerMeta:
    key: str
    description: str
    player_type: p.AbstractPlayer


class PlayerType(Enum):
    """Enum representing different player types in the game, including human and various AI difficulty levels.

    Each member is a tuple of:
    - key (str): Difficulty identifier.
    - description (str): Human-readable label.
    - player_type (AbstractPlayer): Corresponding player class implementation."""

    HUMAN = PlayerMeta("0", "", p.HumanPlayer)
    EASY = PlayerMeta("1", "Easy (Random)", p.RandomAIPlayer)
    MEDIUM = PlayerMeta("2", "Medium (Checks for wins)", p.WinningMoveAIPlayer)
    HARD = PlayerMeta("3", "Hard (Checks for wins and blocks)", p.StrategicAIPlayer)
    IMPOSSIBLE = PlayerMeta("4", "Impossible (Perfect play)", p.MinimaxAIPlayer)

    @property
    def key(self):
        return self.value.key

    @property
    def description(self):
        return self.value.description

    @property
    def player_type(self):
        return self.value.player_type

    @classmethod
    def get_ai_options(cls) -> Iterator[Tuple[str, str]]:
        """Yields all AI player options excluding the human player.

        Returns:
            Iterator[Tuple[str, str]]: Pairs of difficulty key and description for AI
            players."""
        for member in cls:
            if member != cls.HUMAN:
                yield member.key, member.description

    @classmethod
    def get_keys(cls) -> List[int]:
        """Returns all difficulty keys as integers, including the human player.

        Returns:
            List[int]: List of integer keys for all player types."""
        return [int(member.key) for member in cls]

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
            if member.key == key:
                return member.player_type
        return None
