"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Consolidate the game state flags and parameters into a single class.
"""
import pygame
import constants

from enum import Enum, auto

from motionmodels import MotionModels

class GameState:
    """ This maintains the current GameState """

    class GameStateName(Enum):
        """ Enum with all possible GameState values """
        SPLASH: Enum = auto()
        MENU_SCREEN: Enum = auto()
        READY_TO_LAUNCH: Enum = auto()
        PLAYING: Enum = auto()
        PAUSED: Enum = auto()
        GAME_OVER: Enum = auto()
        CREDITS: Enum = auto()
        LEADERBOARD: Enum = auto()
        GET_HIGH_SCORE: Enum = auto()
        HOW_TO_PLAY: Enum = auto()
        SETTINGS: Enum = auto()


    def __init__(self) -> None:

        self.running: bool = True
        self.cur_state: GameState.GameStateName = GameState.GameStateName.SPLASH
        self.fps_avg: float = 0.0
        self.loop_time_avg: float = 0
        self.show_dev_overlay: bool = False
        self.auto_play: bool = False
        self.motion_model: MotionModels = MotionModels.VECTOR_1
        self.tick_time: int = 0
        self.cur_ball_x: int = (constants.WIDTH / 2) - (constants.PAD_WIDTH / 2) # used for the auto-play mode that matches paddle pos to the ball pos
        self.gravity_acc_length: float = constants.WORLD_GRAVITY_ACC
        self.v_gravity_unit: pygame.Vector2 = pygame.Vector2(0.0, 1.0)
        self.v_gravity_acc: pygame.Vector2 = self.v_gravity_unit * self.gravity_acc_length
        self.paddle_impulse_vel_length: float = constants.PADDLE_IMPULSE
        self.ball_speed_step: float = constants.BALL_SPEED_STEP
        self.ball_speed_increased_ratio: float = 1.0 # used to adjust the key-control paddle speed according to ball speed
        self.last_mouse_pos_x: int = 0
        self.paddle_under_mouse_control: bool = False
        self.paddle_under_key_control_left: bool = False
        self.paddle_under_key_control_right: bool = False
        self.paddle_pos_x: int = 0 # used at READY_TO_LAUNCH to keep ball on paddle
        self.bg_sounds: bool = True
        self.music_volume = constants.MUSIC_VOLUME_INITIAL
