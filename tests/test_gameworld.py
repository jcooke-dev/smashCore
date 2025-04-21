"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the GameWorld class.
"""
from unittest import mock
import pytest

from gameworld import GameWorld
from src.levels import Levels
from src.ball import Ball
from src.paddle import Paddle
from src.brick import Brick
from obstacle import Obstacle


@pytest.fixture
def gameworld():
    with mock.patch("pygame.Rect") as mock_rect, mock.patch("pygame.color") as mock_color:
        obstacle_1 = Obstacle(mock_rect, mock_color)
        obstacle_2 = Obstacle(mock_rect, mock_color)
        brick_1 = Brick(mock_rect, mock_color)
        brick_2 = Brick(mock_rect, mock_color)
        brick_3 = Brick(mock_rect, mock_color)

        gw = GameWorld()
        # set world_objects in gameworld
        gw.world_objects = [obstacle_1, brick_1, brick_2, obstacle_2, brick_3]
        return gw

def test_gameworld_init():
    """
    Test the gameworld has a ball, paddle, and at least one brick
    :return:
    """
    Levels.build_level = mock.MagicMock()

    gw = GameWorld()

    ball_found = any(isinstance(obj, Ball) for obj in gw.world_objects)
    paddle_found = any(isinstance(obj, Paddle) for obj in gw.world_objects)
    assert ball_found
    assert paddle_found
    Levels.build_level.assert_called()


def test_remove_obstacles(gameworld):
    """
    Tests that all Obstacles are removed from world_objects

    :param mock_obstacle_rect:
    :param mock_brick_rect:
    :param starting_ge:
    :return:
    """
    #remove obstacles from gameworld world_objects
    gameworld.remove_obstacles()

    assert len(gameworld.world_objects) == 3
    gameworld.world_objects = [obj for obj in gameworld.world_objects if not isinstance(obj, Obstacle)]


def test_remove_bricks(gameworld):
    """
    Tests that all Obstacles are removed from world_objects

    :param mock_obstacle_rect:
    :param mock_brick_rect:
    :param starting_ge:
    :return:
    """
    #remove obstacles from gameworld world_objects
    gameworld.remove_bricks()

    assert len(gameworld.world_objects) == 2
    gameworld.world_objects = [obj for obj in gameworld.world_objects if not isinstance(obj, Brick)]

