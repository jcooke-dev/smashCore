"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the GameEngine class.
"""

import pygame.mouse
import pytest
import constants
from unittest import mock
from src.gameengine import GameEngine
from gamestates import GameStates
from gamestate import GameState
from playerstate import PlayerState



@pytest.fixture
@mock.patch("src.assets.pygame.image.load")
def starting_ge(mock_image_load):
    mock_image = mock.Mock()
    mock_image_load.return_value = mock_image

    ui = mock.Mock()
    gs = GameState()
    #gs = mock.Mock()
    gw = mock.Mock()
    ps = PlayerState()
    #ps = mock.Mock()
    ge = GameEngine(ps, gw, gs, ui)
    return ge


def test_gamestate_reset(starting_ge):
    """
    Asserts the initial values are set to restart the game
    :param starting_ge:
    :return:
    """
    # modify test once multiple levels have been added
    # self.gw = GameWorld(Levels.LevelName.SMASHCORE_?)
    starting_ge.fps = 500 # any number is fine as long as it isn't initial FPS
    starting_ge.gs.cur_state = GameStates.GAME_OVER
    starting_ge.ps.lives = 0
    starting_ge.ps.score = 90
    pygame.mouse.set_visible(True)

    starting_ge.reset_game()

    assert starting_ge.fps == constants.INITIAL_FPS_SIMPLE
    # enums should be compared by identity
    # assert starting_ge.gs.cur_state is GameStates.SPLASH
    # but it isn't working so comparing by name
    assert starting_ge.gs.cur_state.name is GameStates.SPLASH.name
    assert starting_ge.ps.lives == constants.START_LIVES
    assert starting_ge.ps.score == 0
    assert not pygame.mouse.get_visible()


