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
from obstacle import Obstacle
from worldobject import WorldObject


class Levels:
    """ This supplies the level building logic """

    class LevelName(Enum):
        """ Enum with all possible LevelNames for later construction in build_level() """
        SMASHCORE_1: Enum = auto()
        SMASHCORE_SOLID_ROWS_1: Enum = auto()
        SMASHCORE_IMG_CHAMFER_1: Enum = auto()
        SMASHCORE_SOLID_ROWS_IMG_CHAMFER_1: Enum = auto()
        SMASHCORE_SOLID_ROWS_SPACERS: Enum = auto()
        SMASHCORE_MULTIPLIER_1: Enum = auto()
        SMASHCORE_UNBREAKABLE_1: Enum = auto()

    def __init__(self):
        pass

    @staticmethod
    def get_next_level(current: int) -> LevelName:
        current_level = Levels.LevelName(current)
        level_list = list(Levels.LevelName)
        index = level_list.index(current_level)
        if index + 1 < len(level_list):
            return level_list[index + 1]
        else:
            return level_list[0]

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
                Levels.generate_grid_level(gw_list,
                                           row_colors=colors, values=values)

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
                values = [10, 7, 5, 3, 1]

                Levels.generate_grid_level(gw_list,
                                          row_colors=colors, values=values,
                                          use_random_imgs=True)

            case Levels.LevelName.SMASHCORE_SOLID_ROWS_SPACERS:
                skip_positions = [(2, 2), (3, 2), (6, 2), (7, 2),
                                  (2, 3), (3, 3), (6, 3), (7, 3)]
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHTBLUE, constants.PURPLE]
                values = [10, 7, 5, 3, 1]
                Levels.generate_grid_level(gw_list,
                                           rows=len(colors),
                                           row_colors=colors, values=values,
                                           skip_positions=skip_positions)

            case Levels.LevelName.SMASHCORE_MULTIPLIER_1:
                colors = [constants.PINK, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHTBLUE, constants.PURPLE]
                skip_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                                  (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5)]
                multiplier_bricks = [(2, 2), (5, 2)]

                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           use_random_imgs=True,
                                           skip_positions=skip_positions,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.SMASHCORE_UNBREAKABLE_1:
                colors = [constants.PINK, constants.ORANGE, constants.YELLOW,
                          constants.GREEN]
                unbreakable = [(0, 2), (1, 2), (9, 2), (10, 2)]
                Levels.generate_grid_level(gw_list=gw_list, rows=len(colors),
                                           row_colors=colors,
                                           unbreakable=unbreakable)
            case _:
                pass

    @staticmethod
    def generate_grid_level(gw_list: list[WorldObject],
                            rows: int = 5,
                            values: list[int] = None,
                            row_colors: list[int] = None,
                            use_random_imgs: bool = False,
                            row_img_colors: list[pygame.image] = None,
                            skip_positions: list[tuple[int, int]] = None,
                            strong_bricks: list[tuple[int, int]] = None,
                            unbreakable: list[tuple[int, int]] = None
                            ):
        """
        Generates a grid of bricks with optional skip positions and color customization.

        :param gw_list: list[WorldObject]
        :param rows: Number of rows for the grid
        :param values: List of values for each row index (if none use decreasing values based on row)
        :param row_colors: List of colors for each row (if none use random colors)
        :param use_random_imgs: bool use random images
        :param row_img_colors: if not using random images, list of images for each row
        :param skip_positions: x,y brick positions to skip
        :param strong_bricks: (x, y) x, y position of bricks to make strong
        :param unbreakable: (x, y) x, y position of bricks that are unbreakable

        """
        # adjust the distance from the top of the board based on number of rows
        brk_width = 100
        brk_height = 50
        grid_margins: list[int] = [10, 120]
        strong_brick_strength = 5
        strong_brick_bonus = 10

        columns = int((constants.WIDTH - grid_margins[0]) / (brk_width+5))

        pos_x = (constants.WIDTH - grid_margins[0]) / columns
        pos_y = brk_height + 5

        # make sure there are enough items in values and row_colors
        if values is not None:
            rows = min(rows, len(values))
        if row_colors is not None:
            rows = min(rows, len(row_colors))
        if use_random_imgs is False and row_img_colors is not None:
            rows = min(rows, len(row_img_colors))

        if use_random_imgs and row_img_colors is None:  # assign random images, else use colors
            row_img_colors = sample(assets.BRICK_COLORS, rows)
        for i in range(columns):
            for j in range(rows):
                if skip_positions is not None and (i, j) in skip_positions:
                    continue  # Skip these specific positions

                if row_colors is None: # randomize colors if not set
                    row_color = rnd(30, 256), rnd(30, 256), rnd(30, 256)
                else:
                    row_color = row_colors[j]

                if values is None: # no values, value is the row # descending
                    value = rows-j
                else:
                    value = values[j]

                brk_x, brk_y = (grid_margins[0] + pos_x * i,
                               grid_margins[1] + pos_y * j)  # x,y position for brick

                brk_rect = pygame.Rect(brk_x, brk_y,
                                       brk_width, brk_height) # create rectangle

                if strong_bricks is not None and (i, j) in strong_bricks:  # brick is 10X value and 5X strength
                    strong_brick = pygame.transform.scale(
                        assets.BRK_GOLD_IMG, (brk_width, brk_height))
                    gw_list.append(Brick(brk_rect,
                                         row_color,
                                         strength=strong_brick_strength,
                                         value=value,
                                         bonus=strong_brick_bonus,
                                         image=strong_brick))
                elif unbreakable is not None and (i, j) in unbreakable:
                    gw_list.append(Obstacle(brk_rect, constants.GRAY, text="X X X"))
                else:
                    if row_img_colors is not None:
                        scaled_image = pygame.transform.scale(
                            row_img_colors[j], (brk_width, brk_height))
                        gw_list.append(Brick(brk_rect, row_color,
                                             value=value, image=scaled_image))
                    else:
                        gw_list.append(Brick(brk_rect, row_color, value=value))
