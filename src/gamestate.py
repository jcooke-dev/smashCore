"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Consolidate the game state flags and parameters into a single class.
"""

from pygame import Vector2

import constants

from gamestates import GameStates
from motionmodels import MotionModels

class GameState:

    def __init__(self):

        self.running = True
        self.cur_state = GameStates.SPLASH
        self.fps_avg = 0.0
        self.loop_time_avg = 0
        self.show_dev_overlay = False
        self.auto_play = False
        self.motion_model = MotionModels.VECTOR_1
        self.tick_time = 0
        self.cur_ball_x = (constants.WIDTH / 2) - (constants.PAD_WIDTH / 2) # used for the auto-play mode that matches paddle pos to the ball pos
        self.gravity_acc_length = constants.WORLD_GRAVITY_ACC
        self.v_gravity_unit = Vector2(0.0, 1.0)
        self.v_gravity_acc = self.v_gravity_unit * self.gravity_acc_length
        self.paddle_impulse_vel_length = constants.PADDLE_IMPULSE
        self.ball_speed_step = constants.BALL_SPEED_STEP