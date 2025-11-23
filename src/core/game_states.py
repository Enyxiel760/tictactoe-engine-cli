"""Application state definitions for Tic Tac Toe.

Provides enums for full-screen frames and overlays, each linked to a view creation method.
"""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class GameStateMeta:
    """Metadata for a game state.

    Associates a human-readable label with the name of the view creation function used to render
    the state.

    Attributes:
        label: The ID name of the state.
        creation_func: The name of the method in the view class that creates this frame/overlay.
    """

    label: str
    creation_func: str


class GameState:
    """Container for all application states.

    Holds nested enums for frames and overlays, each mapping to a view creation function.
    """

    class Frame(Enum):
        """Full-screen application states.

        Each state is associated with a label and a view creation method.
        """

        WELCOME_SCREEN = GameStateMeta("Welcome", "_create_welcome_frame")
        PLAYER_CREATION = GameStateMeta("Player_Creation", "_create_newplayer_frame")
        MAIN_MENU = GameStateMeta("Main_Menu", "_create_menu_frame")
        GAMEPLAY = GameStateMeta("Game", "_create_gameplay_frame")
        GAME_OVER = GameStateMeta("Game_Over", "_create_game_over_frame")

        @property
        def label(self) -> str:
            """Return the label for this frame state."""
            return self.value.label

        @property
        def creation_func(self) -> str:
            """Return the name of the view creation method for this frame."""
            return self.value.creation_func

    class Overlay(Enum):
        """Overlay dialog states.

        Each overlay is associated with a label and a view creation method.
        """

        AI_SELECTION = GameStateMeta("AI_Selection", "_create_ai_select_overlay")
        TWO_PLAYER_SETUP = GameStateMeta("Two_Player_Setup", "_create_two_player_setup_overlay")
        SETTINGS = GameStateMeta("Settings", "_create_settings_overlay")

        @property
        def label(self) -> str:
            """Return the label for this overlay state."""
            return self.value.label

        @property
        def creation_func(self) -> str:
            """Return the name of the view creation method for this overlay."""
            return self.value.creation_func
