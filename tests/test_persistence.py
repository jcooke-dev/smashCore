import pickle
import os
import persistence
from unittest.mock import mock_open, patch
from constants import GAME_NAME


@patch('platform.system', return_value='Windows')
@patch('os.path.expanduser', return_value='C:\\Users\\test_user')
def test_find_game_data_path_windows(mock_os_path_expanduser, mock_platform_system):
    persistence.find_game_data_path()
    assert persistence.GAME_DATA_PATH == os.path.join('C:\\Users\\test_user', persistence.APP_DATA_PATH_WINDOWS, GAME_NAME)


@patch('platform.system', return_value='Darwin')
@patch('os.path.expanduser', return_value='/Users/test_user')
def test_find_game_data_path_mac(mock_os_path_expanduser, mock_platform_system):
    persistence.find_game_data_path()
    assert persistence.GAME_DATA_PATH == os.path.join('/Users/test_user', '.' + GAME_NAME)


@patch('platform.system', return_value='Linux')
@patch('os.path.expanduser', return_value='/home/test_user')
def test_find_game_data_path_linux(mock_os_path_expanduser, mock_platform_system):
    persistence.find_game_data_path()
    assert persistence.GAME_DATA_PATH == os.path.join('/home/test_user', '.' + GAME_NAME)


@patch('platform.system', return_value='Unknown')
def test_find_game_data_path_default(mock_platform_system):
    persistence.find_game_data_path()
    assert persistence.GAME_DATA_PATH == os.path.join(GAME_NAME + '_settings/')


def mock_find_path_side_effect():
    persistence.GAME_DATA_PATH = "some/file/path"

@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
@patch('pickle.dump')
def test_store_object(mock_pickle, mock_file, mock_os_makedirs):
    test_object = {"key": "value"}
    filename = "test.pkl"
    p = persistence
    p.GAME_DATA_PATH = None
    with patch.object(p, "find_game_data_path", side_effect=mock_find_path_side_effect) as mock_find_path:
        p.store_object(test_object, filename)
        mock_file.assert_called_once_with(os.path.join(persistence.GAME_DATA_PATH, filename), 'wb')
        mock_pickle.assert_called_once_with(test_object, mock_file())
        mock_find_path.assert_called_once()


def test_read_object_success():
    test_object = {"key": "value"}
    filename = "test.pkl"
    p = persistence
    p.GAME_DATA_PATH = None
    with patch.object(p, "find_game_data_path", side_effect=mock_find_path_side_effect) as mock_find_path, \
            patch('builtins.open', mock_open(read_data=pickle.dumps(test_object))) as mocked_file, \
            patch('os.path.getsize', return_value=10):
        result = persistence.read_object(filename)
        mocked_file.assert_called_once_with(os.path.join(persistence.GAME_DATA_PATH, filename), 'rb')
        assert result == test_object
        mock_find_path.assert_called_once()


@patch('os.path.getsize', side_effect=FileNotFoundError)
def test_read_object_file_not_found(mock_os_path_getsize):
    filename = "nonexistent.pkl"
    result = persistence.read_object(filename)
    assert result is None