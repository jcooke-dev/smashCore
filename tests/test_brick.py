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
    """
    Tests the initial state of a brick when only the rect, color, and value
    are passed in
    :param brick:
    :return:
    """
    assert brick.rect == pygame.Rect(0, 0, 100, 50)
    assert brick.color == WHITE
    assert brick.value == 3
    assert brick.strength == 1
    assert brick.bonus == 0


def test_initial_state_no_value():
    """
    Test initial state sets default values for
    value, strength, and bonus when no value is passed in
    :return:
    """
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    brick = Brick(rect, WHITE)
    assert brick.rect == pygame.Rect(0, 0, 100, 50)
    assert brick.color == WHITE
    assert brick.value == 1
    assert brick.strength == 1
    assert brick.bonus == 0
    pygame.quit()

def test_initial_state_with_bonus():
    """
    Test that a bonus is set during intial state when passed in
    :return:
    """
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    brick = Brick(rect, WHITE, bonus=4)
    assert brick.bonus == 4
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


@mock.patch("pygame.image")
@mock.patch("pygame.Surface")
def test_draw_wo_with_image(mock_surface, mock_image):
    """
    Assert draw_wo calls pygame.draw.rect
    :param mock_rect:
    :return:
    """
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    brick_with_image = Brick(rect = rect, color = WHITE, value = 1, image = mock_image)
    brick_with_image.draw_wo(mock_surface)
    pygame.quit()

    # Check pygame.draw.rect was called within draw_wo with specified arguements
    #mock_rect.assert_called_with(screen_mock, brick.color, brick.rect)
    mock_surface.blit.assert_called_with(mock_image, rect)


def test_add_collision(brick):
    brick.add_collision()
    assert brick.strength == 0


def test_should_score(brick):
    assert brick.should_score() is True


def test_should_remove(brick):
    assert brick.should_remove() is False
    brick.strength = 0
    assert brick.should_remove() is True
    brick.strength = 3
    assert brick.should_remove() is False
    brick.strength = -4
    assert brick.should_remove() is True
