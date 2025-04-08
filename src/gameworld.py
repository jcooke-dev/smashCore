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
from src.ball import Ball
from src.paddle import Paddle
from src.levels import Levels


class GameWorld:
    """ The GameWorld holds all objects in the game for update() and draw() processing """

    def __init__(self, level_name = None):

        # setup empty list to hold all world objects
        self.world_objects = []

        # place the ball into the world
        self.world_objects.append(Ball(((constants.WIDTH/2) - (constants.PAD_WIDTH/2)),
            (constants.HEIGHT - constants.PAD_HEIGHT - constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3)),
            image=assets.BALL_IMG))

        # place the paddle into the world
        self.world_objects.append(Paddle(constants.RED, constants.PAD_WIDTH, constants.PAD_HEIGHT, image=assets.PADDLE_IMG))

        # setup the initial bricks level
        Levels.build_level(self, Levels.LevelName.SMASHCORE_1 if level_name is None else level_name)

