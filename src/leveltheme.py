"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: LevelTheme is only an Enum class defining the available level themes.
"""

from enum import Enum, auto

class LevelTheme(Enum):
    """ All available Level themes """
    NO_THEME = auto()
    CLASSIC = auto()
    MODERN = auto()