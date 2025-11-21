from enum import Enum
from dataclasses import dataclass
from tkinter import Frame, Toplevel


@dataclass(frozen=True)
class GameStateMeta:
    label: str
    creation_func: str


class GameState:
    """Defines all application states and holds the method to create the corresponding View component."""

    class Frame(Enum):
        """Defines full-screen application states and their view creation methods."""

        WELCOME_SCREEN = GameStateMeta("Welcome", "_create_welcome_frame")
        PLAYER_CREATION = GameStateMeta("Player_Creation", "_create_newplayer_frame")
        MAIN_MENU = GameStateMeta("Main_Menu", "_create_menu_frame")
        GAMEPLAY = GameStateMeta("Game", "_create_gameplay_frame")
        GAME_OVER = GameStateMeta("Game_Over", "_create_game_over_frame")

        @property
        def label(self) -> str:
            return self.value.label

        @property
        def creation_func(self) -> str:
            return self.value.creation_func

    class Modal(Enum):
        """Defines modal dialog states and their view creation methods."""

        AI_SELECTION = GameStateMeta("AI_Selection", "._create_ai_select_modal")
        TWO_PLAYER_SETUP = GameStateMeta(
            "Two_Player_Setup", "._create_two_player_setup_modal"
        )
        SETTINGS = GameStateMeta("Settings", "._create_settings_modal")

        @property
        def label(self) -> str:
            return self.value.label

        @property
        def creation_func(self) -> str:
            return self.value.creation_func
