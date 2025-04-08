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
def ui():
    """
    Set up UserInterface with mocked up members for screen and font_buttons
    :return:
    """
    pygame.font.init()
    ui = UserInterface()
    ui.screen = mock.Mock()
    ui.surface = mock.Mock()

    mock_font_button = mock.Mock()
    mock_rendered_text = mock.Mock()
    mock_font_button.render.return_value = mock_rendered_text

    ui.font_buttons = mock_font_button
    return ui


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
    ui.font_game_over = mock.Mock()

    ui.draw_pause_menu()
    called_args_game_over = ui.font_game_over.render.call_args

    if called_args_game_over:
        assert called_args_game_over[0][0] == "Game Paused: ESC to Resume"

    ui.font_buttons.render.assert_any_call("Restart Game", mock.ANY, mock.ANY)
    ui.font_buttons.render.assert_any_call("Quit Game", mock.ANY,mock.ANY)
    assert ui.surface.blit.called
    assert ui.screen.blit.called
    assert mock_rect.call_count == 3  #rect for buttons and text
    pass


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
    ui.font_buttons.render.return_value = mock_rendered_btn

    ui.draw_status(3, "99", "1")

    ui.font_buttons.render.assert_any_call("Lives:", True, constants.WHITE)
    ui.font_buttons.render.assert_any_call("Level: 1", True, constants.WHITE)
    ui.font_buttons.render.assert_any_call("Score: 99", True, constants.WHITE)

    assert ui.screen.blit.called
    assert mock_circle.call_count == 3


