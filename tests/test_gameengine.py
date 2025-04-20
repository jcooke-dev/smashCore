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


@pytest.fixture
def starting_ge():
    with mock.patch("src.assets.pygame.image.load") as mock_image_load:
        mock_image = mock.Mock()
        mock_image_load.return_value = mock_image

        ui = mock.Mock()
        gs = GameState()
        gw = mock.Mock()
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
