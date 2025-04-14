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

# paths to serialized files
GAME_DATA_PATH = 'settings/'
LEADERBOARD_FILE_PATH = os.path.join(GAME_DATA_PATH, 'leaderboard.pkl')


def store_object(obj: object, path: str):

    os.makedirs(GAME_DATA_PATH, exist_ok=True)
    with open(path, 'wb') as fileOut:
        pickle.dump(obj, fileOut)

def read_object(path: str):

    try:
        if os.path.getsize(path) > 0:
            with open(path, 'rb') as fileIn:
                if fileIn is not None:
                    obj = pickle.load(fileIn)
                    return obj

    except FileNotFoundError:
        pass
