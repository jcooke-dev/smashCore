import pytest
from unittest.mock import patch, MagicMock
import main


@patch("main.pygame.init")
@patch("main.assets.load_assets")
@patch("main.UserInterface")
@patch("main.GameSettings.create_persisted_object")
@patch("main.GameState")
@patch("main.GameWorld")
@patch("main.PlayerState")
@patch("main.Leaderboard.create_persisted_object")
@patch("main.GameEngine")
def test_main(mock_gameengine, mock_leaderboard, mock_playerstate,
              mock_gameworld, mock_gamestate, mock_gamesettings,
              mock_userinterface, mock_load_assets, mock_pygame_init,
              ):
    """
    Tests that all dependent objects are instantiated.
    Test that assets are loaded
    Test that gameengine loop is called once
    :param mock_gameengine:
    :param mock_leaderboard:
    :param mock_playerstate:
    :param mock_gameworld:
    :param mock_gamestate:
    :param mock_gamesettings:
    :param mock_userinterface:
    :param mock_load_assets:
    :param mock_pygame_init:
    :return:
    """
    mock_gameengine_instance = MagicMock()
    mock_gameengine.return_value = mock_gameengine_instance

    # Run the main function
    main.main()

    # Assert pygame.init() is called
    mock_pygame_init.assert_called_once()

    # Assert assets.load_assets() is called
    mock_load_assets.assert_called_once()

    # Assert UserInterface, GameSettings, GameState, GameWorld, PlayerState, Leaderboard are instantiated
    mock_userinterface.assert_called_once()
    mock_gamesettings.assert_called_once()
    mock_gamestate.assert_called_once()
    mock_gameworld.assert_called_once()
    mock_playerstate.assert_called_once()
    mock_leaderboard.assert_called_once()

    # Assert GameEngine is initialized with the correct arguments
    mock_gameengine.assert_called_once_with(
        mock_leaderboard.return_value,
        mock_playerstate.return_value,
        mock_gameworld.return_value,
        mock_gamestate.return_value,
        mock_gamesettings.return_value,
        mock_userinterface.return_value,
    )

    # Assert ge.run_loop() is called
    mock_gameengine_instance.run_loop.assert_called_once()
