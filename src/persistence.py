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
GAME_DATA_PATH: str = None
APP_DATA_PATH_WINDOWS: str = 'AppData\\Local\\'
# APP_DATA_PATH_MAC = 'AppData\\Local\\'
# APP_DATA_PATH_LINUX = 'AppData\\Local\\'
LEADERBOARD_FILENAME: str = 'leaderboard.pkl'


def find_game_data_path():
    global GAME_DATA_PATH
    # GAME_DATA_PATH = 'settings/'

    print(platform.platform())
    print(platform.system())
    print(os.path.expanduser('~'))

    op_sys: str = platform.system()
    user_profile_path: str = os.path.expanduser('~') #os.environ['USERPROFILE']

    # OS determines best appData path to game settings
    if 'windows' in op_sys.lower():
        GAME_DATA_PATH = os.path.join(user_profile_path, APP_DATA_PATH_WINDOWS, constants.GAME_NAME)
    elif 'darwin' in op_sys.lower(): # macOS
        # GAME_DATA_PATH = os.path.join(user_profile_path, APP_DATA_PATH_MAC, constants.GAME_NAME)
        GAME_DATA_PATH = os.path.join(user_profile_path, '.' + constants.GAME_NAME)
    elif 'linux' in op_sys.lower():
        # GAME_DATA_PATH = os.path.join(user_profile_path, APP_DATA_PATH_LINUX, constants.GAME_NAME)
        GAME_DATA_PATH = os.path.join(user_profile_path, '.' + constants.GAME_NAME)
    else:
        # default to a game-named settings dir in the working directory
        GAME_DATA_PATH = os.path.join(constants.GAME_NAME + '_settings/')

    print(GAME_DATA_PATH)



def store_object(obj: object, filename: str):

    if GAME_DATA_PATH is None:
        find_game_data_path()

    path = os.path.join(GAME_DATA_PATH, filename)

    os.makedirs(GAME_DATA_PATH, exist_ok=True)
    with open(path, 'wb') as fileOut:
        pickle.dump(obj, fileOut)

def read_object(filename: str):

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
