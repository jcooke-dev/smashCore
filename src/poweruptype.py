"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: PowerUpType is only an Enum class defining the available power-ups.
"""

from enum import Enum, auto

class PowerUpType(Enum):
    """ All available Power-Up Types """
    NO_TYPE = auto()
    EXTRA_LIFE = auto()
    PTS_100 = auto()
    PTS_500 = auto()
    PTS_1000 = auto()