"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the GameEngine class.
"""

import pytest
import constants
from unittest import mock
from gameengine import GameEngine
from gamestate import GameState
import src
from src.levels import Levels
from playerstate import PlayerState
from leaderboard import Leaderboard
from brick import Brick
from obstacle import Obstacle
from ball import Ball


@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.mixer.init") as mock_mixer_init, \
         mock.patch("pygame.mixer.music.stop") as mock_mixer_music_stop, \
         mock.patch("pygame.mouse.set_visible") as mock_set_visible, \
         mock.patch("pygame.display.set_caption") as mock_set_caption, \
         mock.patch("pygame.time.get_ticks", return_value=123456) as mock_get_ticks, \
         mock.patch("pygame.color") as mock_color, \
         mock.patch("pygame.rect") as mock_rect, \
         mock.patch("pygame.time.Clock") as mock_clock, \
         mock.patch("pygame.Surface") as mock_surface, \
         mock.patch("pygame.display.set_mode") as mock_set_mode:

        # Setup return values if needed
        mock_set_mode.return_value = mock.Mock(name="screen")
        mock_surface.return_value = mock.Mock(name="surface")
        mock_clock.return_value = mock.Mock(name="clock")

        yield {
            "set_mode": mock_set_mode,
            "surface": mock_surface,
            "clock": mock_clock,
            "rect": mock_rect,
            "color": mock_color,
            "get_ticks": mock_get_ticks,
            "set_caption": mock_set_caption,
            "set_visible": mock_set_visible,
            "mixer_init": mock_mixer_init,
            "mixer.music.stop": mock_mixer_music_stop
        }


@pytest.fixture
def mock_gameworld():
    class GameWorld():
        def __init__(self):
            self.world_objects = []
    return GameWorld()


@pytest.fixture
def starting_ge(mock_gameworld, mock_pygame):
    with mock.patch("src.assets.pygame.image.load") as mock_image_load:
        mock_image = mock.Mock()
        mock_image_load.return_value = mock_image

        ui = mock.Mock()
        gs = mock.Mock()
        gw = mock_gameworld
        ps = mock.Mock()
        lb = mock.Mock()
        ge = GameEngine(lb, ps, gw, gs, ui)
        return ge, mock_pygame


def test_initial_state(starting_ge):
    ge, mock_pygame = starting_ge
    mock_pygame["set_visible"].assert_called_once_with(False)


def test_gamestate_reset(starting_ge):
    """
    Asserts the initial values are set to restart the game
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge
    ge.fps = 500 # any number is fine as long as it isn't initial FPS
    ge.gs.cur_state = GameState.GameStateName.GAME_OVER
    ge.ps.lives = 0
    ge.ps.score = 90
    ge.current_music_path = "/assets/music"

    ge.reset_game()

    assert ge.fps == constants.INITIAL_FPS_SIMPLE
    # enums should be compared by identity
    # assert starting_ge.gs.cur_state is GameStates.READY_TO_LAUNCH
    # but it isn't working so comparing by name
    assert ge.gs.cur_state.name is GameState.GameStateName.READY_TO_LAUNCH.name
    assert ge.ps.lives == constants.START_LIVES
    assert ge.ps.score == 0
    assert ge.current_music_path is None
    mock_pygame["set_visible"].assert_called_with(False)
    mock_pygame["mixer_init"].assert_called_once()


@mock.patch("src.obstacle.pygame.Rect")
@mock.patch("src.brick.pygame.Rect")
def test_remove_obstacles(mock_obstacle_rect, mock_brick_rect, starting_ge):
    ge, mock_pygame = starting_ge
    mock_rect = mock_pygame["rect"]
    mock_color = mock_pygame["color"]
    obstacle_1 = Obstacle(mock_rect, mock_color)
    obstacle_2 = Obstacle(mock_rect, mock_color)
    brick_1 = Brick(mock_rect, mock_color)
    brick_2 = Brick(mock_rect, mock_color)
    brick_3 = Brick(mock_rect, mock_color)

    #set world_objects in gameworld
    ge.gw.world_objects = [obstacle_1, brick_1, brick_2, obstacle_2, brick_3]

    #remove obstacles from gameworld world_objects
    ge.remove_obstacles()

    assert len(ge.gw.world_objects) == 3
    assert obstacle_1 not in ge.gw.world_objects
    assert obstacle_2 not in ge.gw.world_objects
    assert brick_1 in ge.gw.world_objects
    assert brick_2 in ge.gw.world_objects
    assert brick_3 in ge.gw.world_objects


@mock.patch("src.ball.pygame.image")
@mock.patch("src.ball.pygame.Rect")
@mock.patch("src.ball.Ball", spec=src.ball.Ball)
def test_next_level(mock_ball, mock_rect, mock_image, starting_ge):
    ge, mock_pygame = starting_ge
    mock_ball.v_vel_unit = 1
    ge.gw.world_objects = [mock_ball]

    # Set initial player state and level
    ge.ps.level = 1

    # Mock Levels module methods
    Levels.get_level_name_from_num = mock.MagicMock(return_value="Level_2")
    Levels.build_level = mock.MagicMock()

    # Call next_level
    ge.next_level()

    # Ensure obstacles are removed
    #ge.gw.world_objects = [obj for obj in ge.gw.world_objects if not isinstance(obj, Ball)]

    # Ball reset position and speed assertions
    mock_ball.reset_position.assert_called_once()
    expected_ball_speed_v = constants.BALL_SPEED_VECTOR + (ge.ps.level * constants.BALL_SPEED_LEVEL_INCREMENT)
    assert mock_ball.speed_v == expected_ball_speed_v
    assert ge.gs.ball_speed_increased_ratio == expected_ball_speed_v / constants.BALL_SPEED_VECTOR
    assert mock_ball.speed == constants.BALL_SPEED_SIMPLE + (ge.ps.level * constants.BALL_SPEED_LEVEL_INCREMENT)

    # Ensure the level is built
    Levels.get_level_name_from_num.assert_called_once_with(ge.ps.level)
    Levels.build_level.assert_called()

    # Ensure FPS is reset and game state is ready to launch
    assert ge.fps == constants.INITIAL_FPS_SIMPLE
    assert ge.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH

