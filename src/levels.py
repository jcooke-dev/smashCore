"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Levels is a utility class to allow for organized level-building.  Additional levels can be added to the enum
                        and then built-up in buildLevel.
"""

import pygame
import constants
import assets
from random import randrange as rnd
from random import choice, sample
from enum import Enum, auto
from src.brick import Brick
from worldobject import WorldObject


class Levels:
    """ This supplies the level building logic """

    class LevelName(Enum):
        """ Enum with all possible LevelNames for later construction in build_level() """
        SMASHCORE_1: Enum = auto()
        SMASHCORE_SOLID_ROWS_1: Enum = auto()
        SMASHCORE_IMG_CHAMFER_1: Enum = auto()
        SMASHCORE_SOLID_ROWS_IMG_CHAMFER_1: Enum = auto()

    def __init__(self):
        pass

    @staticmethod
    def build_level(gw_list: list[WorldObject], level_name: LevelName) -> None:
        """
        Build the specified level.

        :param gw_list: list[WorldObject]
        :param level_name: LevelName
        :return:
        """

        match level_name:
            case Levels.LevelName.SMASHCORE_1:
                for i in range(10):
                    for j in range(4):
                        random_score = rnd(1, 11)
                        gw_list.append(Brick(pygame.Rect(10 + 120 * i, 60 + 70 * j, 100, 50),
                                             (rnd(30, 256), rnd(30, 256), rnd(30, 256)),
                                             random_score))

            case Levels.LevelName.SMASHCORE_SOLID_ROWS_1:
                colors = [constants.RED, constants.ORANGE, constants.GREEN, constants.YELLOW, constants.LIGHTBLUE]
                values = [10, 7, 5, 3, 1]

                num_columns = int((constants.WIDTH - 10) / 105)
                horizontal = (constants.WIDTH - 10) / num_columns
                vertical = 55

                for i in range(num_columns):
                    for j in range(5):
                        gw_list.append(Brick(pygame.Rect(10 + horizontal * i, 60 + vertical * j, 100, 50),
                                                      colors[j], values[j]))

            case Levels.LevelName.SMASHCORE_IMG_CHAMFER_1:
                for i in range(10):
                    for j in range(4):
                        random_brick = choice(assets.BRICK_COLORS)
                        scaled_brick = pygame.transform.scale(random_brick, (110, 40))
                        random_score = rnd(1, 11)
                        gw_list.append(Brick(pygame.Rect(35 + 113 * i, 120 + 40 * j, 110, 40),
                                                      (rnd(30, 256), rnd(30, 256), rnd(30, 256)),
                                                      random_score, image=scaled_brick))

            case Levels.LevelName.SMASHCORE_SOLID_ROWS_IMG_CHAMFER_1:
                colors = [constants.RED, constants.ORANGE, constants.GREEN, constants.YELLOW, constants.LIGHTBLUE]

                # generates list of 5 unique brick colors every time the level loads
                random_row_colors = sample(assets.BRICK_COLORS, 5)

                row_colors =[]
                for brick_color in random_row_colors:
                    row_brick_color = pygame.transform.scale(brick_color, (100, 50))
                    row_colors.append(row_brick_color)

                values = [10, 7, 5, 3, 1]

                num_columns = int((constants.WIDTH - 10) / 105)
                horizontal = (constants.WIDTH - 10) / num_columns
                vertical = 55

                for i in range(num_columns):
                    for j in range(5):
                        gw_list.append(Brick(pygame.Rect(10 + horizontal * i, 60 + vertical * j, 100, 50),
                                                      colors[j], values[j], image=row_colors[j]))

            case _:
                pass
