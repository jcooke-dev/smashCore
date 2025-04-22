"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Ball class.
"""
from enum import Enum, auto

import pygame
import pytest
from paddle import Paddle
from pygame import Vector2
from ball import Ball
from constants import BALL_RADIUS, BALL_SPEED_SIMPLE, WIDTH, HEIGHT, WHITE
from gamestate import GameState
from motionmodels import MotionModels
from leaderboard import Leaderboard


@pytest.fixture
def ball():
    """
    Create a ball to be used for testing
    :return:
    """
    pygame.init()
    ball = Ball(x=10, y=10)
    yield ball
    pygame.quit()


@pytest.fixture
def paddle():
    """
    Create paddle to be used in testing
    :return:
    """
    a_paddle = Paddle(WHITE, 100, 50)
    a_paddle.rect = pygame.Rect(90, 90, 10, 10)
    return a_paddle


@pytest.fixture
def playerstate():
    """
    Set up a playerstate for tests
    :return:
    """
    class PlayerState:
        def __init__(self):
            self.lives = 3
            self.score = 0
    return PlayerState()


@pytest.fixture
def gamestate():
    """
    Set up gamestate for tests
    :return:
    """
    class GameState:
        class GameStateName(Enum):
            PLAYING: Enum = auto()
        def __init__(self):
            self.cur_state = GameState.GameStateName.PLAYING
            self.motion_model = MotionModels.SIMPLE_1
            self.gravity_acc_length = 0
            self.v_gravity_acc = Vector2(0, 0)
            self.tick_time = 1
            self.cur_ball_x = 0
    return GameState()

@pytest.fixture
def leaderboard():
    """
    Setup leaderboard for tests
    :return:
    """
    class Leaderboard:
        def __init__(self):
            self.l_top_scores = []

        def is_high_score(self, score):
            return False

    return Leaderboard()


def test_initial_state(ball):
    """
    Test initial state of ball on creation
    :param ball:
    :return:
    """
    assert ball.can_react is True
    assert ball.radius == BALL_RADIUS
    assert ball.x == 10 - BALL_RADIUS
    assert ball.y == 10
    assert ball.image is None
    assert ball.dx in [1, -1]
    assert ball.dy == -1
    assert ball.speed == BALL_SPEED_SIMPLE
    assert ball.rect.x == ball.x
    assert ball.rect.y == ball.y
    assert ball.primed_collision_wall_left is True
    assert ball.primed_collision_wall_right is True
    assert ball.primed_collision_wall_top is True


def test_update_wo_position_update_simple(ball, gamestate):
    """
    Test the ball position is updated based on gamestate
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1

    ball.update_wo(gs, None, None)

    assert ball.rect.x == ball.x
    assert ball.rect.y == ball.y


def test_update_wo_wall_collision_left_simple(ball, gamestate):
    """
    Test the ball direction on collision from left
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.cur_state = GameState.GameStateName.PLAYING
    gs.motion_model = MotionModels.SIMPLE_1

    ball.dx = -1 # must ensure moving to the left before collision test (since __init__ has it randomly either -1, 1)

    ball.rect.centerx = 0  # simulate collision with left wall
    ball.update_wo(gs, None, None)

    assert ball.dx == 1  # direction should reverse


def test_update_wo_wall_collision_right_simple(ball, gamestate):
    """
    Test ball direction on collision from right
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.cur_state = GameState.GameStateName.PLAYING
    gs.motion_model = MotionModels.SIMPLE_1

    ball.dx = 1  # must ensure moving to the right before collision test (since __init__ has it randomly either -1, 1)

    ball.rect.centerx = WIDTH  # simulate collision with right wall
    ball.update_wo(gs, None, None)

    assert ball.dx == -1  # direction should reverse


def test_update_wo_wall_collision_top_simple(ball, gamestate):
    """
    Test ball direction on collision from top
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.cur_state = GameState.GameStateName.PLAYING
    gs.motion_model = MotionModels.SIMPLE_1

    ball.rect.centery = 0  # simulate collision with top wall
    ball.update_wo(gs, None, None)

    assert ball.dy == 1  # direction should reverse


def test_update_wo_gravity_application_vector(ball, gamestate):
    """
    Test ball velocity
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.cur_state = GameState.GameStateName.PLAYING
    gs.motion_model = MotionModels.VECTOR_1
    gs.gravity_acc_length = 1.0
    gs.v_gravity_acc = Vector2(0, 1)
    gs.tick_time = 1

    initial_velocity = ball.v_vel.y
    ball.update_wo(gs, None, None)

    assert ball.v_vel.y > initial_velocity # gravity should increase y velocity


def test_update_wo_game_state_ready_to_launch(ball, gamestate):
    """
    Test ball position on READY_TO_LAUNCH state
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH

    ball.update_wo(gs, None, None)

    assert gs.cur_ball_x == ball.x  # ball should not move


def test_update_wo_game_state_game_over(ball, gamestate, playerstate, leaderboard):
    """
    Test game state is GAME_OVER when ball goes below window
    :param ball:
    :param gamestate:
    :param playerstate:
    :param leaderboard:
    :return:
    """
    gs = gamestate
    ps = playerstate
    lb = leaderboard
    ball.rect.top = HEIGHT + 100  # simulate ball going below window
    ps.lives = 1

    ball.update_wo(gs, ps, lb)

    assert gs.cur_state == GameState.GameStateName.GAME_OVER  # game should be over


def test_simple_horizontal_collision(ball, gamestate):
    """
    Test ball direction for horizontal collision
    :param ball:
    :param gamestate:
    :return:
    """
    ball.paddle_impulse_vel_length = 0

    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1
    ball.dx = 1  # moving right
    wo = pygame.sprite.Sprite()
    wo.rect = pygame.Rect(
        ball.rect.right - 1,
        ball.rect.y, 10, 10)  # simulate collision from right

    ball.detect_collision(wo, gs)

    assert ball.dx == -1  # direction should reverse


def test_simple_vertical_collision(ball, gamestate):
    """
    Test ball y position after vertical collision
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1
    ball.dy = 1  # moving down
    wo = pygame.sprite.Sprite()
    wo.rect = pygame.Rect(
        ball.rect.x,
        ball.rect.bottom - 1, 10, 10)  # simulate collision from bottom

    ball.detect_collision(wo, gs)

    assert ball.dy == -1  # direction should reverse


def test_simple_diagonal_collision(ball, gamestate):
    """
    Test ball position after diagonal collision
    :param ball:
    :param gamestate:
    :return:
    """
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1
    ball.dx = 1  # moving right
    ball.dy = 1  # moving down
    wo = pygame.sprite.Sprite()
    wo.rect = pygame.Rect(
        ball.rect.right - 1,
        ball.rect.bottom - 1, 10, 10)  # simulate diagonal collision

    ball.detect_collision(wo, gs)

    assert ball.dx == -1  # direction should reverse
    assert ball.dy == -1  # direction should reverse


def test_paddle_impulse(ball, gamestate, paddle):
    """
    Test ball velocity changes after collision when impulse is set
    :param ball:
    :param gamestate:
    :param paddle:
    :return:
    """
    gs = gamestate
    gs.paddle_impulse_vel_length = 0
    gs.motion_model = MotionModels.VECTOR_1
    gs.paddle_impulse_vel_length = 10.0  # set impulse
    initial_velocity = ball.v_vel.y

    ball.detect_collision(paddle, gs)

    assert ball.v_vel.y != initial_velocity  # velocity should change


def test_reset_position(ball):
    """
    Test ball resets position
    :param ball:
    :return:
    """
    initial_position = ball.rect.center
    ball.reset_position()
    assert ball.rect.center != initial_position  # position should reset


def test_move_to_x(ball):
    """
    Test ball moves to correct X position
    :param ball:
    :return:
    """
    ball.move_to_x(90)
    assert ball.rect.x == 90
    assert ball.v_pos.x == 90
    assert ball.x == 90
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH


def test_move_to_x_stays_onscreen_left(ball):
    """
    Test ball stays on screen when x position is not on screen
    :param ball:
    :return:
    """
    ball.move_to_x(50)
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH


def test_move_to_x_stays_onscreen_right(ball):
    """
    Test ball stays on screen when x position is not on screen
    :param ball:
    :return:
    """
    ball.move_to_x(WIDTH+1)
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH
