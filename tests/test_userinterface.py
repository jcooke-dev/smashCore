"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the UserInterface class.
"""

import pytest
import pygame
from unittest import mock
from userinterface import UserInterface
import constants


@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.mouse") as mock_mouse, \
         mock.patch("pygame.rect") as mock_rect, \
         mock.patch("pygame.draw.rect") as mock_draw_rect, \
         mock.patch("pygame.color") as mock_color, \
         mock.patch("pygame.Surface") as mock_surface:

        # Setup return values if needed
        #mock_set_mode.return_value = mock.MagicMock(name="screen")
        #mock_surface.return_value = mock.MagicMock(name="surface")
        #mock_clock.return_value = mock.MagicMock(name="clock")

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
def ui():
    """
    Set up UserInterface with mocked up members for screen and font_buttons
    :return:
    """
    pygame.init()
    pygame.font.init()

    with mock.patch(
        "userinterface.pygame.transform.scale") as mock_scaled_image:
        ui = UserInterface()
        ui.screen = mock.Mock()
        ui.surface = mock.Mock()

        mock_font_button = mock.Mock()
        mock_font_status = mock.Mock()
        mock_rendered_text = mock.Mock()
        mock_font_button.render.return_value = mock_rendered_text
        mock_font_status.render.return_value = mock_rendered_text

        ui.font_buttons = mock_font_button
        ui.font_status = mock_font_status
        yield ui
    pygame.quit()


@pytest.fixture
def ui():
    """Fixture to create a UserInterface instance with mocked pygame dependencies."""
    with patch("pygame.font.Font") as MockFont, patch("pygame.Surface") as MockSurface:
        MockFont.return_value.render = Mock(return_value=MockSurface())
        MockSurface().get_rect = Mock(return_value=pygame.Rect(0, 0, 100, 50))
        ui = UserInterface()
        ui.surface = MockSurface()
        ui.screen = MockSurface()
        return ui


def test_draw_button(ui):
    """Test the draw_button method."""
    with patch("pygame.mouse.get_pos", return_value=(50, 50)), \
         patch("pygame.mouse.get_pressed", return_value=(1, 0, 0)):
        mock_action = Mock()
        rect = ui.draw_button(Mock(), 40, 40, 100, 50, pygame.Color("blue"), pygame.Color("red"), mock_action)
        assert rect.topleft == (40, 40)
        assert mock_action.call_count == 1  # Action should be called when clicked


def test_initialize_background_elements(ui):
    """Test initialization of background elements."""
    ui.initialize_background_elements()
    assert len(ui.background_balls) == 8  # Check if 8 balls are created
    assert len(ui.background_bricks) > 0  # Ensure bricks are initialized


def test_draw_pause_menu(ui):
    """Test rendering of the pause menu."""
    with patch("pygame.draw.rect"), patch("pygame.Surface.blit"):
        restart_rect, main_menu_rect, quit_rect = ui.draw_pause_menu()
        assert isinstance(restart_rect, pygame.Rect)
        assert isinstance(main_menu_rect, pygame.Rect)
        assert isinstance(quit_rect, pygame.Rect)


def test_update_background_elements(ui):
    """Test background element updates."""
    ui.initialize_background_elements()
    initial_positions = [ball["rect"].topleft for ball in ui.background_balls]
    ui.update_background_elements()
    updated_positions = [ball["rect"].topleft for ball in ui.background_balls]
    assert initial_positions != updated_positions  # Ensure positions are updated


def test_draw_status(ui):
    """Test status rendering."""
    with patch("pygame.Surface.blit"):
        ui.draw_status(lives=3, score=100, level=2)
        # Check if rendering occurs without exceptions


def test_draw_game_intro(ui):
    """Test game intro rendering."""
    with patch("pygame.Surface.blit"):
        ui.draw_game_intro()
        # Check if rendering occurs without exceptions

@mock.patch("pygame.draw.rect")
def test_draw_pause_menu(mock_rect, ui):
    """
    Asserts the correct text and buttons were rendered and blitted
    Assert "Game Paused: ESC to Resume" was rendered
    Assert "Restart Game" was rendered
    Assert "Quit Game" was rendered
    Assert surface was blitted
    Assert screen was blitted
    Assert pygame.draw.rect was called 3 times
    :param mock_rect:
    :param ui:
    :return:
    """
    ui.font_title1_text = mock.Mock()
    ui.font_title2_text = mock.Mock()

    ui.draw_pause_menu()
    called_args_title1 = ui.font_title1_text.render.call_args
    called_args_title2 = ui.font_title2_text.render.call_args

    if called_args_title1:
        assert called_args_title1[0][0] == "Game Paused:"
    if called_args_title2:
        assert called_args_title2[0][0] == "Press ESC to Resume"

    ui.font_buttons.render.assert_any_call("Restart", mock.ANY, mock.ANY)
    ui.font_buttons.render.assert_any_call("Main Menu", mock.ANY, mock.ANY)
    ui.font_buttons.render.assert_any_call("Quit", mock.ANY,mock.ANY)
    assert ui.surface.blit.called
    assert ui.screen.blit.called
    assert mock_rect.call_count == 4  #rect for buttons and text


def test_game_intro(ui):
    """
    Asserts "Press SPACEBAR to start" was rendered and is blitted
    :param ui:
    :return:
    """
    ui.draw_game_intro()
    called_args = ui.font_buttons.render.call_args
    if called_args:
        assert called_args[0][0] == "Press SPACEBAR to start"

    assert ui.screen.blit.called


@mock.patch("pygame.draw.circle")
def test_draw_status(mock_circle, ui):
    """
    Asserts that "Lives:" label was rendered and blitted
    Asserts that pygame.draw.circle was called 3 times
    :param mock_circle:
    :param ui:
    :return:
    """
    # draw_status expects font_buttons to have a width for status spacing
    mock_rendered_btn = mock.Mock()
    mock_rendered_btn.get_width.return_value = 50
    ui.font_status.render.return_value = mock_rendered_btn

    ui.draw_status(3, 99, 1)

    ui.font_status.render.assert_any_call("Lives:", True, constants.WHITE)
    ui.font_status.render.assert_any_call("Level: 1", True, constants.WHITE)
    ui.font_status.render.assert_any_call("Score: 99", True, constants.WHITE)

    assert ui.screen.blit.called
    assert mock_circle.call_count == 3


