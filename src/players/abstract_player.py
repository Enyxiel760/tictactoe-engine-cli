"""Abstract player definition for Tic Tac Toe.

Defines the base contract for all player entities, enforcing a common interface for move
acquisition and identity management.
"""

from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """Base class for all players (human or AI).

    Attributes:
        name: The display name of the player.
        marker: The game marker assigned to the player (e.g., "X" or "O").
    """

    def __init__(self, name: str, marker: str):
        """Initialize a new player.

        Args:
            name: The display name of the player.
            marker: The game marker assigned to the player.
        """
        self.name = name
        self.marker = marker
        # Future: Add self.stats, self.unique_id, etc. here

    @abstractmethod
    def get_move(self) -> tuple[int, int]:
        """Determine the player's next move.

        Abstract method that must be implemented by subclasses to acquire the next move.

        Returns:
            tuple[int, int]: The 0-indexed (row, col) coordinates for the move.
        """
        pass
