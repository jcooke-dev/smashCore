"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Consolidate the player state data into a single class.
"""

import constants
from leveltheme import LevelTheme


class PlayerState:
    """ This maintains the current PlayerState """

    def __init__(self) -> None:

        self.lives: int = constants.START_LIVES
        self.score: int = constants.START_SCORE
        self.theme: LevelTheme = LevelTheme.MODERN
        self.level: int = 1
