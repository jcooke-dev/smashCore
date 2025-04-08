"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is an enum containing every MotionModel.
"""

from enum import Enum, auto


class MotionModels(Enum):
    """ Enum with all possible MotionModel values """

    # initial motion code with simplified calculations and clock.tick(fps) to time the update loop
    SIMPLE_1 = auto()

    # motion calculations using POS/VEL/ACC vectors and the clock.tick() returned delta time, so the motion is unlinked
    # from the frame rate - can set a MAX_FPS_VECTOR to limit the fps a bit (rather than letting it run all out)
    VECTOR_1 = auto()

