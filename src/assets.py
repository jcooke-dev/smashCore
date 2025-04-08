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
import pygame

ART_DIR = 'assets/art/'
SOUND_DIR = 'assets/sound/'
BACKGROUND_FILENAME = 'background.png'
BRK_YELLOW_FILENAME = 'yellow_brick.png'
BRK_BLUE_FILENAME = 'blue_brick.png'
BRK_GREEN_FILENAME = 'green_brick.png'
BRK_RED_FILENAME = 'red_brick.png'
BRK_PINK_FILENAME = 'pink_brick.png'
BRK_ORANGE_FILENAME = 'orange_brick.png'
BRK_LTBLUE_FILENAME = 'lt_blue_brick.png'
BRK_PURPLE_FILENAME = 'purple_brick.png'
BRK_TEAL_FILENAME = 'teal_brick.png'
BRK_LAVENDER_FILENAME = 'lavender_brick.png'
BALL_FILENAME = 'ball.png'
PADDLE_FILENAME = 'paddle.png'

BACKGROUND_IMG, BALL_IMG, PADDLE_IMG = None, None, None
BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG = None, None, None
BRK_RED_IMG, BRK_PINK_IMG, BRK_ORANGE_IMG, = None, None, None
BRK_LTBLUE_IMG, BRK_PURPLE_IMG, BRK_TEAL_IMG = None, None, None
BRK_LAVENDER_IMG = None


def load_assets():
    """
    Lazy load the assets
    :return:
    """
    global BACKGROUND_IMG, BALL_IMG, PADDLE_IMG
    global BRK_YELLOW_IMG, BRK_BLUE_IMG, BRK_GREEN_IMG, BRK_RED_IMG
    global BRK_PINK_IMG, BRK_ORANGE_IMG, BRK_LTBLUE_IMG, BRK_PURPLE_IMG
    global BRK_TEAL_IMG, BRK_LAVENDER_IMG
    BACKGROUND_IMG = pygame.image.load(os.path.join(ART_DIR, BACKGROUND_FILENAME))
    BRK_YELLOW_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_YELLOW_FILENAME))
    BRK_BLUE_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_BLUE_FILENAME))
    BRK_GREEN_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_GREEN_FILENAME))
    BRK_RED_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_RED_FILENAME))
    BRK_PINK_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_PINK_FILENAME))
    BRK_ORANGE_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_ORANGE_FILENAME))
    BRK_LTBLUE_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_LTBLUE_FILENAME))
    BRK_PURPLE_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_PURPLE_FILENAME))
    BRK_TEAL_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_TEAL_FILENAME))
    BRK_LAVENDER_IMG = pygame.image.load(os.path.join(ART_DIR, BRK_LAVENDER_FILENAME))
    BALL_IMG = pygame.image.load(os.path.join(ART_DIR, BALL_FILENAME))
    PADDLE_IMG = pygame.image.load(os.path.join(ART_DIR, PADDLE_FILENAME))
