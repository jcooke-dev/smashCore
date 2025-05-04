"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas
    Module Description: This is the test harness for testing the GameEngine.events_handler().
"""

import pytest
from unittest.mock import MagicMock, patch
import pygame
from gameengine import GameEngine
from gamestate import GameState
from constants import PADDLE_IMPULSE_INCREMENT, WORLD_GRAVITY_ACC_INCREMENT
from motionmodels import MotionModels


@pytest.fixture
def mock_pygame():
    """
    Set up mock pygame object dependencies
    """
    with patch("pygame.quit") as mock_pygame_quit, \
         patch("pygame.key.get_pressed") as mock_key_pressed, \
         patch("pygame.mixer.init") as mock_mixer_init, \
         patch("pygame.mixer.music") as mock_mixer_music, \
         patch("pygame.mixer.find_channel") as mock_mixer_find_channel, \
         patch.object(pygame.mixer, "set_num_channels"), \
         patch("pygame.mixer.Sound") as mock_mixer_sound, \
         patch("pygame.mouse.get_pos", return_value=[4, 4]) as mock_mouse_pos, \
         patch("pygame.mouse.set_pos") as mouse_pos_set, \
         patch("pygame.mouse.set_visible") as mock_mouse_set_visible, \
         patch("pygame.display.set_mode") as mock_set_mode, \
         patch("pygame.draw.line") as mock_draw_line:

        # Setup return values if needed

        yield {
            "set_mode": mock_set_mode,
            "mouse_set_visible": mock_mouse_set_visible,
            "mouse_get_pos": mock_mouse_pos,
            "mixer_init": mock_mixer_init,
            "mixer.music": mock_mixer_music,
            "mixer.Sound": mock_mixer_sound,
            "quit": mock_pygame_quit,
            "draw_line": mock_draw_line
        }


@pytest.fixture
def setup_gameengine(mock_pygame):
    """Fixture to create a mock GameEngine object."""
    gs = GameState()
    gset = MagicMock()
    ui = MagicMock()
    ps = MagicMock()
    ps.level = 1
    ps.score = 0
    lb = MagicMock()
    gw = MagicMock()

    ge = GameEngine(lb, ps, gw, gs, gset, ui)
    ge.restart_game_button = MagicMock(pygame.Rect)
    ge.restart_game_button.collidepoint.return_value = False

    ge.quit_game_button = MagicMock(pygame.Rect)
    ge.quit_game_button.collidepoint.return_value = False

    ge.main_menu_button = MagicMock(pygame.Rect)
    ge.main_menu_button.collidepoint.return_value = False

    return ge, mock_pygame


def test_quit_event(setup_gameengine):
    """Test quitting the game with QUIT event."""
    ge, mock_pygame = setup_gameengine
    events = [pygame.event.Event(pygame.QUIT)]

    with patch.object(ge, 'clean_shutdown') as mock_shutdown:
        ge.handle_events(events)
        mock_shutdown.assert_called_once()


@pytest.mark.parametrize("starting_gs, expected_gs",
                         [(GameState.GameStateName.PLAYING, GameState.GameStateName.PAUSED),
                          (GameState.GameStateName.READY_TO_LAUNCH, GameState.GameStateName.PAUSED),
                          (GameState.GameStateName.PAUSED, GameState.GameStateName.PLAYING)])
def test_toggle_pause(starting_gs, expected_gs, setup_gameengine):
    """Test toggling pause state with ESCAPE key."""
    ge, mock_pygame = setup_gameengine
    ge.prev_state = expected_gs
    ge.mouse_pos = [10, 10]
    ge.gs.cur_state = starting_gs
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)]

    ge.handle_events(events)

    assert ge.gs.cur_state == expected_gs


def test_spacebar_gamestate_changes(setup_gameengine):
    """ Test gamestate changes from READY_TO_LAUNCH to PLAYING when spacebar is pressed
    :param setup_gameengine:
    :return:
    """
    ge, mock_pygame = setup_gameengine
    ge.gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]

    ge.handle_events(events)

    assert ge.gs.cur_state == ge.gs.cur_state == GameState.GameStateName.PLAYING


def test_toggle_dev_overlay(setup_gameengine):
    """Test toggling developer overlay with CTRL+D."""
    ge, mock_pygame = setup_gameengine
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d, mod=pygame.KMOD_CTRL)]

    ge.handle_events(events)

    assert ge.gs.show_dev_overlay is True


def test_toggle_auto_play(setup_gameengine):
    """Test toggling auto-play mode with CTRL+A."""
    ge, mock_pygame = setup_gameengine
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, mod=pygame.KMOD_CTRL)]

    ge.handle_events(events)

    assert ge.gs.auto_play is True


@pytest.mark.parametrize("event, expected_impulse", [
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=pygame.KMOD_CTRL), PADDLE_IMPULSE_INCREMENT),
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0)
])
def test_adjust_paddle_impulse(event, expected_impulse, setup_gameengine):
    """Test increasing and decreasing paddle impulse with CTRL+P and CTRL+SHIFT+P."""
    ge, mock_pygame = setup_gameengine

    ge.handle_events([event])
    assert ge.gs.paddle_impulse_vel_length == expected_impulse


@pytest.mark.parametrize("event, expected_gravity", [
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g, mod=pygame.KMOD_CTRL), WORLD_GRAVITY_ACC_INCREMENT),
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0)
])
def test_adjust_gravity(event, expected_gravity, setup_gameengine):
    """Test increasing and decreasing gravity with CTRL+G and CTRL+SHIFT+G."""
    ge, mock_pygame = setup_gameengine

    ge.handle_events([event])
    assert ge.gs.gravity_acc_length == expected_gravity


@pytest.mark.parametrize("event, expected_speed", [
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s, mod=pygame.KMOD_CTRL), 3.4),
    (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 1.4)
])
def test_adjust_ball_speed(event, expected_speed, setup_gameengine):
    """Test increasing and decreasing ball speed with CTRL+S and CTRL+SHIFT+S."""
    ge, mock_pygame = setup_gameengine
    ge.gs.ball_speed_step = 2.4

    with patch("gameengine.BALL_SPEED_STEP_INCREMENT", 1):
        ge.handle_events([event])
        assert ge.gs.ball_speed_step == expected_speed


@pytest.mark.parametrize("model_current, model_expected", [(MotionModels.VECTOR_1, MotionModels.SIMPLE_1), (MotionModels.SIMPLE_1, MotionModels.VECTOR_1)])
def test_toggle_motion_model(model_current, model_expected, setup_gameengine):
    """Test toggling motion models with CTRL+M."""
    ge, mock_pygame = setup_gameengine
    ge.gs.motion_model = model_current
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m, mod=pygame.KMOD_CTRL)

    # Toggle from SIMPLE_1 between VECTOR_1
    ge.handle_events([event])
    assert ge.gs.motion_model == model_expected


@patch("pygame.mixer.music.set_volume")
@pytest.mark.parametrize("event, starting_music_volume, expected_music_volume, expected_sounds",
    [
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_EQUALS, mod=pygame.KMOD_CTRL), 0.5, 0.6, True),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL), 0.5, 0.4, True),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_EQUALS, mod=pygame.KMOD_CTRL), 0.0, 0.1, True),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL), 0.1, 0.0, False),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL), 0.0, 0.0, False),
    ],
)
def test_adjust_music_volume(mock_set_volume, setup_gameengine, event, starting_music_volume, expected_music_volume, expected_sounds):
    """Test increasing and decreasing music volume."""
    ge, mock_pygame = setup_gameengine
    ge.gset.bgm_sounds = starting_music_volume > 0
    ge.gset.music_volume = starting_music_volume

    with patch("gameengine.MUSIC_VOLUME_STEP", .1):

        ge.handle_events([event])

        assert ge.gset.music_volume == expected_music_volume
        mock_set_volume.assert_called_with(expected_music_volume)
        assert ge.gset.bgm_sounds is expected_sounds


@pytest.mark.parametrize(
    "event, starting_sfx_volume, expected_sfx_volume, expected_sfx_sounds",
    [
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_EQUALS, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0.5, 0.6, True,),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0.5, 0.4, True),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0.0, 0.0, False),
        (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_MINUS, mod=pygame.KMOD_CTRL | pygame.KMOD_SHIFT), 0.1, 0.0, False),
    ],
)
def test_adjust_sfx_volume(setup_gameengine, event, starting_sfx_volume, expected_sfx_volume, expected_sfx_sounds):
    """Test increasing and decreasing sound effects volume."""
    ge, mock_pygame = setup_gameengine
    ge.gs.cur_state = GameState.GameStateName.SETTINGS
    ge.gset.sfx_sounds = starting_sfx_volume > 0
    ge.gset.sfx_volume = starting_sfx_volume

    with patch("gameengine.SFX_VOLUME_STEP", .1):
        ge.handle_events([event])

        assert ge.gset.sfx_volume == expected_sfx_volume
        assert ge.gset.sfx_sounds is expected_sfx_sounds
        if expected_sfx_sounds:
            mock_pygame['mixer.Sound'].assert_called_once()
            mock_sound_instance = mock_pygame['mixer.Sound'].return_value
            mock_sound_instance.set_volume.assert_called_with(expected_sfx_volume)


def test_force_load_next_level(setup_gameengine):
    """Test forcing the next level with CTRL+L."""
    ge, mock_pygame = setup_gameengine
    initial_level = ge.ps.level

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_l, mod=pygame.KMOD_CTRL)
    with patch.object(ge, "next_level") as mock_next_level:
        ge.handle_events([event])

        assert ge.ps.level == initial_level + 1
        mock_next_level.assert_called_once()


def test_high_score_input(setup_gameengine):
    """Test handling high score input."""
    ge, mock_pygame = setup_gameengine
    ge.gs.cur_state = GameState.GameStateName.GET_HIGH_SCORE
    ge.ui.tb_initials_text = ""

    # Test adding a character
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode='XYZ')
    ge.handle_events([event])
    assert ge.ui.tb_initials_text == "XYZ"

    # Test backspace
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    ge.handle_events([event])
    assert ge.ui.tb_initials_text == "XY"

    # Test submitting the high score
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    with patch.object(ge.lb, "add_score") as mock_add_score:
        ge.handle_events([event])
        mock_add_score.assert_called_once_with(ge.ps, ge.ui)
        assert ge.gs.cur_state == GameState.GameStateName.GAME_OVER


def test_mouse_button_down_in_high_score(setup_gameengine):
    """Test mouse click on high score submit button."""
    ge, mock_pygame = setup_gameengine
    ge.gs.cur_state = GameState.GameStateName.GET_HIGH_SCORE
    ge.high_score_enter_btn = MagicMock()
    ge.high_score_enter_btn.collidepoint.return_value = True

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(4, 4))
    with patch.object(ge.lb, "add_score") as mock_add_score:
        ge.handle_events([event])
        mock_add_score.assert_called_once_with(ge.ps, ge.ui)
        assert ge.gs.cur_state == GameState.GameStateName.GAME_OVER


@pytest.mark.parametrize("cur_state", [GameState.GameStateName.PAUSED, GameState.GameStateName.GAME_OVER])
def test_mouse_button_down_and_paused_or_game_over(cur_state, setup_gameengine):
    ge, mock_pygame = setup_gameengine
    ge.gs.cur_state = cur_state
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(4, 4))

    ge.restart_game_button.collidepoint.return_value = True
    with patch.object(ge, "reset_game") as mock_reset, patch.object(ge, "clean_shutdown") as mock_shutdown:
        ge.restart_game_button.collidepoint.return_value = True
        ge.handle_events([event])
        mock_reset.assert_called_once()

        ge.restart_game_button.collidepoint.return_value = False
        ge.quit_game_button.collidepoint.return_value = True
        ge.handle_events([event])
        mock_shutdown.assert_called_once()

        ge.quit_game_button.collidepoint.return_value = False
        ge.main_menu_button.collidepoint.return_value = True
        ge.handle_events([event])
        assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN
