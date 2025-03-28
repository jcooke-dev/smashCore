"""
    Levels is a utility class to allow for organized level-building.  Additional levels can be added to the enum
    and then built-up in buildLevel.
"""

import pygame
from random import randrange as rnd
from enum import Enum, auto

from src.brick import Brick


class Levels:

    # enum to hold all level names
    class LevelName(Enum):
        SMASHCORE_1 = auto() # first SMASHCORE level



    def __init__(self):
        pass

    # this adds the specified level to the passed GameWorld
    @staticmethod
    def build_level(gw, level_name):

        match level_name:
            case Levels.LevelName.SMASHCORE_1:
                for i in range(10):
                    for j in range(4):
                        gw.world_objects.append(Brick(pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50),
                                          (rnd(30, 256), rnd(30, 256), rnd(30, 256))))
            case _:
                pass

