"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Level class.
"""
import pygame
import pytest
from unittest import mock
from src.brick import Brick
from levels import Levels
import assets


@pytest.fixture
def mock_gameworld():
    class GameWorld:
        def __init__(self):
            self.world_objects = []
    return GameWorld()


@mock.patch("src.assets.pygame.image.load")
@mock.patch("pygame.transform.scale")
def test_level_smashcore_1(mock_scale_image, mock_image_load, mock_gameworld):
    assets.load_assets()
    Levels.build_level(mock_gameworld.world_objects, Levels.LevelName.SMASHCORE_1)

    # Assert that the correct number of bricks are added
    assert len(mock_gameworld.world_objects) == 40  # 10 columns * 4 rows
    for brick in mock_gameworld.world_objects:
        assert isinstance(brick, Brick)
        assert isinstance(brick.rect, pygame.Rect)
        assert 30 <= brick.color[0] <= 255  # Randomized RGB values
        assert 1 <= brick.value <= 10



def test_next_level_1():
    next_level = Levels.get_level_name_from_num(1)
    assert next_level is Levels.LevelName.SMASHCORE_1


def test_next_level_3():
    next_level = Levels.get_level_name_from_num(3)
    assert next_level is Levels.LevelName.SMASHCORE_IMG_CHAMFER_1


def test_next_level_last():
    last_level: Levels.LevelName = list(Levels.LevelName)[-1]
    next_level = Levels.get_level_name_from_num(last_level.value + 1)
    assert next_level is Levels.LevelName.SMASHCORE_1