"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This module defines and loads the various art and sound assets.
"""

import os
import sys
import pygame
from gamestate import GameState


def asset_path(directory, filename):
    """
    Handles creating paths to assets depending on how application is run (from installation or from pycharm)
    :param directory:
    :param filename:
    :return:
    """
    try:
        # PyInstaller creates a temp directory inside the onefile executable
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, directory, filename)


ART_DIR: str = 'assets/art/'
SOUND_DIR: str = 'assets/sound/'

SPLASH_MUSIC_FILENAME: str = 'splash_music.wav'
MENU_MUSIC_FILENAME: str = 'menu_music.wav'
GAME_MUSIC_FILENAME: str = 'game_music.wav'
GAME_OVER_MUSIC_FILENAME: str = 'game_over_music.wav'
SCORE_MUSIC_FILENAME: str = 'score_music.wav'

BACKGROUND_FILENAME: str = 'background.png'
BRK_YELLOW_FILENAME: str = 'yellow_brick.png'
BRK_BLUE_FILENAME: str = 'blue_brick.png'
BRK_GREEN_FILENAME: str = 'green_brick.png'
BRK_RED_FILENAME: str = 'red_brick.png'
BRK_PINK_FILENAME: str = 'pink_brick.png'
BRK_ORANGE_FILENAME: str = 'orange_brick.png'
BRK_LTBLUE_FILENAME: str = 'lt_blue_brick.png'
BRK_PURPLE_FILENAME: str = 'purple_brick.png'
BRK_TEAL_FILENAME: str = 'teal_brick.png'
BRK_LAVENDER_FILENAME: str = 'lavender_brick.png'
BRK_GOLD_FILENAME: str = 'gold_brick.png'
BALL_FILENAME: str = 'ball.png'
PADDLE_FILENAME: str = 'paddle.png'

BACKGROUND_IMG, BALL_IMG, PADDLE_IMG = None, None, None
BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG = None, None, None
BRK_RED_IMG, BRK_PINK_IMG, BRK_ORANGE_IMG, = None, None, None
BRK_LTBLUE_IMG, BRK_PURPLE_IMG, BRK_TEAL_IMG = None, None, None
BRK_LAVENDER_IMG, BRK_GOLD_IMG = None, None
BRICK_COLORS = []

MUSIC_PATHS = {}


def load_assets():
    """
    Lazy load the assets
    :return:
    """
    global BACKGROUND_IMG, BALL_IMG, PADDLE_IMG
    global BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG, BRK_RED_IMG
    global BRK_PINK_IMG, BRK_ORANGE_IMG, BRK_LTBLUE_IMG, BRK_PURPLE_IMG
    global BRK_TEAL_IMG, BRK_LAVENDER_IMG, BRK_GOLD_IMG, BRICK_COLORS
    global MUSIC_PATHS

    BACKGROUND_IMG = pygame.image.load(asset_path(ART_DIR, BACKGROUND_FILENAME))
    BRK_YELLOW_IMG = pygame.image.load(asset_path(ART_DIR, BRK_YELLOW_FILENAME))
    BRK_BLUE_IMG = pygame.image.load(asset_path(ART_DIR, BRK_BLUE_FILENAME))
    BRK_GREEN_IMG = pygame.image.load(asset_path(ART_DIR, BRK_GREEN_FILENAME))
    BRK_RED_IMG = pygame.image.load(asset_path(ART_DIR, BRK_RED_FILENAME))
    BRK_PINK_IMG = pygame.image.load(asset_path(ART_DIR, BRK_PINK_FILENAME))
    BRK_ORANGE_IMG = pygame.image.load(asset_path(ART_DIR, BRK_ORANGE_FILENAME))
    BRK_LTBLUE_IMG = pygame.image.load(asset_path(ART_DIR, BRK_LTBLUE_FILENAME))
    BRK_PURPLE_IMG = pygame.image.load(asset_path(ART_DIR, BRK_PURPLE_FILENAME))
    BRK_TEAL_IMG = pygame.image.load(asset_path(ART_DIR, BRK_TEAL_FILENAME))
    BRK_LAVENDER_IMG = pygame.image.load(asset_path(ART_DIR, BRK_LAVENDER_FILENAME))
    BRK_GOLD_IMG = pygame.image.load(asset_path(ART_DIR, BRK_GOLD_FILENAME))  # do not put in array of BRICK_COLORS
    BALL_IMG = pygame.image.load(asset_path(ART_DIR, BALL_FILENAME))
    PADDLE_IMG = pygame.image.load(asset_path(ART_DIR, PADDLE_FILENAME))

    BRICK_COLORS = [BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG, BRK_RED_IMG, BRK_PINK_IMG, BRK_ORANGE_IMG,
                    BRK_LTBLUE_IMG, BRK_PURPLE_IMG, BRK_TEAL_IMG, BRK_LAVENDER_IMG]

    # music
    MUSIC_PATHS[GameState.GameStateName.SPLASH] = asset_path(SOUND_DIR, SPLASH_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.MENU_SCREEN] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.HOW_TO_PLAY] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.CREDITS] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.LEADERBOARD] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.PLAYING] = asset_path(SOUND_DIR, GAME_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.GAME_OVER] = asset_path(SOUND_DIR, GAME_OVER_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.GET_HIGH_SCORE] = asset_path(SOUND_DIR, SCORE_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.READY_TO_LAUNCH] = asset_path(SOUND_DIR, GAME_MUSIC_FILENAME)
