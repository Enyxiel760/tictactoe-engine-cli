from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """Base class for all players (human or AI)"""

    def __init__(self, name: str, marker: str):
        self.name = name
        self.marker = marker
        # Future: Add self.stats, self.unique_id, etc. here

    @abstractmethod
    def get_move(self) -> Tuple[int, int]:
        """Abstract method. Must be implemented by subclasses to aquire the next move.
        Returns the 0-indexed (row, col) coordinates for the move."""

        pass
