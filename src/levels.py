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

from random import randrange as rnd
from random import choice, sample
from enum import Enum
import pygame
import constants
import assets
from leveltheme import LevelTheme
from brick import Brick
from obstacle import Obstacle
from worldobject import WorldObject


class Levels:
    """ This supplies the level building logic """

    class LevelName(Enum):
        """ Enum with all possible LevelNames for later construction in build_level() """

        # changing this from auto() to explicit numbering, since mapping the level number
        # to this wrapping set of enum LevelNames (that logic in get_level_name_from_num()
        # needs enum values here to work reliably)
        CLASSIC_RANDOM_1: Enum = 1
        CLASSIC_SOLID_ROWS_1: Enum = 2
        MODERN_RANDOM_1: Enum = 3
        MODERN_SOLID_ROWS_1: Enum = 4
        CLASSIC_SOLID_ROWS_SPACERS_1: Enum = 5
        MODERN_MULTIPLIER_1: Enum = 6
        MODERN_UNBREAKABLE_1: Enum = 7
        CLASSIC_MULTIPLIER_1: Enum = 8
        CLASSIC_UNBREAKABLE_1: Enum = 9
        MODERN_SOLID_ROWS_SPACERS_1: Enum = 10
        CLASSIC_MULTIPLIER_2: Enum = 11
        MODERN_MULTIPLIER_2: Enum = 12
        CLASSIC_MIXED_1: Enum = 13
        MODERN_MIXED_1: Enum = 14
        CLASSIC_UNBREAKABLE_2: Enum = 15
        MODERN_UNBREAKABLE_2: Enum = 16
        CLASSIC_MIXED_2: Enum = 17
        MODERN_MIXED_2: Enum = 18



    # this is the CLASSIC theme level sequence
    themed_sequence_classic: list[LevelName] = [LevelName.CLASSIC_RANDOM_1,
                                                LevelName.CLASSIC_SOLID_ROWS_1,
                                                LevelName.CLASSIC_SOLID_ROWS_SPACERS_1,
                                                LevelName.CLASSIC_MULTIPLIER_1,
                                                LevelName.CLASSIC_MULTIPLIER_2,
                                                LevelName.CLASSIC_MIXED_1,
                                                LevelName.CLASSIC_UNBREAKABLE_1,
                                                LevelName.CLASSIC_UNBREAKABLE_2,
                                                LevelName.CLASSIC_MIXED_2]
    # this is the MODERN theme level sequence
    themed_sequence_modern: list[LevelName] = [LevelName.MODERN_RANDOM_1,
                                               LevelName.MODERN_SOLID_ROWS_1,
                                               LevelName.MODERN_SOLID_ROWS_SPACERS_1,
                                               LevelName.MODERN_MULTIPLIER_1,
                                               LevelName.MODERN_MULTIPLIER_2,
                                               LevelName.MODERN_MIXED_1,
                                               LevelName.MODERN_UNBREAKABLE_1,
                                               LevelName.MODERN_UNBREAKABLE_2,
                                               LevelName.MODERN_MIXED_2]

    def __init__(self):
        pass

    @classmethod
    def get_level_name_from_num(cls, level_theme: LevelTheme, level_num: int) -> LevelName:
        """
        Find the proper LevelName from an index/value that must wrap around in this enum.

        :param level_theme: theme determines which list of LevelNames is sequenced
        :param level_num: the current 1-based level number, so can increase beyond the
            number of LevelNames
        :return:
        """

        level_name: Levels.LevelName = Levels.LevelName.CLASSIC_RANDOM_1

        match level_theme:
            case LevelTheme.NO_THEME:
                level_val = ((level_num - 1) % len(Levels.LevelName)) + 1
                level_name = Levels.LevelName(level_val)
            case LevelTheme.CLASSIC:
                level_val = (level_num - 1) % len(cls.themed_sequence_classic)
                level_name = cls.themed_sequence_classic[level_val]
            case LevelTheme.MODERN:
                level_val = (level_num - 1) % len(cls.themed_sequence_modern)
                level_name = cls.themed_sequence_modern[level_val]
            case _:
                pass

        return level_name

    @staticmethod
    def build_level(gw_list: list[WorldObject], level_name: LevelName) -> None:
        """
        Build the specified level.

        :param gw_list: list[WorldObject]
        :param level_name: LevelName
        :return:
        """

        match level_name:
            case Levels.LevelName.CLASSIC_RANDOM_1:
                for i in range(10):
                    for j in range(4):
                        random_score = rnd(1, 11)
                        random_color = choice(constants.BRICK_SOLIDS)
                        gw_list.append(Brick(pygame.Rect(10 + 120 * i, 80 + 70 * j, 100, 50),
                                             random_color, random_score))

            case Levels.LevelName.CLASSIC_SOLID_ROWS_1:
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE]
                Levels.generate_grid_level(gw_list,
                                           row_colors=colors)

            case Levels.LevelName.MODERN_RANDOM_1:
                for i in range(10):
                    for j in range(4):
                        random_color = choice(constants.BRICK_SOLIDS)
                        random_brick = choice(assets.BRICK_COLORS)
                        scaled_brick = pygame.transform.scale(random_brick, (100, 50))
                        random_score = rnd(1, 11)
                        gw_list.append(Brick(pygame.Rect(10 + 120 * i, 80 + 70 * j, 100, 50),
                                             random_color, random_score, image=scaled_brick))

            case Levels.LevelName.MODERN_SOLID_ROWS_1:
                colors = [constants.RED, constants.ORANGE, constants.GREEN, constants.YELLOW, constants.LIGHT_BLUE]
                Levels.generate_grid_level(gw_list,
                                          row_colors=colors,
                                          use_random_imgs=True)

            case Levels.LevelName.CLASSIC_SOLID_ROWS_SPACERS_1:
                skip_positions = [(2, 2), (3, 2), (7, 2), (8, 2),
                                  (2, 3), (3, 3), (7, 3), (8, 3)]
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE, constants.PURPLE]
                Levels.generate_grid_level(gw_list,
                                           rows=len(colors),
                                           row_colors=colors,
                                           skip_positions=skip_positions)

            case Levels.LevelName.MODERN_MULTIPLIER_1:
                colors = [constants.PINK, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE]
                skip_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                                  (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5)]
                multiplier_bricks = [(3, 0), (8, 0), (3, 1), (8, 1)]

                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           use_random_imgs=True,
                                           skip_positions=skip_positions,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.MODERN_UNBREAKABLE_1:
                unbreakable = [(0, 2), (1, 2), (9, 2), (10, 2)]
                Levels.generate_grid_level(gw_list=gw_list, rows=5,
                                           use_random_imgs=True,
                                           unbreakable=unbreakable)

            case Levels.LevelName.CLASSIC_MULTIPLIER_1:
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE]
                skip_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                                  (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5)]
                multiplier_bricks = [(3, 0), (8, 0), (3, 1), (8, 1)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           row_colors=colors,
                                           skip_positions=skip_positions,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.CLASSIC_UNBREAKABLE_1:
                unbreakable = [(0, 2), (1, 2), (9, 2), (10, 2)]
                Levels.generate_grid_level(gw_list=gw_list, rows=5,
                                           unbreakable=unbreakable)

            case Levels.LevelName.MODERN_SOLID_ROWS_SPACERS_1:
                skip_positions = [(2, 2), (3, 2), (7, 2), (8, 2),
                                  (2, 3), (3, 3), (7, 3), (8, 3)]
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE, constants.PURPLE]
                row_img_colors = [assets.BRK_RED_IMG, assets.BRK_ORANGE_IMG, assets.BRK_YELLOW_IMG,
                                  assets.BRK_GREEN_IMG, assets.BRK_BLUE_IMG]
                Levels.generate_grid_level(gw_list,
                                           rows=len(colors),
                                           row_colors=colors, row_img_colors=row_img_colors,
                                           skip_positions=skip_positions)

            case Levels.LevelName.CLASSIC_MULTIPLIER_2:
                colors = [constants.RED, constants.ORANGE, constants.GREEN,
                          constants.GREEN, constants.LIGHT_BLUE]
                multiplier_bricks = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                     (6, 4), (7, 3), (8, 2), (9, 1), (10, 0)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           row_colors=colors,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.MODERN_MULTIPLIER_2:
                colors = [constants.PINK, constants.ORANGE, constants.GREEN,
                          constants.GREEN, constants.LIGHT_BLUE]
                multiplier_bricks = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                     (6, 4), (7, 3), (8, 2), (9, 1), (10, 0)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           use_random_imgs=True,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.CLASSIC_MIXED_1:
                colors = [constants.RED, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE]
                skip_positions = [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                                  (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5)]
                multiplier_bricks = [(4, 0), (5, 0), (6, 0), (4, 1), (4, 2), (5, 2),
                                  (6, 2), (6, 3), (6, 4), (5, 4), (4, 4)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           row_colors=colors,
                                           skip_positions=skip_positions,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.MODERN_MIXED_1:
                colors = [constants.PINK, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE, constants.PURPLE]
                skip_positions = [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                                  (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5)]
                multiplier_bricks = [(4, 0), (5, 0), (6, 0), (4, 1), (4, 2), (5, 2),
                                  (6, 2), (6, 3), (6, 4), (5, 4), (4, 4)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           use_random_imgs=True,
                                           skip_positions=skip_positions,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.CLASSIC_UNBREAKABLE_2:
                unbreakable = [(2, 2), (3, 2), (7, 2), (8, 2),
                                  (2, 3), (3, 3), (7, 3), (8, 3)]
                Levels.generate_grid_level(gw_list=gw_list, rows=5,
                                           unbreakable=unbreakable)

            case Levels.LevelName.MODERN_UNBREAKABLE_2:
                unbreakable = [(2, 2), (3, 2), (7, 2), (8, 2),
                                  (2, 3), (3, 3), (7, 3), (8, 3)]
                Levels.generate_grid_level(gw_list=gw_list, rows=5,
                                           use_random_imgs=True,
                                           unbreakable=unbreakable)

            case Levels.LevelName.CLASSIC_MIXED_2:
                colors = [constants.PURPLE, constants.ORANGE, constants.LIGHT_BLUE,
                          constants.GREEN, constants.RED]
                multiplier_bricks = [(2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (3, 2),
                                  (4, 2), (4, 3), (4, 4), (3, 4), (2, 4),
                                     (6, 0), (7, 0), (8, 0), (6, 1), (6, 2), (6, 3),
                                     (6, 4), (7, 4), (8, 4)]
                unbreakable = [(3, 1), (4, 1), (2, 3), (3, 3),
                               (7, 1), (7, 2), (7, 3), (8, 1), (8, 2), (8, 3)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           row_colors=colors,
                                           unbreakable=unbreakable,
                                           strong_bricks=multiplier_bricks)

            case Levels.LevelName.MODERN_MIXED_2:
                colors = [constants.PINK, constants.ORANGE, constants.YELLOW,
                          constants.GREEN, constants.LIGHT_BLUE,
                          constants.PURPLE]
                multiplier_bricks = [(2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (3, 2),
                                  (4, 2), (4, 3), (4, 4), (3, 4), (2, 4),
                                     (6, 0), (7, 0), (8, 0), (6, 1), (6, 2), (6, 3),
                                     (6, 4), (7, 4), (8, 4)]
                unbreakable = [(3, 1), (4, 1), (2, 3), (3, 3),
                               (7, 1), (7, 2), (7, 3), (8, 1), (8, 2), (8, 3)]
                Levels.generate_grid_level(gw_list=gw_list,
                                           rows=len(colors),
                                           use_random_imgs=True,
                                           unbreakable=unbreakable,
                                           strong_bricks=multiplier_bricks)

            case _:
                pass

    @staticmethod
    def generate_grid_level(gw_list: list[WorldObject],
                            rows: int = 5,
                            row_colors: list[int] = None,
                            use_random_imgs: bool = False,
                            row_img_colors: list[pygame.image] = None,
                            skip_positions: list[tuple[int, int]] = None,
                            strong_bricks: list[tuple[int, int]] = None,
                            unbreakable: list[tuple[int, int]] = None
                            ):
        """
        Generates a grid of bricks with optional skip positions, strong brick positions,
        unbreakable brick (obstacle) positions, and color customization.

        Order of preference for brick types if overlapping coordinates in brick sets passed in:
        1. Skip
        2. Strong
        3. Unbreakable

        :param gw_list: list[WorldObject]
        :param rows: Number of rows for the grid
        :param row_colors: List of colors for each row (if none use random row colors)
        :param use_random_imgs: bool use random row images
        :param row_img_colors: if not using random images, list of images for each row
        :param skip_positions: x,y brick positions to skip
        :param strong_bricks: (x, y) x, y position of bricks to make strong
        :param unbreakable: (x, y) x, y position of bricks that are unbreakable

        """
        brk_width: int = 100
        brk_height: int = 50
        grid_margins: list[int] = [10, 120]
        values = [10, 7, 5, 3, 1]

        # set brick strength and bonus
        strong_brick_strength: int = 5
        strong_brick_bonus: int = 10

        # calculate columns and first brick positions based on board width
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

        if row_colors is None:
            row_colors = sample(constants.BRICK_SOLIDS, rows)
        # assign random images, else use colors
        if use_random_imgs and row_img_colors is None:
            row_img_colors = sample(assets.BRICK_COLORS, rows)

        # generate columns, rows of bricks
        for i in range(columns):
            for j in range(rows):

                # Skip these specific positions
                if skip_positions is not None and (i, j) in skip_positions:
                    continue

                row_color = row_colors[j]
                value = values[j]

                # x,y position for brick
                brk_x, brk_y = (grid_margins[0] + pos_x * i, grid_margins[1] + pos_y * j)

                # create rectangle
                brk_rect = pygame.Rect(brk_x, brk_y, brk_width, brk_height)

                # brick is 10X value and 5X strength
                if strong_bricks is not None and (i, j) in strong_bricks:
                    if row_img_colors is not None:
                        strong_brick = pygame.transform.scale(
                            assets.BRK_GOLD_IMG, (brk_width, brk_height))
                        gw_list.append(Brick(brk_rect,
                                             row_color,
                                             strength=strong_brick_strength,
                                             value=value,
                                             bonus=strong_brick_bonus,
                                             image=strong_brick))
                    else:
                        gw_list.append(Brick(brk_rect, constants.YELLOW,
                                             strength=strong_brick_strength,
                                             value=value,
                                             bonus=strong_brick_bonus))

                # obstacle bricks
                elif unbreakable is not None and (i, j) in unbreakable:
                    if row_img_colors is not None:
                        scaled_image = pygame.transform.scale(assets.BRK_OBSTACLE_IMG, (brk_width, brk_height))
                        gw_list.append(Obstacle(brk_rect, row_color, scaled_image))
                    else:
                        gw_list.append(Obstacle(brk_rect, constants.GRAY, text="X X X"))
                # all other bricks
                else:
                    if row_img_colors is not None:
                        scaled_image = pygame.transform.scale(
                            row_img_colors[j], (brk_width, brk_height))
                        gw_list.append(Brick(brk_rect, row_color,
                                             value=value, image=scaled_image))
                    else:
                        gw_list.append(Brick(brk_rect, row_color, value=value))
