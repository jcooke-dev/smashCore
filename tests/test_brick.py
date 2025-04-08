"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Brick class.
"""

import pygame
import pytest
from unittest import mock
from brick import Brick
from constants import WHITE


@pytest.fixture
def brick():
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    brick = Brick(rect, WHITE, 3)
    yield brick
    pygame.quit()


def test_initial_state(brick):
    assert brick.rect == pygame.Rect(0, 0, 100, 50)
    assert brick.color == WHITE
    assert brick.value == 3
    assert brick.strength == 1


def test_initial_state_no_value(brick):
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    brick = Brick(rect, WHITE)
    assert brick.rect == pygame.Rect(0, 0, 100, 50)
    assert brick.color == WHITE
    assert brick.value == 1
    assert brick.strength == 1
    pygame.quit()


@mock.patch("pygame.draw.rect")
def test_draw_wo(mock_rect, brick):
    """
    Assert draw_wo calls pygame.draw.rect
    :param mock_rect:
    :return:
    """
    screen_mock = mock.Mock()
    brick.draw_wo(screen_mock)

    # Check pygame.draw.rect was called within draw_wo with specified arguements
    mock_rect.assert_called_with(screen_mock, brick.color, brick.rect)


def test_add_collision(brick):
    brick.add_collision()
    assert brick.strength == 0


def test_should_remove(brick):
    assert brick.should_remove() == False
    brick.strength = 0
    assert brick.should_remove() == True
    brick.strength = 3
    assert brick.should_remove() == False
    brick.strength = -4
    assert brick.should_remove() == True