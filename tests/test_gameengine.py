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
from playerstate import PlayerState
from leaderboard import Leaderboard
from brick import Brick
from obstacle import Obstacle


@pytest.fixture
def mock_gameworld():
    class GameWorld:
        def __init__(self):
            self.world_objects = []
    return GameWorld()


@pytest.fixture
def starting_ge(mock_gameworld):
    with mock.patch("src.assets.pygame.image.load") as mock_image_load:
        mock_image = mock.Mock()
        mock_image_load.return_value = mock_image

        ui = mock.Mock()
        gs = GameState()
        gw = mock_gameworld
        ps = PlayerState()
        lb = Leaderboard()
        ge = GameEngine(lb, ps, gw, gs, ui)
        return ge


@mock.patch("pygame.mixer.music.stop")
@mock.patch("pygame.mouse.set_visible")
def test_gamestate_reset(mock_set_visible, mock_mixer_stop, starting_ge):
    """
    Asserts the initial values are set to restart the game
    :param starting_ge:
    :return:
    """
    # modify test once multiple levels have been added
    # self.gw = GameWorld(Levels.LevelName.SMASHCORE_?)

    starting_ge.fps = 500 # any number is fine as long as it isn't initial FPS
    starting_ge.gs.cur_state = GameState.GameStateName.GAME_OVER
    starting_ge.ps.lives = 0
    starting_ge.ps.score = 90
    starting_ge.current_music_path = "/assets/music"

    starting_ge.reset_game()

    assert starting_ge.fps == constants.INITIAL_FPS_SIMPLE
    # enums should be compared by identity
    # assert starting_ge.gs.cur_state is GameStates.READY_TO_LAUNCH
    # but it isn't working so comparing by name
    assert starting_ge.gs.cur_state.name is GameState.GameStateName.READY_TO_LAUNCH.name
    assert starting_ge.ps.lives == constants.START_LIVES
    assert starting_ge.ps.score == 0
    assert starting_ge.current_music_path is None
    mock_mixer_stop.assert_called_once()
    mock_set_visible.assert_called_once_with(False)


@mock.patch("src.obstacle.pygame.Rect")
@mock.patch("src.brick.pygame.Rect")
@mock.patch("pygame.color")
@mock.patch("pygame.rect")
def test_remove_obstacles(mock_rec, mock_color, mock_obstacle_rect, mock_brick_rect, starting_ge):
    obstacle_1 = Obstacle(mock_rec, mock_color)
    obstacle_2 = Obstacle(mock_rec, mock_color)
    brick_1 = Brick(mock_rec, mock_color)
    brick_2 = Brick(mock_rec, mock_color)
    brick_3 = Brick(mock_rec, mock_color)

    #set world_objects in gameworld
    starting_ge.gw.world_objects = [obstacle_1, brick_1, brick_2, obstacle_2, brick_3]

    #remove obstacles from gameworld world_objects
    starting_ge.remove_obstacles()

    assert len(starting_ge.gw.world_objects) == 3
    assert obstacle_1 not in starting_ge.gw.world_objects
    assert obstacle_2 not in starting_ge.gw.world_objects
    assert brick_1 in starting_ge.gw.world_objects
    assert brick_2 in starting_ge.gw.world_objects
    assert brick_3 in starting_ge.gw.world_objects
