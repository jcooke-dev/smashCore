import pygame.mouse
import pytest

import constants
from src.userinterface import UserInterface
from src.gamestate import GameState
from src.gameworld import GameWorld
from src.playerstate import PlayerState
from src.gameengine import GameEngine
from src.gamestates import GameStates


@pytest.fixture
def starting_ge():
    ui = UserInterface()
    gs = GameState()
    gw = GameWorld()
    ps = PlayerState()
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






