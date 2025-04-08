"""
    Levels is a utility class to allow for organized level-building.  Additional levels can be added to the enum
    and then built-up in buildLevel.
"""

import pygame
from random import randrange as rnd
from random import choice
from enum import Enum, auto
from src.brick import Brick
import constants
import assets

class Levels:

    class LevelName(Enum):
        SMASHCORE_1 = auto()
        SMASHCORE_SOLID_ROWS_1 = auto()

    def __init__(self):
        pass

    @staticmethod
    def build_level(gw, level_name):

        match level_name:
            case Levels.LevelName.SMASHCORE_1:
                for i in range(10):
                    for j in range(4):
                        random_brick = choice(assets.BRICK_COLORS)
                        scaled_brick = pygame.transform.scale(random_brick, (110, 40))
                        random_score = rnd(1, 11)
                        gw.world_objects.append(Brick(pygame.Rect(35 + 113 * i, 120 + 40 * j, 110, 40),
                                                      (rnd(30, 256), rnd(30, 256), rnd(30, 256)),
                                                      random_score, image=scaled_brick))

            case Levels.LevelName.SMASHCORE_SOLID_ROWS_1:
                colors = [constants.RED, constants.ORANGE, constants.GREEN, constants.YELLOW, constants.LIGHTBLUE]
                brick_colors = [assets.BRK_RED_IMG, assets.BRK_ORANGE_IMG, assets.BRK_GREEN_IMG,
                              assets.BRK_YELLOW_IMG, assets.BRK_LTBLUE_IMG]
                row_bricks = []
                for brick in brick_colors:
                    row_brick = pygame.transform.scale(brick, (100, 50))
                    row_bricks.append(row_brick)

                values = [10, 7, 5, 3, 1]

                num_columns = int((constants.WIDTH - 10) / 105)
                horizontal = (constants.WIDTH - 10) / num_columns
                vertical = 55

                for i in range(num_columns):
                    for j in range(5):
                        gw.world_objects.append(Brick(pygame.Rect(10 + horizontal * i, 60 + vertical * j, 100, 50),
                                                      colors[j], values[j], image=row_bricks[j]))
            case _:
                pass

