"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Consolidate the game state flags and parameters into a single class.
"""
from enum import Enum, auto
import pygame
import constants
from motionmodels import MotionModels


class GameState:
    """ This maintains the current GameState """

    class GameStateName(Enum):
        """ Enum with all possible GameState values """
        SPLASH = auto()
        MENU_SCREEN = auto()
        READY_TO_LAUNCH = auto()
        PLAYING = auto()
        PAUSED = auto()
        GAME_OVER = auto()
        CREDITS = auto()
        LEADERBOARD = auto()
        GET_HIGH_SCORE = auto()
        HOW_TO_PLAY = auto()
        SETTINGS = auto()


    def __init__(self) -> None:

        self.running: bool = True
        self.cur_state: GameState.GameStateName = GameState.GameStateName.SPLASH
        self.fps_avg: float = 0.0
        self.loop_time_avg: float = 0
        self.show_dev_overlay: bool = False
        self.auto_play: bool = False
        self.motion_model: MotionModels = MotionModels.VECTOR_1
        self.tick_time: int = 0
        self.cur_ball_x: int = (constants.WIDTH // 2) - (constants.PAD_WIDTH // 2) # used for the auto-play mode that matches paddle pos to the ball pos
        self.gravity_acc_length: float = constants.WORLD_GRAVITY_ACC
        self.v_gravity_unit: pygame.Vector2 = pygame.Vector2(0.0, 1.0)
        self.v_gravity_acc: pygame.Vector2 = self.v_gravity_unit * self.gravity_acc_length
        self.paddle_impulse_vel_length: float = constants.PADDLE_IMPULSE
        self.ball_speed_step: float = constants.BALL_SPEED_STEP
        self.ball_speed_increased_ratio: float = 1.0 # used to adjust the key-control paddle speed according to ball speed
        self.last_mouse_pos_x: int = 0

        self.level_cleared: bool = False

        # shake effect config
        self.shake_screen_brick: bool = False
        self.shake_strength: int = 0

        # these are used to index into the following lists on subsequent calls to utils.get_shaking_offset() to get the shake offset
        self.shake_off_index_x = 0
        self.shake_off_index_y = 0
        # these are the shake offset values to sequence through -- better to hard-code these up front, rather than trying to calculate
        self.shake_offsets_x = [5, 5, 3, -4, -1, -3, -2, -2, 3, 4, 1, 2, 0, -1, -2, -3, -2, 1, 0, 5, 2, 1, 0, -1, -2, -1, 0, 0]
        self.shake_offsets_y = [5, -5, 0, -3, -3, 1, 1, 0, 4, -2, 1, -2, 1, 1, 2, 3, -2, -1, 4, 2, 2, -1, 2, 3, 2, -1, 0, 0]

        self.paddle_pos_x: int = 0  # used at READY_TO_LAUNCH to keep ball on paddle

        self.paddle_under_key_control_left: bool = False
        self.paddle_under_key_control_right: bool = False
