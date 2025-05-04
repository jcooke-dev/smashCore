"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas
    Module Description: This is the test harness for testing the GameSettings.
"""

import pytest
from unittest.mock import patch, MagicMock
from gamesettings import GameSettings
import persistence
import constants

# Mock constants for testing
constants.MUSIC_VOLUME_INITIAL = 50
constants.SFX_VOLUME_INITIAL = 50


@pytest.fixture
def game_settings():
    return GameSettings()


def test_initial_values(game_settings):
    assert game_settings.is_fullscreen is False
    assert game_settings.paddle_under_auto_control is True
    assert game_settings.paddle_under_mouse_control is True
    assert game_settings.bgm_sounds is True
    assert game_settings.sfx_sounds is True
    assert game_settings.music_volume == constants.MUSIC_VOLUME_INITIAL
    assert game_settings.sfx_volume == constants.SFX_VOLUME_INITIAL


@patch("persistence.read_object")
def test_create_persisted_object_from_file(mock_read_object):
    mock_read_object.return_value = MagicMock()
    game_settings = GameSettings.create_persisted_object()
    assert game_settings == mock_read_object.return_value
    mock_read_object.assert_called_once_with(persistence.SETTINGS_FILENAME)


@patch("persistence.read_object")
def test_create_persisted_object_default(mock_read_object):
    mock_read_object.return_value = None
    game_settings = GameSettings.create_persisted_object()
    assert isinstance(game_settings, GameSettings)
    mock_read_object.assert_called_once_with(persistence.SETTINGS_FILENAME)


@patch("persistence.read_object")
def test_load_game_settings(mock_read_object):
    mock_read_object.return_value = MagicMock()
    result = GameSettings.load("dummy_filename")
    assert result == mock_read_object.return_value
    mock_read_object.assert_called_once_with("dummy_filename")


@patch("persistence.store_object")
def test_store_game_settings(mock_store_object, game_settings):
    game_settings.store("dummy_filename")
    mock_store_object.assert_called_once_with(game_settings, "dummy_filename")
