
from enum import Enum, auto


class GameStates(Enum):
    SPLASH = auto()
    READY_TO_LAUNCH = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
