from abc import ABC, abstractmethod


class AbstractController(ABC):
    """The blueprint for all game controllers (CLI, GUI, Web, etc.).
    Responsible for the game lifecycle."""

    @abstractmethod
    def run(self) -> None:
        """Starts the main control loop for the game."""
        pass
