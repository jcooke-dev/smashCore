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
FONT_DIR: str = 'assets/fonts/'

SPLASH_MUSIC_FILENAME: str = 'splash_music.wav'
MENU_MUSIC_FILENAME: str = 'menu_music.wav'
GAME_MUSIC_FILENAME: str = 'game_music.mp3'
GAME_OVER_MUSIC_FILENAME: str = 'game_over_music.wav'
SCORE_MUSIC_FILENAME: str = 'score_music.wav'
BRICK_SFX_FILENAME: str = 'brick.wav'
PADDLE_SFX_FILENAME: str = 'paddle.wav'
LEFT_WALL_SFX_FILENAME: str = 'left_wall.wav'
RIGHT_WALL_SFX_FILENAME: str = 'right_wall.wav'
TOP_WALL_SFX_FILENAME: str = 'top_wall.wav'

BACKGROUND_FILENAME: str = 'background.png'
BRK_YELLOW_FILENAME: str = 'yellow_brick_hd.png'
BRK_BLUE_FILENAME: str = 'blue_brick_hd.png'
BRK_GREEN_FILENAME: str = 'green_brick_hd.png'
BRK_RED_FILENAME: str = 'red_brick_hd.png'
BRK_PINK_FILENAME: str = 'pink_brick_hd.png'
BRK_ORANGE_FILENAME: str = 'orange_brick_hd.png'
BRK_LTBLUE_FILENAME: str = 'lt_blue_brick_hd.png'
BRK_PURPLE_FILENAME: str = 'purple_brick_hd.png'
BRK_TEAL_FILENAME: str = 'teal_brick_hd.png'
BRK_LAVENDER_FILENAME: str = 'lavender_brick_hd.png'
BRK_GOLD_FILENAME: str = 'gold_brick.png'
BALL_FILENAME: str = 'ball.png'
PADDLE_FILENAME: str = 'paddle.png'

ANIMATE_BRICK_0_FILENAME: str = 'animate_brick_0.png'
ANIMATE_BRICK_1_FILENAME: str = 'animate_brick_1.png'
ANIMATE_BRICK_2_FILENAME: str = 'animate_brick_2.png'
ANIMATE_BRICK_3_FILENAME: str = 'animate_brick_3.png'
ANIMATE_BRICK_4_FILENAME: str = 'animate_brick_4.png'
ANIMATE_BRICK_5_FILENAME: str = 'animate_brick_5.png'
ANIMATE_BRICK_6_FILENAME: str = 'animate_brick_6.png'
ANIMATE_BRICK_7_FILENAME: str = 'animate_brick_7.png'
ANIMATE_BRICK_8_FILENAME: str = 'animate_brick_8.png'
ANIMATE_BRICK_9_FILENAME: str = 'animate_brick_9.png'
ANIMATE_BRICK_10_FILENAME: str = 'animate_brick_10.png'
ANIMATE_BRICK_11_FILENAME: str = 'animate_brick_11.png'
ANIMATE_BRICK_12_FILENAME: str = 'animate_brick_12.png'
ANIMATE_BRICK_13_FILENAME: str = 'animate_brick_13.png'
ANIMATE_BRICK_14_FILENAME: str = 'animate_brick_14.png'
ANIMATE_BRICK_15_FILENAME: str = 'animate_brick_15.png'
ANIMATE_BRICK_16_FILENAME: str = 'animate_brick_16.png'

MUTE_ICON_FILENAME: str = 'mute_white.png'
VOLUME_ICON_FILENAME: str = 'volume_white.png'

BACKGROUND_IMG, BALL_IMG, PADDLE_IMG = None, None, None
BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG = None, None, None
BRK_RED_IMG, BRK_PINK_IMG, BRK_ORANGE_IMG, = None, None, None
BRK_LTBLUE_IMG, BRK_PURPLE_IMG, BRK_TEAL_IMG = None, None, None
BRK_LAVENDER_IMG, BRK_GOLD_IMG = None, None
ANIMATE_BRICK_0_IMG, ANIMATE_BRICK_1_IMG, ANIMATE_BRICK_2_IMG = None, None, None
ANIMATE_BRICK_3_IMG, ANIMATE_BRICK_4_IMG, ANIMATE_BRICK_5_IMG, ANIMATE_BRICK_6_IMG = None, None, None, None
ANIMATE_BRICK_7_IMG, ANIMATE_BRICK_8_IMG, ANIMATE_BRICK_9_IMG, ANIMATE_BRICK_10_IMG = None, None, None, None
ANIMATE_BRICK_11_IMG, ANIMATE_BRICK_12_IMG, ANIMATE_BRICK_13_IMG, ANIMATE_BRICK_14_IMG = None, None, None, None
ANIMATE_BRICK_15_IMG, ANIMATE_BRICK_16_IMG = None, None
MUTE_ICON, VOLUME_ICON, CHANNEL = None, None, None

BRICK_COLORS = []

BRICK_ANIMATION = []

MUSIC_PATHS = {}
BRICK_SFX, PADDLE_SFX, LEFT_WALL_SFX, RIGHT_WALL_SFX, TOP_WALL_SFX = None, None, None, None, None


def load_assets():
    """
    Lazy load the assets
    :return:
    """
    global BACKGROUND_IMG, BALL_IMG, PADDLE_IMG
    global BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG, BRK_RED_IMG
    global BRK_PINK_IMG, BRK_ORANGE_IMG, BRK_LTBLUE_IMG, BRK_PURPLE_IMG
    global BRK_TEAL_IMG, BRK_LAVENDER_IMG, BRK_GOLD_IMG, BRICK_COLORS
    global BRICK_ANIMATION, ANIMATE_BRICK_0_IMG, ANIMATE_BRICK_1_IMG, ANIMATE_BRICK_2_IMG
    global ANIMATE_BRICK_3_IMG, ANIMATE_BRICK_4_IMG, ANIMATE_BRICK_5_IMG, ANIMATE_BRICK_6_IMG
    global ANIMATE_BRICK_7_IMG, ANIMATE_BRICK_8_IMG, ANIMATE_BRICK_9_IMG, ANIMATE_BRICK_10_IMG, ANIMATE_BRICK_11_IMG
    global ANIMATE_BRICK_12_IMG, ANIMATE_BRICK_13_IMG, ANIMATE_BRICK_14_IMG, ANIMATE_BRICK_15_IMG, ANIMATE_BRICK_16_IMG
    global MUSIC_PATHS, BRICK_SFX, LEFT_WALL_SFX, RIGHT_WALL_SFX, TOP_WALL_SFX, PADDLE_SFX
    global MUTE_ICON, VOLUME_ICON, CHANNEL

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

    ANIMATE_BRICK_0_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_0_FILENAME))
    ANIMATE_BRICK_1_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_1_FILENAME))
    ANIMATE_BRICK_2_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_2_FILENAME))
    ANIMATE_BRICK_3_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_3_FILENAME))
    ANIMATE_BRICK_4_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_4_FILENAME))
    ANIMATE_BRICK_5_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_5_FILENAME))
    ANIMATE_BRICK_6_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_6_FILENAME))
    ANIMATE_BRICK_7_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_7_FILENAME))
    ANIMATE_BRICK_8_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_8_FILENAME))
    ANIMATE_BRICK_9_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_9_FILENAME))
    ANIMATE_BRICK_10_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_10_FILENAME))
    ANIMATE_BRICK_11_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_11_FILENAME))
    ANIMATE_BRICK_12_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_12_FILENAME))
    ANIMATE_BRICK_13_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_13_FILENAME))
    ANIMATE_BRICK_14_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_14_FILENAME))
    ANIMATE_BRICK_15_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_15_FILENAME))
    ANIMATE_BRICK_16_IMG = pygame.image.load(asset_path(ART_DIR, ANIMATE_BRICK_16_FILENAME))

    MUTE_ICON = pygame.image.load(asset_path(ART_DIR, MUTE_ICON_FILENAME))
    VOLUME_ICON = pygame.image.load(asset_path(ART_DIR, VOLUME_ICON_FILENAME))

    BRICK_COLORS = [BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG, BRK_RED_IMG, BRK_PINK_IMG, BRK_ORANGE_IMG,
                    BRK_LTBLUE_IMG, BRK_PURPLE_IMG, BRK_TEAL_IMG, BRK_LAVENDER_IMG]

    BRICK_ANIMATION = [ANIMATE_BRICK_0_IMG, ANIMATE_BRICK_1_IMG, ANIMATE_BRICK_2_IMG, ANIMATE_BRICK_3_IMG, ANIMATE_BRICK_4_IMG,
                       ANIMATE_BRICK_5_IMG, ANIMATE_BRICK_6_IMG, ANIMATE_BRICK_7_IMG, ANIMATE_BRICK_8_IMG,
                       ANIMATE_BRICK_9_IMG, ANIMATE_BRICK_10_IMG, ANIMATE_BRICK_11_IMG, ANIMATE_BRICK_12_IMG,
                       ANIMATE_BRICK_13_IMG, ANIMATE_BRICK_14_IMG, ANIMATE_BRICK_15_IMG, ANIMATE_BRICK_16_IMG]

    # music
    MUSIC_PATHS[GameState.GameStateName.SPLASH] = asset_path(SOUND_DIR, SPLASH_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.MENU_SCREEN] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.HOW_TO_PLAY] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.SETTINGS] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.CREDITS] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.LEADERBOARD] = asset_path(SOUND_DIR, MENU_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.PLAYING] = asset_path(SOUND_DIR, GAME_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.GAME_OVER] = asset_path(SOUND_DIR, GAME_OVER_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.GET_HIGH_SCORE] = asset_path(SOUND_DIR, SCORE_MUSIC_FILENAME)
    MUSIC_PATHS[GameState.GameStateName.READY_TO_LAUNCH] = asset_path(SOUND_DIR, GAME_MUSIC_FILENAME)

    # soundfx
    BRICK_SFX = asset_path(SOUND_DIR, BRICK_SFX_FILENAME)
    PADDLE_SFX = asset_path(SOUND_DIR, PADDLE_SFX_FILENAME)
    LEFT_WALL_SFX = asset_path(SOUND_DIR, LEFT_WALL_SFX_FILENAME)
    RIGHT_WALL_SFX = asset_path(SOUND_DIR, RIGHT_WALL_SFX_FILENAME)
    TOP_WALL_SFX = asset_path(SOUND_DIR, TOP_WALL_SFX_FILENAME)

    # sound channel selector
    CHANNEL = [pygame.mixer.Channel(i) for i in range(7)]