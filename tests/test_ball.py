import pytest
from ball import Ball
from constants import BALL_RADIUS, BALL_SPEED_SIMPLE
from unittest import mock

@pytest.fixture
def ball():
    return Ball(10, 10)


def test_initial_state(ball):
    assert ball.can_react is True
    assert ball.radius == BALL_RADIUS
    assert ball.x == 10 - BALL_RADIUS
    assert ball.y == 10
    assert ball.image is None
    assert ball.dx == 1 or ball.dx == -1
    assert ball.dy == -1
    assert ball.speed == BALL_SPEED_SIMPLE


