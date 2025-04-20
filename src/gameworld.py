"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This holds all the WorldObjects present in the game world.  These can be different types: static objects, moving
                        objects, objects that can participate in collisions, and objects that react to collisions.
"""

import constants
import assets
from ball import Ball
from paddle import Paddle
from levels import Levels
from worldobject import WorldObject


class GameWorld:
    """ The GameWorld holds all objects in the game for update() and draw() processing """

    def __init__(self, level_name: Levels.LevelName = None) -> None:
        """
        Allows for setting the initial level build, but with a default if None passed

        :param level_name: a LevelName value, but None works as a default
        """
        # setup empty list to hold all world objects
        self.world_objects: list[WorldObject] = []

        # place the ball into the world
        self.world_objects.append(Ball(((constants.WIDTH/2) - (constants.PAD_WIDTH/2)),
            (constants.HEIGHT - constants.PAD_HEIGHT - constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3)),
            image=assets.BALL_IMG))

        # place the paddle into the world
        self.world_objects.append(Paddle(constants.RED, constants.PAD_WIDTH, constants.PAD_HEIGHT, image=assets.PADDLE_IMG))

        # set up the initial bricks level
        Levels.build_level(self.world_objects, Levels.LevelName.SMASHCORE_1 if level_name is None else level_name)
