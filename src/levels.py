"""
    Levels is a utility class to allow for organized level-building.  Additional levels can be added to the enum
    and then built-up in buildLevel.
"""

import pygame
from enum import Enum, auto

from src.brick import Brick
import constants # import the constants file.


class Levels:

    class LevelName(Enum):
        SMASHCORE_1 = auto()

    def __init__(self):
        pass

    @staticmethod
    def build_level(gw, level_name):

        match level_name:
            case Levels.LevelName.SMASHCORE_1:
                colors = [constants.RED, constants.ORANGE, constants.GREEN, constants.YELLOW, constants.LIGHTBLUE] # define the colors
                for i in range(10):
                    for j in range(5): # change to 5 rows to use all the colors.
                        gw.world_objects.append(Brick(pygame.Rect(10 + 120 * i, 60 + 70 * j, 100, 50),
                                          colors[j]))
            case _:
                pass
