"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This handles persisting and reading back various game/player data/objects to/from disk
"""

import os.path
import pickle
import platform

import constants

# paths to serialized files
GAME_DATA_PATH: str = None # holds the proper OS-dependent user settings dir
APP_DATA_PATH_WINDOWS: str = 'AppData\\Local\\'
LEADERBOARD_FILENAME: str = 'leaderboard.pkl'


def find_game_data_path():
    """
    Finds the user profile path for the main operating systems targeted (windows, mac, linux)
    otherwise uses a default directory SMASHCORE_settings

    :return:
    """
    global GAME_DATA_PATH

    op_sys: str = platform.system()
    user_profile_path: str = os.path.expanduser('~')

    # OS determines best appData path to game settings
    if 'windows' in op_sys.lower():
        GAME_DATA_PATH = os.path.join(user_profile_path, APP_DATA_PATH_WINDOWS, constants.GAME_NAME)
    elif 'darwin' in op_sys.lower(): # macOS
        GAME_DATA_PATH = os.path.join(user_profile_path, '.' + constants.GAME_NAME)
    elif 'linux' in op_sys.lower():
        GAME_DATA_PATH = os.path.join(user_profile_path, '.' + constants.GAME_NAME)
    else:
        # default to a game-named settings dir in the working directory
        GAME_DATA_PATH = os.path.join(constants.GAME_NAME + '_settings/')


def store_object(obj: object, filename: str):
    """
    Store serialized object using pickle

    :param obj: the object to store
    :param filename: the filename to store object to
    :return:
    """

    if GAME_DATA_PATH is None:
        find_game_data_path()

    path = os.path.join(GAME_DATA_PATH, filename)

    os.makedirs(GAME_DATA_PATH, exist_ok=True)
    with open(path, 'wb') as fileOut:
        pickle.dump(obj, fileOut)


def read_object(filename: str):
    """
    Load serialized file using pickle for reading
    :param filename: name of the file to read
    :return:
    """

    if GAME_DATA_PATH is None:
        find_game_data_path()

    path = os.path.join(GAME_DATA_PATH, filename)

    try:
        if os.path.getsize(path) > 0:
            with open(path, 'rb') as fileIn:
                if fileIn is not None:
                    obj = pickle.load(fileIn)
                    return obj

    except FileNotFoundError:
        pass
