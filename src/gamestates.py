
from enum import Enum, auto


class GameStates(Enum):
    SPLASH = auto()
    MENU_SCREEN = auto()
    READY_TO_LAUNCH = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    CREDITS = auto()
