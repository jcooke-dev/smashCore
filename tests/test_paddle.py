"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Paddle class.
"""

from paddle import Paddle
from constants import BLACK
from constants import PAD_WIDTH, PAD_HEIGHT, WIDTH
from unittest import mock


@mock.patch("pygame.draw.rect")
def test_draw_wo(mock_rect):
    """
    Assert draw_wo calls pygame.draw.rect
    :param mock_rect:
    :return:
    """
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.draw_wo(mock.ANY)
    assert mock_rect.call_count == 1


def test_move_left():
    """
    Asserts the paddle x position is on the screen (greater than 0)
    :return:
    """
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_left(1000)
    assert paddle.rect.x >= 0


def test_move_right():
    """
    Asserts the paddle x position is on the screen (less than the screen width)
    :return:
    """
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_right(WIDTH+500)
    assert paddle.rect.x <= WIDTH - PAD_WIDTH
    assert paddle.rect.x >= 0


def test_move_by_mouse_left():
    """
    Asserts the paddle x position is on the screen (greater than 0)
    :return:
    """
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_to_x(-5)
    assert paddle.rect.x >= 0


def test_move_by_mouse_right():
    """
    Asserts the paddle x position is on the screen (less than the screen width)
    :return:
    """
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_to_x(WIDTH + 500)
    assert paddle.rect.x <= WIDTH - PAD_WIDTH
    assert paddle.rect.x >= 0
