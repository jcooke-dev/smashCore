"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the GameState class.
"""

from pygame import Vector2
from gamestate import GameState
from motionmodels import MotionModels
from constants import WIDTH, PAD_WIDTH, WORLD_GRAVITY_ACC
from constants import PADDLE_IMPULSE, BALL_SPEED_STEP


def test_gamestate_init():
    gs = GameState()
    assert gs.running is True
    assert gs.cur_state == GameState.GameStateName.SPLASH
    assert gs.fps_avg == 0.0
    assert gs.loop_time_avg == 0
    assert gs.show_dev_overlay is False
    assert gs.auto_play is False
    assert gs.motion_model == MotionModels.VECTOR_1
    assert gs.tick_time == 0
    assert gs.cur_ball_x == (WIDTH / 2) - (PAD_WIDTH / 2)
    assert gs.gravity_acc_length == WORLD_GRAVITY_ACC
    assert gs.v_gravity_unit == Vector2(0.0, 1.0)
    assert gs.v_gravity_acc == gs.v_gravity_unit * gs.gravity_acc_length
    assert gs.paddle_impulse_vel_length == PADDLE_IMPULSE
    assert gs.ball_speed_step == BALL_SPEED_STEP
