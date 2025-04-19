"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Obstacle class.
"""
import pygame
import pytest
import constants
from obstacle import Obstacle


@pytest.fixture
def obstacle():
    pygame.init()
    rect = pygame.Rect(0, 0, 100, 50)
    obstacle = Obstacle(rect, constants.WHITE)
    yield obstacle
    pygame.quit()


def test_initial_state(obstacle):
    assert obstacle.rect == pygame.Rect(0, 0, 100, 50)
    assert obstacle.color == constants.WHITE
    assert obstacle.image is None
    assert obstacle.text == ""
