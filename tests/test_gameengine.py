"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the GameEngine class.
"""
from unittest.mock import patch

import pytest

import assets
import constants
from unittest import mock
from gameengine import GameEngine
from gamesettings import GameSettings
from gamestate import GameState
from leveltheme import LevelTheme
from userinterface import UserInterface
from playerstate import PlayerState
from leaderboard import Leaderboard
from gameworld import GameWorld
from ball import Ball


@pytest.fixture
def mock_pygame():
    """
    Set up mock pygame object dependencies
    :return:
    """
    with mock.patch("pygame.quit") as mock_pygame_quit, \
         mock.patch("pygame.event.get") as mock_event_get,\
         mock.patch("pygame.mixer.init") as mock_mixer_init, \
         mock.patch("pygame.mixer.music") as mock_mixer_music, \
         mock.patch("pygame.mouse.set_visible") as mock_set_visible, \
         mock.patch("pygame.display.set_caption") as mock_set_caption, \
         mock.patch("pygame.time.get_ticks", return_value=123456) as mock_get_ticks, \
         mock.patch("pygame.color") as mock_color, \
         mock.patch("pygame.rect") as mock_rect, \
         mock.patch("pygame.time.Clock") as mock_clock, \
         mock.patch("pygame.Surface") as mock_surface, \
         mock.patch("pygame.display.set_mode") as mock_set_mode:

        # Setup return values if needed
        mock_set_mode.return_value = mock.MagicMock(name="screen")
        mock_surface.return_value = mock.MagicMock(name="surface")
        mock_clock.return_value = mock.MagicMock(name="clock")

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
            "mixer.music": mock_mixer_music,
            "event.get": mock_event_get,
            "quit": mock_pygame_quit
        }


@pytest.fixture
def starting_ge(mock_pygame):
    """
    Create initial gameengine for testing
    :param mock_pygame:
    :return:
    """
    with mock.patch("assets.pygame.image.load") as mock_image_load:
        mock_image = mock.Mock()
        mock_image_load.return_value = mock_image

        ui = mock.MagicMock(UserInterface)
        gset = mock.MagicMock(GameSettings)
        gs = mock.MagicMock(GameState)
        gw = mock.MagicMock(GameWorld)
        ps = mock.MagicMock(PlayerState)
        lb = mock.MagicMock(Leaderboard)

        ui.start_button_rect = mock.MagicMock()
        ui.credits_button_rect = mock.MagicMock()

        ge = GameEngine(lb, ps, gw, gs, gset, ui)
        return ge, mock_pygame


def test_initial_state(starting_ge):
    """
    Test the initial state set the mouse pointer to not visible

    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge
    mock_pygame["set_visible"].assert_called_once_with(False)


def test_gamestate_reset(starting_ge):
    """
    Tests game is reset to initial values

    :param starting_ge:
    :return:
    """
    dummy_colors = ["red", "green", "blue"]
    with patch("assets.BRICK_COLORS", new=dummy_colors) as mock_assets, patch("pygame.transform.scale") as mock_image:

        ge, mock_pygame = starting_ge
        ge.fps = 500 # any number is fine as long as it isn't initial FPS
        ge.gs.cur_state = GameState.GameStateName.GAME_OVER
        ge.ps.lives = 0
        ge.ps.theme = LevelTheme.MODERN
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


def test_next_level(starting_ge):
    """
    Tests that ball position is reset, ball speed is increased based on predefined increment,
    the next level number is retrieved, the levels are built for the level number,
    FPS is reset, and GameState is set to READY_TO_LAUNCH
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge
    with mock.patch("gameengine.Levels.get_level_name_from_num", return_value="Level_2") as mock_get_level_name, \
            mock.patch("gameengine.Levels.build_level") as mock_build_level:

        mock_ball = mock.MagicMock(Ball)
        mock_ball.v_vel_unit = 1
        ge.gw.world_objects = [mock_ball]

        # Set initial player state and level
        ge.ps.level = 1
        ge.ps.theme = LevelTheme.MODERN

        # Call next_level
        ge.next_level()

        # Ball reset position and speed assertions
        mock_ball.reset_position.assert_called_once()
        expected_ball_speed_v = constants.BALL_SPEED_VECTOR + (ge.ps.level * constants.BALL_SPEED_LEVEL_INCREMENT)
        assert mock_ball.speed_v == expected_ball_speed_v
        assert ge.gs.ball_speed_increased_ratio == expected_ball_speed_v / constants.BALL_SPEED_VECTOR
        assert mock_ball.speed == constants.BALL_SPEED_SIMPLE + (ge.ps.level * constants.BALL_SPEED_LEVEL_INCREMENT)

        # Ensure the level is built
        mock_get_level_name.assert_called_once_with(ge.ps.theme, ge.ps.level)
        mock_build_level.assert_called()

        # Ensure FPS is reset and game state is ready to launch
        assert ge.fps == constants.INITIAL_FPS_SIMPLE
        assert ge.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH


def test_draw_world_and_status(starting_ge):
    """
    Test that draw_wo is called on world objects and ui.draw_status is called

    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge
    mock_wo = mock.MagicMock()
    mock_wo.draw_wo.return_value = None
    ge.gw.world_objects = [mock_wo]
    ge.ps.lives = 2
    ge.ps.score = 320
    ge.ps.level = 1

    # Call draw_world_and_status
    ge.draw_world_and_status()

    # Ensure draw_wo was called once
    # Ensure draw_status was called on UI with player status
    mock_wo.draw_wo.assert_called_once_with(ge.screen)
    ge.ui.draw_status.assert_called_once_with(2, 320, 1)


@mock.patch("gameengine.exit")
def test_clean_shutdown(mock_exit, starting_ge):
    """
    Tests that clean_shutdown stops the music, sets the current_music_path to None,
    sets the GameState to GAME_OVER, calls pygame.quit, and exit()
    :param mock_exit:
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge

    ge.clean_shutdown()

    mock_pygame["mixer.music"].stop.assert_called_once()
    assert ge.current_music_path is None
    assert ge.gs.running is False
    assert ge.gs.cur_state == GameState.GameStateName.GAME_OVER

    ge.lb.store.assert_called_once()
    mock_pygame['quit'].assert_called_once()
    mock_exit.assert_called_once()


def test_play_music_bgm_sound_off(starting_ge):
    """
    Tests that when bgm_sounds is False, the music is stopped
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge

    #Set GameState background sounds to False
    ge.gset.bgm_sounds = False

    # Play Music
    ge.play_music()

    # Assert that music is stopped
    mock_pygame["mixer.music"].stop.assert_called_once()
    assert ge.current_music_path is None


def test_play_music_correct_file_and_volume(starting_ge):
    """
    Tests that music plays correct music for the current game state
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge

    ge.gset.bgm_sounds = True
    ge.gs.cur_state = GameState.GameStateName.GET_HIGH_SCORE
    ge.gset.music_volume = 1.0
    music_path = '/path/to/music.wav'
    assets.MUSIC_PATHS[GameState.GameStateName.GET_HIGH_SCORE] = music_path

    ge.play_music()

    mock_pygame['mixer.music'].load.assert_called_once_with(music_path)
    mock_pygame['mixer.music'].set_volume.assert_called_once_with(1.0)
    mock_pygame['mixer.music'].play.assert_called_once_with(0)
    assert ge.current_music_path == music_path


def test_play_music_no_music_path(starting_ge):
    """
    Tests that music plays correct music for the current game state
    :param starting_ge:
    :return:
    """
    ge, mock_pygame = starting_ge

    ge.gset.bgm_sounds = True
    ge.gs.cur_state = GameState.GameStateName.HOW_TO_PLAY
    ge.current_music_path = "/path/to/current_music.wav"


    # Ensure no MUSIC_PATH is defined for this state
    if GameState.GameStateName.HOW_TO_PLAY in assets.MUSIC_PATHS:
        del assets.MUSIC_PATHS[GameState.GameStateName.HOW_TO_PLAY]

    ge.play_music()

    mock_pygame['mixer.music'].stop.assert_called_once()
    assert ge.current_music_path is None
