"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Consolidate all game settings into a single class.
"""

import constants
import persistence


class GameSettings:
    """ This maintains the current game settings """

    def __init__(self) -> None:

        self.is_fullscreen: bool = False

        self.paddle_under_auto_control: bool = True
        self.paddle_under_mouse_control: bool = True

        self.bgm_sounds: bool = True
        self.sfx_sounds: bool = True
        self.music_volume = constants.MUSIC_VOLUME_INITIAL
        self.sfx_volume = constants.SFX_VOLUME_INITIAL

    @classmethod
    def create_persisted_object(cls):
        """
        Creates a GameSettings object from file, if exists, else default
        :return:
        """
        gset = cls.load(persistence.SETTINGS_FILENAME)
        if gset is None:
            gset = GameSettings()
        return gset

    @classmethod
    def load(cls, filename: str):
        """
        Loads GameSettings from file
        :param filename:
        :return:
        """
        return persistence.read_object(filename)

    def store(self, filename: str):
        """
        Stores GameSettings in file
        :param filename:
        :return:
        """
        persistence.store_object(self, filename)