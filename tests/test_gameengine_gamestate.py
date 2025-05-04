"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for testing the GameEngine.handle_gamestate().
"""
from unittest.mock import patch

import pygame
import pytest

import constants
from unittest import mock
from unittest.mock import MagicMock

import playerstate
from gameengine import GameEngine
from gamesettings import GameSettings
from gamestate import GameState
from gameworld import GameWorld
from leveltheme import LevelTheme
from userinterface import UserInterface
from leaderboard import Leaderboard
from ball import Ball
from brick import Brick
from paddle import Paddle
from animation import Animation
import utils


@pytest.fixture
def mock_pygame():
    """
    Set up mock pygame object dependencies
    """
    with mock.patch("pygame.mixer.init") as mock_mixer_init, \
         mock.patch("pygame.mixer.music") as mock_mixer_music, \
         mock.patch.object(pygame.mixer, "Sound") as mock_mixer_sound, \
         mock.patch.object(pygame.mixer, "find_channel") as mock_mixer_find_channel, \
         mock.patch("pygame.mouse.set_visible") as mock_mouse_set_visible, \
         mock.patch("pygame.mouse.get_pos", return_value=[4]) as mock_mouse_pos, \
         mock.patch("pygame.time.get_ticks", return_value=123456) as mock_get_ticks, \
         mock.patch("pygame.display.set_mode") as mock_set_mode, \
         mock.patch.object(pygame.mixer, "set_num_channels"), \
         mock.patch("pygame.draw.line") as mock_draw_line, \
         mock.patch("pygame.font") as mock_font:

        # Setup return values if needed
        mock_set_mode.return_value = mock.MagicMock(name="screen")
        mock_font.return_value.render = MagicMock(return_value=pygame.Surface)

        yield {
            "mixer_init": mock_mixer_init,
            "mixer.music": mock_mixer_music,
            "mixer.sound": mock_mixer_sound,
            "mixer.find_channel": mock_mixer_find_channel,
            "set_mode": mock_set_mode,
            "get_ticks": mock_get_ticks,
            "font": mock_font,
            "mouse_set_visible": mock_mouse_set_visible,
            "mouse_mock_position": mock_mouse_pos,
            "draw_line": mock_draw_line
        }

@pytest.fixture
def starting_ge(mock_pygame):
    """
    Create initial gameengine for testing
    """
    with mock.patch("assets.pygame.image.load") as mock_image_load:
        mock_image = mock.Mock()
        mock_image_load.return_value = mock_image

        ui = mock.MagicMock(UserInterface)
        gset = mock.MagicMock(GameSettings)
        gset.paddle_under_auto_control = True
        gset.paddle_under_mouse_control = True
        gset.sfx_volume = 0.5
        gset.music_volume = 0.5

        gs = GameState()
        gw = mock.MagicMock(GameWorld)
        gw.world_objects = []
        ps = playerstate.PlayerState()
        lb = mock.MagicMock(Leaderboard)

        gset.is_fullscreen = False

        ge = GameEngine(lb, ps, gw, gs, gset, ui)
        return ge, mock_pygame


@pytest.fixture
def starting_ge_main_menu(starting_ge):
    """
    Set up the buttons as if the main menu is displayed
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.MENU_SCREEN

    ge.ui.start_classic_button_rect = pygame.Rect(100, 100, 100, 50)
    ge.ui.start_modern_button_rect = pygame.Rect(100, 200, 100, 50)
    ge.ui.how_to_play_button_rect = pygame.Rect(100, 300, 100, 50)
    ge.ui.settings_button_rect = pygame.Rect(100, 400, 100, 50)
    ge.ui.leader_button_rect = pygame.Rect(100, 500, 100, 50)
    ge.ui.credits_button_rect = pygame.Rect(100, 600, 100, 50)
    ge.ui.quit_button_start_rect = pygame.Rect(100, 700, 100, 50)
    return ge, mock_pygame


@pytest.fixture
def starting_ge_settings(starting_ge):
    """
    Set up the buttons as if settings screen
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.SETTINGS

    ge.ui.vol_bgm_btn_rect = mock.MagicMock(pygame.Rect)
    ge.ui.vol_bgm_btn_rect.collidepoint.return_value = False

    ge.ui.vol_sfx_btn_rect = mock.MagicMock(pygame.Rect)
    ge.ui.vol_sfx_btn_rect.collidepoint.return_value = False

    ge.ui.back_button_rect = mock.MagicMock(pygame.Rect)
    ge.ui.back_button_rect.collidepoint.return_value = False

    ge.ui.knob_bg_rect = mock.MagicMock(pygame.Rect)
    ge.ui.knob_bg_rect.collidepoint.return_value = False

    ge.ui.knob_sf_rect = mock.MagicMock(pygame.Rect)
    ge.ui.knob_sf_rect.collidepoint.return_value = False

    ge.ui.pad_btn_rect = mock.MagicMock(pygame.Rect)
    ge.ui.pad_btn_rect.collidepoint.return_value = False

    ge.ui.graphics_btn_rect = mock.MagicMock(pygame.Rect)
    ge.ui.graphics_btn_rect.collidepoint.return_value = False

    return ge, mock_pygame


def test_gamestate_splash(starting_ge_main_menu):
    """
    Tests that when the gamestate is SPLASH that the ui is called and the gamestate
    transitions to MENU
    """
    ge, mock_pygame = starting_ge_main_menu
    ge.gs.cur_state = GameState.GameStateName.SPLASH
    ge.app_start_ticks = 1000
    ge.handle_gamestate(None)

    with patch('pygame.time.get_ticks', return_value=1000 + (constants.SPLASH_TIME_SECS + 1) * 1000):
        ge.ui.draw_splash_screen.assert_called_once()
        assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN


@pytest.mark.parametrize("position, theme",[((150, 125), LevelTheme.CLASSIC), ((150, 225), LevelTheme.MODERN)])
def test_gamestate_menu_play_btn(position, theme, starting_ge_main_menu):
    """
    Tests that level theme changes to CLASSIC or MODERN based on position clicked
    Tests mouse is visible
    Tests that ui.draw_start_screen was called
    Tests that reset_game was called
    """
    ge, mock_pygame = starting_ge_main_menu
    ge.ps.theme = LevelTheme.NO_THEME
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=position)

    with patch.object(ge, 'reset_game') as mock_reset_game:
        ge.handle_gamestate([event])
        ge.ui.draw_start_screen.assert_called_once()
        mock_pygame["mouse_set_visible"].assert_called_with(True)
        assert ge.ps.theme == theme
        assert ge.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH
        mock_reset_game.assert_called_once()


def test_gamestate_menu_quit_btn(starting_ge_main_menu):
    """
    Tests quit button is pressed and clean_shutdown is called
    """
    ge, mock_pygame = starting_ge_main_menu
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(150, 725))

    with patch.object(ge, 'clean_shutdown') as mock_clean_shutdown:
        ge.handle_gamestate([event])
        mock_clean_shutdown.assert_called_once()


@pytest.mark.parametrize("position, game_state",[
    ((150, 325), GameState.GameStateName.HOW_TO_PLAY),
    ((150, 425), GameState.GameStateName.SETTINGS),
    ((150, 525), GameState.GameStateName.LEADERBOARD),
    ((150, 625), GameState.GameStateName.CREDITS)])
def test_gamestate_menu_click_remaining_btns(position, game_state, starting_ge_main_menu):
    """
    Tests remaining buttons are clicked: How to play, settings, leaderboard, credits
    """
    ge, mock_pygame = starting_ge_main_menu
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=position)
    ge.handle_gamestate([event])
    assert ge.gs.cur_state == game_state


def test_gamestate_how_to_play(starting_ge):
    """
    Tests that when the game state is HOW_TO_PLAY that ui.draw_how_to_play_screen is called
    Tests that  pygame.mouse_set_visible is called with True
    Tests that the event to click the back button is pressed and the game state is changed the MENU_SCREEN
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.HOW_TO_PLAY
    ge.ui.back_button_rect = pygame.Rect(100, 800, 100, 40)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(150, 825))
    ge.handle_gamestate([event])

    ge.ui.draw_how_to_play_screen.assert_called_once()
    mock_pygame["mouse_set_visible"].assert_called_with(True)
    assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN


def test_gamestate_credits(starting_ge):
    """
    Tests that when the game state is CREDITS that ui.draw_credits_screen is called
    Tests that  pygame.mouse_set_visible is called with True
    Tests that the event to click the back button is pressed and the game state is changed the MENU_SCREEN
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.CREDITS
    ge.ui.back_button_rect = pygame.Rect(100, 800, 100, 40)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(150, 825))
    ge.handle_gamestate([event])

    ge.ui.draw_credits_screen.assert_called_once()
    mock_pygame["mouse_set_visible"].assert_called_with(True)
    assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN


def test_gamestate_leaderboard(starting_ge):
    """
    Tests that when the game state is LEADERBOARD that ui.draw_leaderboard_screen is called
    Tests that  pygame.mouse_set_visible is called with True
    Tests that the event to click the back button is pressed and the game state is changed the MENU_SCREEN
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.LEADERBOARD
    ge.ui.back_button_rect = pygame.Rect(100, 800, 100, 40)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(150, 825))
    ge.handle_gamestate([event])

    ge.ui.draw_leaderboard_screen.assert_called_once()
    mock_pygame["mouse_set_visible"].assert_called_with(True)
    assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN


@pytest.mark.parametrize("starting_auto_state, starting_mouse_state, ending_auto_state, ending_mouse_state",
                         [(True, True, False, False),  # starting paddle is auto, will result in keyboard
                          (True, False, False, True),  # starting paddle is auto, will result in mouse
                          (False, False, True, False), # starting paddle is keyboard, will result in auto
                          (False, True,  True, True), # starting paddle is mouse, will result in auto
                          ])
def test_gamestate_paused_toggle_paddle_control(starting_auto_state, starting_mouse_state, ending_auto_state, ending_mouse_state, starting_ge):
    """
    for auto detection auto_control is T, mouse_control is T or F
    for mouse control, auto_control is F and mouse_control is T
    for keyboard control, auto_control is F and mouse_control is F

    Tests that when the game state is PAUSED, the paddle control button is clicked,
    the ge.draw_world_and_status is called, ge.ui.draw_pause_menu is called
    and that ge.gset.paddle_under_auto_control and ge.gset.paddle_under_mouse_control are set based correctly
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.PAUSED

    with patch.object(ge, 'draw_world_and_status') as mock_draw_world_and_status, patch.object(ge.ui, 'draw_pause_menu') as mock_draw_pause_menu:
        mock_draw_pause_menu.return_value = (1, 2, 3)

        ge.ui.pad_btn_rect = pygame.Rect(200, 100, 100, 50)
        ge.gset.paddle_under_auto_control = starting_auto_state
        ge.gset.paddle_under_mouse_control = starting_mouse_state
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(250, 125))

        ge.handle_gamestate([event])
        mock_draw_world_and_status.assert_called_once()
        mock_draw_pause_menu.assert_called()
        assert ge.gs.cur_state == GameState.GameStateName.PAUSED
        assert ge.gset.paddle_under_auto_control is ending_auto_state
        assert ge.gset.paddle_under_mouse_control is ending_mouse_state


def test_gamestate_highscore(starting_ge):
    """
    Tests that when the game state is GET_HIGH_SCORE that ui.draw_get_high_score is called
    game state is changed the MENU_SCREEN
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.GET_HIGH_SCORE

    with patch.object(ge, 'draw_world_and_status') as mock_draw_world_and_status, patch.object(ge.ui, 'draw_get_high_score') as mock_draw_get_high_score:
        ge.handle_gamestate(None)

        mock_draw_world_and_status.assert_called_once()
        mock_draw_get_high_score.assert_called_once()


def test_gamestate_game_over(starting_ge):
    """
    Tests that when the game state is GAME_OVER that ge.draw_world_and_status is called, ui.draw_game_over_menu is called
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.GAME_OVER

    with patch.object(ge, 'draw_world_and_status') as mock_draw_world_and_status, patch.object(ge.ui, 'draw_game_over_menu') as mock_draw_game_over_menu:
        mock_draw_game_over_menu.return_value = (1, 2, 3)
        ge.handle_gamestate(None)

        mock_draw_world_and_status.assert_called_once()
        mock_draw_game_over_menu.assert_called_once()


@mock.patch("levels.Levels")
def test_gamestate_ready_to_launch_initialization(mock_levels, starting_ge):
    """
    Test GameState READY_TO_LAUNCH, one brick, one paddle, and one ball in world_objects
    Test that mouse position is updated to the last known mouse position
    Test that level is the same
    Test draw_world_and_status was called once
    Test draw_game_intro was called once
    Test mouse_set_visible was called with False
    """
    ge, mock_pygame = starting_ge
    brick = mock.MagicMock(spec=Brick)
    brick.can_react = False
    paddle = mock.MagicMock(spec=Paddle)
    paddle.can_react = False
    ball = mock.MagicMock(spec=Ball)
    ball.can_react = True
    ball.commanded_pos_x = 0
    ball.rect = mock.MagicMock
    ge.gw.world_objects = [paddle, ball, brick]
    ge.gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH
    ge.gs.last_mouse_pos_x = 5
    ge.gs.paddle_pos_x = 10
    ge.ps.level = 1

    with patch.object(ge, 'draw_world_and_status') as mock_draw_world_and_status, \
            patch.object(ge.ui, "draw_game_intro") as mock_ui_draw_game_intro, \
            patch.object(ge, "handle_collisions_between_worldobjects") as mock_handle_collisions:
        ge.handle_gamestate([])
        mock_pygame["mouse_set_visible"].assert_called_with(False)
        assert ge.gs.last_mouse_pos_x == 4
        mock_draw_world_and_status.assert_called_once()
        mock_ui_draw_game_intro.assert_called_once()
        assert ge.ps.level == 1
        assert ball.commanded_pos_x == 10


@mock.patch("levels.Levels")
def test_gamestate_playing(mock_levels, starting_ge):
    """
    Test GameState PLAYING, no bricks and level_cleared == True indicating level is over
    Test draw_world_and_status was called once
    Test draw_game_intro was not called
    Test that last_mouse_pos_x changed to 4
    Test mouse_set_visible was called with False
    Test that level increments by one
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.PLAYING
    ge.gs.level_cleared = True
    ge.gs.last_mouse_pos_x = 5
    ge.ps.level = 1

    with patch.object(ge, 'draw_world_and_status') as mock_draw_world_and_status, patch.object(ge.ui, "draw_game_intro") as mock_ui_draw_game_intro:
        ge.handle_gamestate([])
        mock_pygame["mouse_set_visible"].assert_called_with(False)
        assert ge.gs.last_mouse_pos_x == 4
        mock_draw_world_and_status.assert_called_once()
        mock_ui_draw_game_intro.assert_not_called()
        assert ge.ps.level == 2


@mock.patch("levels.Levels")
def test_gamestate_playing_paddle_mouse_control_changes(mock_levels, starting_ge):
    """
    Test GameState PLAYING, with a paddle in world_objects
    Test that paddle_under_mouse_control changes from False to True whe
    """
    ge, mock_pygame = starting_ge
    ge.gset.paddle_under_mouse_control = False
    ge.gset.paddle_under_auto_control = True
    ge.gs.cur_state = GameState.GameStateName.PLAYING

    ge.handle_gamestate([])
    assert ge.gset.paddle_under_mouse_control


@pytest.mark.parametrize("auto_play, auto_control", [(True, True), (False, True), (False, False)])
@mock.patch("levels.Levels")
def test_gamestate_playing_with_paddle(mock_levels, auto_play, auto_control, starting_ge):
    """
    Test GameState PLAYING, with a paddle in world_objects
    Test auto_play True, the paddle x position changes to the ball x position
    Test auto_play False, auto_control True,  paddle x position changes to pygame.mouse.get_pos and paddle_under_mouse_control is False
    Test auto_play False, auto_control False, paddle x position changes to pygame.mouse.get_pos and paddle_under_mouse_control is True
    """
    ge, mock_pygame = starting_ge
    ge.gset.paddle_under_auto_control = auto_control
    ge.gset.paddle_under_mouse_control = True
    paddle = mock.MagicMock(spec=Paddle)
    paddle.can_react = False
    paddle.commanded_pos_x = 0
    ge.gw.world_objects = [paddle]
    ge.gs.cur_state = GameState.GameStateName.PLAYING
    ge.gs.cur_ball_x = 5
    ge.gs.auto_play = auto_play

    ge.handle_gamestate([])
    if auto_play:
        assert paddle.commanded_pos_x == ge.gs.cur_ball_x
    else:
        assert paddle.commanded_pos_x == 4
        if auto_control:
            assert not ge.gset.paddle_under_mouse_control
        else:
            assert ge.gset.paddle_under_mouse_control


@pytest.mark.parametrize("can_react", [True, False])
@mock.patch("levels.Levels")
def test_gamestate_playing_skip_non_reacting_objects(mock_levels, can_react, starting_ge):
    """
    Test that objects with can_react=False are skipped.
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.PLAYING

    # Set up the mock world objects
    world_object_1 = mock.MagicMock()
    world_object_1.can_react = can_react # set world_object_1 to react
    world_object_2 = mock.MagicMock()
    world_object_2.can_react = False # set
    ge.gw.world_objects = [world_object_1, world_object_2]

    with patch.object(ge, "handle_collisions_between_worldobjects") as mock_handle_collisions:
        ge.handle_gamestate([])

    if can_react:
        mock_handle_collisions.assert_called_with(world_object_1, world_object_2)
    else:
        # Ensure handle_collisions was not called
        mock_handle_collisions.assert_not_called()


@pytest.mark.parametrize("should_remove", [True, False])
@mock.patch("levels.Levels")
def test_gamestate_playing_remove_animation_when_done(mock_levels, should_remove, starting_ge):
    """
    Test that an Animation object is removed if should_remove() returns True.
    """
    ge, mock_pygame = starting_ge
    ge.gs.cur_state = GameState.GameStateName.PLAYING

    # mock animation world object
    animation_wo = mock.MagicMock(spec=Animation)
    animation_wo.should_remove.return_value = should_remove
    animation_wo.can_react = False
    ge.gw.world_objects = [animation_wo]

    # run function being tested
    ge.handle_gamestate([])

    animation_wo.should_remove.assert_called_once()
    if should_remove:
        # Verify the Animation object was removed
        assert animation_wo not in ge.gw.world_objects

    else:
        # Verify the Animation object was not removed
        assert animation_wo in ge.gw.world_objects


def test_handle_collisions_detects_collision(starting_ge):
    """
    Test that the method detects collisions and behaves correctly when allow_collision is True.
    """
    ge, mock_pygame = starting_ge
    current_wo = mock.MagicMock()
    current_wo.__class__ = Ball
    other_wo = mock.MagicMock()

    # Mock collision detection
    current_wo.rect.colliderect.return_value = True
    current_wo.speed = 1
    current_wo.speed_v = 1
    current_wo.v_vel = 1
    current_wo.v_vel_unit = 1
    other_wo.allow_collision.return_value = True
    other_wo.should_score.return_value = True
    other_wo.should_remove.return_value = True
    other_wo.value = 10
    other_wo.bonus = 5
    other_wo.strength_initial = constants.SHAKE_STRENGTH_THRESHOLD + 1
    ge.gw.world_objects = [current_wo, other_wo]

    with patch.object(utils, "start_shake") as mock_shake:
        ge.handle_collisions_between_worldobjects(current_wo, other_wo)

        # Assert collision was detected and methods were called
        current_wo.detect_collision.assert_called_once_with(other_wo, ge.gs, ge.gset)
        other_wo.add_collision.assert_called_once()
        assert ge.ps.score == 15  # Score updated
        other_wo.trigger_destruction_effect.assert_called_once_with(ge.gw.world_objects, ge.gset, ge.ps)

        # Assert shake logic was triggered
        mock_shake.assert_called_once_with(ge.gs, (constants.SHAKE_STRENGTH_THRESHOLD + 1) * constants.SHAKE_OFFSET_BASE)

        # Assert other_wo was removed from world_objects
        assert other_wo not in ge.gw.world_objects

        # Assert ball speed adjustments
        if isinstance(current_wo, Ball):
            assert current_wo.speed == 1.20
            assert current_wo.speed_v == 1 + ge.gs.ball_speed_step
            assert current_wo.v_vel == current_wo.v_vel_unit * current_wo.speed_v


def test_handle_collisions_resets_collision_flag(starting_ge):
    """
    Tests that nothing happens when collisions aren't allowed
    """
    ge, mock_pygame = starting_ge
    current_wo = mock.MagicMock()
    other_wo = mock.MagicMock()
    ge.gw.world_objects = [current_wo, other_wo]

    # Mock no collision
    current_wo.rect.colliderect.return_value = False

    # Call the function
    ge.handle_collisions_between_worldobjects(current_wo, other_wo)

    # Assert prime_for_collision was called
    other_wo.prime_for_collision.assert_called_once()


def test_handle_collisions_no_effect_on_disallowed_collision(starting_ge):
    """
    Test that the method does nothing when allow_collision is False.
    """
    ge, mock_pygame = starting_ge
    current_wo = mock.MagicMock()
    other_wo = mock.MagicMock()
    ge.gw.world_objects = [current_wo, other_wo]

    # Mock collision detection
    current_wo.rect.colliderect.return_value = True
    other_wo.allow_collision.return_value = False

    # Call the function
    ge.handle_collisions_between_worldobjects(current_wo, other_wo)

    # Assert no further calls were made
    current_wo.detect_collision.assert_not_called()
    other_wo.add_collision.assert_not_called()
    other_wo.trigger_destruction_effect.assert_not_called()
    assert other_wo in ge.gw.world_objects


def test_settings_initialization(starting_ge_settings):
    """
    Test GameState is SETTNGS, mouse is visible, draw_settings_screen was called
    """
    ge, mock_pygame = starting_ge_settings

    ge.handle_gamestate([])

    ge.ui.draw_settings_screen.assert_called_once_with(ge.gset)
    mock_pygame["mouse_set_visible"].assert_called_with(True)


@pytest.mark.parametrize('bgm_sound, bgm_volume', [(True, 0.5), (False, 0.0), (False, 0.5)])
def test_settings_toggle_bgm(bgm_sound, bgm_volume, starting_ge_settings):
    """
    Toggles background music off and on
    """
    ge, mock_pygame = starting_ge_settings
    ge.gset.bgm_sounds = bgm_sound
    ge.gset.music_volume = bgm_volume

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.vol_bgm_btn_rect.collidepoint.return_value = True

    ge.handle_gamestate([event])

    if bgm_sound:  # previous had sound, should now be mute
        assert not ge.gset.bgm_sounds
        assert ge.gset.music_volume <= 0
    else:  # was previously mute, now has sound
        assert ge.gset.bgm_sounds
        assert ge.gset.music_volume == constants.MUSIC_VOLUME_STEP

    mock_pygame['mixer.music'].set_volume.assert_called_with(ge.gset.music_volume)
    assert ge.gs.cur_state == GameState.GameStateName.SETTINGS


@pytest.mark.parametrize('sfx_sound, sfx_volume', [(True, 0.5), (False, 0.0), (False, 0.5)])
def test_settings_toggle_sfx(sfx_sound, sfx_volume, starting_ge_settings):
    """
    Toggles sound effects off and on
    """
    ge, mock_pygame = starting_ge_settings
    ge.gset.sfx_sounds = sfx_sound
    ge.gset.sfx_volume = sfx_volume

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.vol_sfx_btn_rect.collidepoint.return_value = True

    ge.handle_gamestate([event])

    if sfx_sound:  # previous had sound effects, should now be mute
        assert not ge.gset.sfx_sounds
        assert ge.gset.sfx_volume <= 0
    else:  # sound effects were previously mute, now have sound
        assert ge.gset.sfx_sounds
        assert ge.gset.sfx_volume == constants.SFX_VOLUME_STEP

    assert ge.gs.cur_state == GameState.GameStateName.SETTINGS


def test_settings_main_menu_btn_clicked(starting_ge_settings):
    """
    Tests the GameState changes to MENU_SCREEN when the back button is clicked
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.back_button_rect.collidepoint.return_value = True

    ge.handle_gamestate([event])

    assert ge.gs.cur_state == GameState.GameStateName.MENU_SCREEN


def test_settings_prep_music_slider(starting_ge_settings):
    """
    get the background music slider ready to be moved
    """
    ge, mock_pygame = starting_ge_settings
    ge.dragging_bgm_slider = False

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.knob_bg_rect.collidepoint.return_value = True

    ge.handle_gamestate([event])

    assert ge.dragging_bgm_slider


def test_settings_prep_sfx_slider(starting_ge_settings):
    """
    get the sfx slider ready to be moved
    """
    ge, mock_pygame = starting_ge_settings
    ge.dragging_sfx_slider = False

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    ge.gset.paddle_under_auto_control = True
    ge.gset.paddle_under_mouse_control = True

    # button being tested
    ge.ui.knob_sf_rect.collidepoint.return_value = True

    ge.handle_gamestate([event])

    assert ge.dragging_sfx_slider


@pytest.mark.parametrize("starting_auto_state, starting_mouse_state, ending_auto_state, ending_mouse_state",
                         [(True, True, False, False),  # starting paddle is auto, will result in keyboard
                          (True, False, False, True),  # starting paddle is auto, will result in mouse
                          (False, False, True, False),  # starting paddle is keyboard, will result in auto
                          (False, True,  True, True),  # starting paddle is mouse, will result in auto
                          ])
def test_settings_paddle_control_toggle(starting_auto_state, starting_mouse_state, ending_auto_state, ending_mouse_state, starting_ge_settings):
    """
    for auto detection auto_control is T, mouse_control is T or F
    for mouse control, auto_control is F and mouse_control is T
    for keyboard control, auto_control is F and mouse_control is F

    Tests that ge.gset.paddle_under_auto_control and ge.gset.paddle_under_mouse_control are set based correctly
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.pad_btn_rect.collidepoint.return_value = True
    ge.gset.paddle_under_auto_control = starting_auto_state
    ge.gset.paddle_under_mouse_control = starting_mouse_state

    ge.handle_gamestate([event])

    assert ge.gs.cur_state == GameState.GameStateName.SETTINGS
    assert ge.gset.paddle_under_auto_control is ending_auto_state
    assert ge.gset.paddle_under_mouse_control is ending_mouse_state


@pytest.mark.parametrize("screen_mode", [True, False])
def test_settings_toggle_fullscreen_windowed(screen_mode, starting_ge_settings):
    """
    Tests that screen size toggles between full and window
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONDOWN

    # button being tested
    ge.ui.graphics_btn_rect.collidepoint.return_value = True
    ge.gset.is_fullscreen = screen_mode

    with patch.object(ge, 'set_graphics_mode') as set_graphics_mode:
        ge.handle_gamestate([event])

        assert ge.gset.is_fullscreen is not screen_mode
        set_graphics_mode.assert_called()
        assert ge.gs.cur_state == GameState.GameStateName.SETTINGS


@pytest.mark.parametrize("old_volume, new_x_position, expected_new_volume",
                         [(0.75, 772, 0.625),
                          (0.875, 856, 0.75),
                          (0.625, 770, 0.625),
                          (1, 1000, 1),
                          (0, 10, 0)])
def test_settings_adjust_music_slider(old_volume, new_x_position, expected_new_volume, starting_ge_settings):
    """
    Tests background music settings are adjusted based on the slider x position
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEMOTION
    event.pos = [new_x_position]

    ge.dragging_bgm_slider = True
    ge.ui.vol_bgm_btn_rect.centerx = 237

    ge.handle_gamestate([event])

    assert ge.gset.music_volume == expected_new_volume
    mock_pygame['mixer.music'].set_volume.assert_called_with(ge.gset.music_volume)
    if expected_new_volume == 0:
        assert not ge.gset.bgm_sounds  # volume is 0, bgm_sound is off
    else:
        assert ge.gset.bgm_sounds  # volume is > 0, bgm_sound is on


@pytest.mark.parametrize("old_volume, new_x_position, expected_new_volume",
                         [(0.75, 772, 0.625),
                          (0.875, 856, 0.75),
                          (0.625, 770, 0.625),
                          (1, 1000, 1),
                          (0, 10, 0)])
def test_settings_adjust_sfx_slider(old_volume, new_x_position, expected_new_volume, starting_ge_settings):
    """
    Tests sound effect settings are adjusted based on the slider x position
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEMOTION
    event.pos = [new_x_position]

    ge.dragging_sfx_slider = True
    ge.ui.vol_sfx_btn_rect.centerx = 237

    ge.handle_gamestate([event])

    assert ge.gset.sfx_volume == expected_new_volume
    if expected_new_volume == 0:
        assert not ge.gset.sfx_sounds  # volume is 0, bgm_sound is off
    else:
        assert ge.gset.sfx_sounds  # volume is > 0, bgm_sound is on


def test_settings_reset_slider_checks(starting_ge_settings):
    """
    Tests sliders are set to falase on MOUSEBUTTONUP
    """
    ge, mock_pygame = starting_ge_settings

    event = mock.MagicMock()
    event.type = pygame.MOUSEBUTTONUP

    ge.dragging_bgm_slider = True
    ge.dragging_sfx_slider = True

    ge.handle_gamestate([event])

    assert not ge.dragging_bgm_slider
    assert not ge.dragging_sfx_slider






