"""
    This holds all the WorldObjects present in the game world.  These can be different types: static objects, moving
    objects, objects that can participate in collisions, and objects that react to collisions.
"""

import pygame

import constants
from src.ball import Ball
from src.paddle import Paddle
from src.levels import Levels


class GameWorld:

    def __init__(self, level_name = None):

        # setup empty list to hold all world objects
        self.world_objects = []

        # place the ball into the world
        self.world_objects.append(Ball())

        # place the paddle into the world
        self.world_objects.append(Paddle(pygame.Color('red'), constants.PAD_WIDTH, constants.PAD_HEIGHT))

        # setup the initial bricks level
        Levels.build_level(self, Levels.LevelName.SMASHCORE_1 if level_name is None else level_name)


