from enum import Enum


class GameState(Enum):
    """Represents the various states of the game lifecycle."""

    WELCOME_SCREEN = "Welcome"
    PLAYER_CREATION = "Player_Creation"
    MAIN_MENU = "Main_Menu"
    GAMEPLAY = "Game"
    GAME_OVER = "Game_Over"
