"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Level class.
"""
import pytest
from unittest import mock
from unittest.mock import patch
import pygame
import assets
from obstacle import Obstacle
from brick import Brick
from levels import Levels


@pytest.fixture
def mock_gameworld():
    class GameWorld:
        def __init__(self):
            self.world_objects = []
    return GameWorld()


# Test get_level_name_from_num
@pytest.mark.parametrize("input_level, expected_enum", [
    (1, Levels.LevelName.SMASHCORE_1),
    (3, Levels.LevelName.SMASHCORE_IMG_CHAMFER_1),
    (7, Levels.LevelName.SMASHCORE_UNBREAKABLE_1),
    (8, Levels.LevelName.SMASHCORE_1),  # Wraps around
    (11, Levels.LevelName.SMASHCORE_SOLID_ROWS_IMG_CHAMFER_1),
    (14, Levels.LevelName.SMASHCORE_UNBREAKABLE_1),  # Wraps around
    (15, Levels.LevelName.SMASHCORE_1),  # Wraps around
])
def test_get_level_name_from_num(input_level, expected_enum):
    result = Levels.get_level_name_from_num(input_level)
    assert result == expected_enum


@mock.patch("assets.pygame.image.load")
@mock.patch("pygame.transform.scale")
def test_level_smashcore_1(mock_scale_image, mock_image_load, mock_gameworld):
    assets.load_assets()
    Levels.build_level(mock_gameworld.world_objects, Levels.LevelName.SMASHCORE_1)

    for brick in mock_gameworld.world_objects:
        assert isinstance(brick, Brick)
        assert isinstance(brick.rect, pygame.Rect)
        assert 30 <= brick.color[0] <= 255  # Randomized RGB values
        assert 1 <= brick.value <= 10


# Test build_level
@pytest.mark.parametrize("level_name, expected_brick_count", [
    (Levels.LevelName.SMASHCORE_1, 40),  # 10x4 grid
    (Levels.LevelName.SMASHCORE_IMG_CHAMFER_1, 40), #10x4 grid
])
def test_build_level(level_name, expected_brick_count):
    with patch("assets.BRICK_COLORS", return_value=[]) as mock_assets, patch("pygame.transform.scale") as mock_image:
        gw_list = []
        Levels.build_level(gw_list, level_name)
        assert len(gw_list) == expected_brick_count
        assert all(isinstance(obj, Brick) for obj in gw_list)


# Test generate_grid_level with mock data results in 11 columns
@patch("levels.constants.WIDTH", 1200)
def test_generate_grid_level_basic():
    gw_list = []
    rows = 5
    columns = 11
    values = [10, 7, 5, 3, 1]
    row_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

    Levels.generate_grid_level(
        gw_list=gw_list,
        rows=rows,
        values=values,
        row_colors=row_colors,
    )

    assert len(gw_list) == rows * columns
    for obj in gw_list:
        assert isinstance(obj, Brick)
        assert obj.value in values
        assert obj.color in row_colors


# Test generate_grid_level with width of 600 results in 5 columns
@patch("levels.constants.WIDTH", 600)
def test_generate_grid_level_basic_width_600():
    gw_list = []
    rows = 5
    columns = 5
    values = [10, 7, 5, 3, 1]
    row_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

    Levels.generate_grid_level(
        gw_list=gw_list,
        rows=rows,
        values=values,
        row_colors=row_colors,
    )

    assert len(gw_list) == rows * columns
    for obj in gw_list:
        assert isinstance(obj, Brick)
        assert obj.value in values
        assert obj.color in row_colors


# test generate_grid_level with not enough row_colors results in 3 rows
@patch("levels.constants.WIDTH", 1200)
def test_generate_grid_level_three_rows_colors():
    gw_list = []
    rows = 5
    columns = 11
    values = [10, 7, 5, 3, 1]
    row_colors = [(0, 0, 255), (255, 255, 0), (255, 165, 0)]

    Levels.generate_grid_level(
        gw_list=gw_list,
        rows=rows,
        values=values,
        row_colors=row_colors,
    )

    assert len(gw_list) == len(row_colors) * columns
    for obj in gw_list:
        assert isinstance(obj, Brick)
        assert obj.value in values
        assert obj.color in row_colors


# test generate_grid_level with not enough values results in 4 rows
@patch("levels.constants.WIDTH", 1200)
def test_generate_grid_level_four_values():
    gw_list = []
    rows = 5
    columns = 11
    values = [7, 5, 3, 1]
    row_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

    Levels.generate_grid_level(
        gw_list=gw_list,
        rows=rows,
        values=values,
        row_colors=row_colors,
    )

    assert len(gw_list) == len(values) * columns
    for obj in gw_list:
        assert isinstance(obj, Brick)
        assert obj.value in values
        assert obj.color in row_colors


# Test generate_grid_level with skip_positions
def test_generate_grid_level_with_skipped_positions():
    gw_list = []
    rows = 5
    columns = 11
    skip_positions = [(2, 2), (3, 3)]

    with patch("levels.constants.WIDTH", 1200):
        Levels.generate_grid_level(
            gw_list=gw_list,
            rows=rows,
            skip_positions=skip_positions,
        )

    # Check skipped positions
    assert len(gw_list) == rows*columns - len(skip_positions)
    skipped_bricks = [(brick.rect.x, brick.rect.y) for idx, brick in enumerate(gw_list)]
    for pos in skip_positions:
        assert pos not in skipped_bricks


# Test generate_grid_level with strong bricks
@patch ("pygame.transform.scale")
def test_generate_grid_level_with_strong_bricks(mock_scaled_image):
    gw_list = []
    rows = 5
    strong_bricks = [(1, 1), (3, 2)]

    with patch("levels.constants.WIDTH", 1200):
        Levels.generate_grid_level(
            gw_list=gw_list,
            rows=rows,
            strong_bricks=strong_bricks,
        )

    # Check strong bricks
    for idx, obj in enumerate(gw_list):
        if (obj.rect.x, obj.rect.y) in strong_bricks:
            assert obj.strength == 5  # Strong brick strength


# Test generate_grid_level with obstacle bricks
def test_generate_grid_level_with_obstacle_bricks():
    gw_list = []
    rows = 5
    obstacle_bricks = [(1, 1), (3, 2)]

    with patch("levels.constants.WIDTH", 1200):
        Levels.generate_grid_level(
            gw_list=gw_list,
            rows=rows,
            unbreakable=obstacle_bricks,
        )

    # Check obstacle bricks
    for idx, obj in enumerate(gw_list):
        if (obj.rect.x, obj.rect.y) in obstacle_bricks:
            assert isinstance(obj, Obstacle)
