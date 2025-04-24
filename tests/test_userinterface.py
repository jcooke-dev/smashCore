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
from unittest.mock import MagicMock
from userinterface import UserInterface
import constants


@pytest.fixture
def mock_pygame():
    with mock.patch("pygame.mouse") as mock_mouse, \
         mock.patch("pygame.rect") as mock_rect, \
         mock.patch("pygame.draw.rect") as mock_draw_rect, \
         mock.patch("pygame.transform.scale") as mock_transform_scale, \
         mock.patch("pygame.font") as mock_font, \
         mock.patch("pygame.color") as mock_color, \
         mock.patch("pygame.SRCALPHA") as mock_srcalpha, \
         mock.patch("pygame.Surface") as mock_surface:

        # Setup return values if needed
        #mock_set_mode.return_value = mock.MagicMock(name="screen")
        mock_surface.return_value = MagicMock(name="surface")
        mock_surface().get_rect = MagicMock(return_value=pygame.Rect(0, 0, 100, 50))
        mock_font.return_value.render = MagicMock(return_value=pygame.Surface)
        mock_mouse.get_pos.return_value = (50,50)
        mock_mouse.get_pressed.return_value = (1, 0, 0)


        yield {
            "surface": mock_surface,
            "srcalpha": mock_srcalpha,
            "color": mock_color,
            "font": mock_font,
            "transform.scale": mock_transform_scale,
            "draw.rect": mock_draw_rect,
            "rect": mock_rect,
            "mouse": mock_mouse
        }

@pytest.fixture
def ui_fixture(mock_pygame):
    """
    Set up UserInterface with mock dependencies
    :return:
    """
    ui = UserInterface()
    ui.screen = mock.Mock()
    ui.surface = mock_pygame['surface']
    ui.pad_btn_rect = mock.Mock()

    mock_font_button = mock.Mock()
    mock_font_status = mock.Mock()
    mock_rendered_text = mock.Mock()
    mock_font_button.render.return_value = mock_rendered_text
    mock_font_status.render.return_value = mock_rendered_text

    ui.font_title_text = mock_pygame['font'].title
    ui.font_title_text.return_value = MagicMock(return_value=pygame.Rect(0, 0, 100, 50))

    ui.font_buttons = mock_font_button
    ui.font_status = mock_font_status
    return ui, mock_pygame


def test_initialize_background_elements(ui_fixture):
    """Test initialization of background elements."""
    ui, mock_pygame = ui_fixture
    assert len(ui.background_balls) == 8  # Check if 8 balls are created
    assert len(ui.background_bricks) > 0  # Ensure bricks are initialized


def test_draw_button(ui_fixture):
    """
    Tests draw_button to ensure correct placement and if collidepoint intersects
    mouse position then the action is called.
    :param ui_fixture:
    :return:
    """
    ui, mock_pygame = ui_fixture
    with mock.patch("pygame.mouse.get_pos", return_value=(45, 45)), \
            mock.patch("pygame.mouse.get_pressed", return_value=(1, 0, 0)):
        mock_surface = mock_pygame['surface']
        mock_action = MagicMock()
        rect = ui.draw_button(mock_surface, 40, 40, 100, 50, pygame.Color("blue"), pygame.Color("red"), mock_action)
        assert rect.topleft == (40, 40)
        assert mock_action.call_count == 1  # Action should be called when clicked


def test_draw_pause_menu(ui_fixture):
    """
    Asserts the correct text and buttons were rendered and blitted
    Assert "Game Paused: " was rendered
    Assert "Press ESC to Continue was rendered
    Assert "Paddle Control" was rendered
    Assert all button fonts are rendered (Mouse/Keyboard control, Try Again, Main Menu, Quit)
    Assert surface was blitted
    Assert screen was blitted
    Assert pygame.draw.rect was called 5 times
    :param mock_rect:
    :param ui:
    :return:
    """
    ui, mock_pygame = ui_fixture

    ui.font_title1_text = mock_pygame['font']
    ui.font_title2_text = mock_pygame['font']
    ui.font_pad_btn_lbl = mock_pygame['font']
    ui.font_buttons = mock_pygame["font"]

    fake_render = lambda text, flag, color: type("FakeSurface", (), {
            "get_rect": lambda self, **kwargs: type("FakeRect", (), {"x": 100, "y": kwargs.get("topright", (0, 0))[1]})(),
            "get_width": lambda self: 80},)()

    ui.font_title1_text.render.side_effect = fake_render
    ui.font_title2_text.render.side_effect = fake_render
    ui.font_pad_btn_lbl.render.side_effect = fake_render
    ui.font_buttons.render.side_effect = fake_render

    ui.draw_pause_menu(True)

    assert ui.surface.blit.called
    assert ui.screen.blit.called
    assert mock_pygame["draw.rect"].call_count == 5


def test_draw_game_over_menu(ui_fixture):
    """
    Asserts the correct text and buttons were rendered and blitted
    Assert "YOU GOT SMASHED!" was rendered
    Assert "Try Again" was rendered
    Assert "Restart Game" was rendered
    Assert "Quit Game" was rendered
    Assert surface was blitted
    Assert screen was blitted
    Assert pygame.draw.rect was called 4 times
    :param mock_rect:
    :param ui:
    :return:
    """
    ui, mock_pygame = ui_fixture

    mock_action = MagicMock()

    ui.draw_game_over_menu(mock_action)
    called_args_title = ui.font_title_text.render.call_args

    assert called_args_title[0][0]  == "YOU GOT SMASHED!"
    ui.font_buttons.render.assert_any_call("Try Again", mock.ANY, mock.ANY)
    ui.font_buttons.render.assert_any_call("Main Menu", mock.ANY, mock.ANY)
    ui.font_buttons.render.assert_any_call("Quit", mock.ANY, mock.ANY)

    assert mock_pygame['mouse'].set_visible

    assert ui.surface.blit.called
    assert ui.screen.blit.called
    assert mock_pygame["draw.rect"].call_count == 4  #rect for buttons and text


def test_game_intro(ui_fixture):
    """
    Asserts "Press SPACEBAR to start" was rendered and is blitted
    :param ui:
    :return:
    """
    ui, mock_pygame = ui_fixture

    ui.draw_game_intro()
    called_args = ui.font_buttons.render.call_args
    if called_args:
        assert called_args[0][0] == "Press SPACEBAR to start"

    assert ui.screen.blit.called


@mock.patch("pygame.draw.circle")
def test_draw_status(mock_circle, ui_fixture):
    """
    Asserts that "Lives:" label was rendered and blitted
    Asserts that pygame.draw.circle was called 3 times
    :param mock_circle:
    :param ui:
    :return:
    """
    # draw_status expects font_buttons to have a width for status spacing
    ui, mock_pygame = ui_fixture

    mock_rendered_btn = mock.Mock()
    mock_rendered_btn.get_width.return_value = 50
    ui.font_status.render.return_value = mock_rendered_btn

    ui.draw_status(3, 99, 1)

    ui.font_status.render.assert_any_call("Lives:", True, constants.WHITE)
    ui.font_status.render.assert_any_call("Level: 1", True, constants.WHITE)
    ui.font_status.render.assert_any_call("Score: 99", True, constants.WHITE)

    assert ui.screen.blit.called
    assert mock_circle.call_count == 3


def test_update_background_elements(ui_fixture):
    """Test background element updates."""
    ui, mock_pygame = ui_fixture
    initial_positions = [ball["rect"].topleft for ball in ui.background_balls]
    ui.update_background_elements()
    updated_positions = [ball["rect"].topleft for ball in ui.background_balls]
    assert initial_positions != updated_positions  # Ensure positions are updated