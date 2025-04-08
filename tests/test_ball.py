import pygame
import pytest
from paddle import Paddle
from pygame import Vector2
from ball import Ball
from constants import BALL_RADIUS, BALL_SPEED_SIMPLE, WIDTH, HEIGHT, WHITE
from gamestates import GameStates
from motionmodels import MotionModels


@pytest.fixture
def ball():
    pygame.init()
    return Ball(x=10, y=10)


@pytest.fixture
def paddle():
    a_paddle = Paddle(WHITE, 100, 50)
    a_paddle.rect = pygame.Rect(90, 90, 10, 10)
    return a_paddle


@pytest.fixture
def playerstate():
    class PlayerState:
        def __init__(self):
            self.lives = 3
    return PlayerState()


@pytest.fixture
def gamestate():
    class GameState:
        def __init__(self):
            self.cur_state = GameStates.PLAYING
            self.motion_model = MotionModels.SIMPLE_1
            self.gravity_acc_length = 0
            self.v_gravity_acc = Vector2(0, 0)
            self.tick_time = 1
            self.cur_ball_x = 0
    return GameState()


def test_initial_state(ball):
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
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1

    ball.update_wo(gs, None)

    assert ball.rect.x == ball.x
    assert ball.rect.y == ball.y


def test_update_wo_wall_collision_left_simple(ball, gamestate):
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1

    ball.dx = -1 # must ensure moving to the left before collision test (since __init__ has it randomly either -1, 1)

    ball.rect.centerx = 0  # simulate collision with left wall
    ball.update_wo(gs, None)

    assert ball.dx == 1  # direction should reverse


def test_update_wo_wall_collision_right_simple(ball, gamestate):
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1

    ball.dx = 1  # must ensure moving to the right before collision test (since __init__ has it randomly either -1, 1)

    ball.rect.centerx = WIDTH  # simulate collision with right wall
    ball.update_wo(gs, None)

    assert ball.dx == -1  # direction should reverse


def test_update_wo_wall_collision_top_simple(ball, gamestate):
    gs = gamestate
    gs.motion_model = MotionModels.SIMPLE_1

    ball.rect.centery = 0  # simulate collision with top wall
    ball.update_wo(gs, None)

    assert ball.dy == 1  # direction should reverse


def test_update_wo_gravity_application_vector(ball, gamestate):
    gs = gamestate
    gs.motion_model = MotionModels.VECTOR_1
    gs.gravity_acc_length = 1.0
    gs.v_gravity_acc = Vector2(0, 1)
    gs.tick_time = 1

    initial_velocity = ball.v_vel.y
    ball.update_wo(gs, None)

    assert ball.v_vel.y > initial_velocity # gravity should increase y velocity


def test_update_wo_game_state_ready_to_launch(ball, gamestate):
    gs = gamestate
    gs.cur_state = GameStates.READY_TO_LAUNCH

    ball.update_wo(gs, None)

    assert gs.cur_ball_x == ball.x  # ball should not move


def test_update_wo_game_state_game_over(ball, gamestate, playerstate):
    gs = gamestate
    ps = playerstate
    ball.rect.top = HEIGHT + 100  # simulate ball going below window
    ps.lives = 1

    ball.update_wo(gs, ps)

    assert gs.cur_state == GameStates.GAME_OVER  # game should be over


def test_simple_horizontal_collision(ball, gamestate):
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
    gs = gamestate
    gs.paddle_impulse_vel_length = 0
    gs.motion_model = MotionModels.VECTOR_1
    gs.paddle_impulse_vel_length = 10.0  # set impulse
    initial_velocity = ball.v_vel.y

    ball.detect_collision(paddle, gs)

    assert ball.v_vel.y != initial_velocity  # velocity should change


def test_reset_position(ball):
    initial_position = ball.rect.center
    ball.reset_position()
    assert ball.rect.center != initial_position  # position should reset


def test_move_to_x(ball):
    ball.move_to_x(90)
    assert ball.rect.x == 90
    assert ball.v_pos.x == 90
    assert ball.x == 90
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH


def test_move_to_x_stays_onscreen_left(ball):
    ball.move_to_x(50)
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH


def test_move_to_x_stays_onscreen_right(ball):
    ball.move_to_x(WIDTH+1)
    assert ball.rect.left > 0
    assert ball.rect.right < WIDTH
