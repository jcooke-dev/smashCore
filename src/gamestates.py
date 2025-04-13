"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is an enum containing every GameState.
"""

from enum import Enum, auto


class GameStates(Enum):
    """ Enum with all possible GameState values """
    SPLASH = auto()
    MENU_SCREEN = auto()
    READY_TO_LAUNCH = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    CREDITS = auto()
    LEADERBOARD = auto()
    GET_HIGH_SCORE = auto()
