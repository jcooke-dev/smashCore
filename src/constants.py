"""
    Constants to be used throughout the application
"""
import os

import pygame

GAME_NAME = "SmashCore"

# width and height of game board
WIDTH, HEIGHT = 1200, 800

INITIAL_FPS_SIMPLE = 60
MAX_FPS_VECTOR = 250 # note this should work out to a whole number of clock.tick ms for the loop

SPLASH_TIME_SECS = 2

PAD_WIDTH, PAD_HEIGHT = 150, 20
PADDLE_START_POSITION_OFFSET = 10
PAD_MOVE_LEFT = 25
PAD_MOVE_RIGHT = 25

BALL_RADIUS = 15
BALL_SPEED_SIMPLE = 6
BALL_SPEED_VECTOR = 0.55
BALL_SPEED_INCREMENT_VECTOR = 0.013
WORLD_GRAVITY_ACC = 0.00020
PADDLE_IMPULSE = 0.04

art_dir = 'assets/art/'
sound_dir = 'assets/sound/'
background_img_path = 'background.png'
yellow_img_path = 'yellow_brick.png'
blue_img_path = 'blue_brick.png'
green_img_path = 'green_brick.png'
red_img_path = 'red_brick.png'
pink_img_path = 'pink_brick.png'
orange_img_path = 'orange_brick.png'
lt_blue_img_path = 'lt_blue_brick.png'
purple_img_path = 'purple_brick.png'
teal_img_path = 'teal_brick.png'
lavender_img_path = 'lavender_brick.png'
ball_img_path = 'ball.png'
paddle_img_path = 'paddle.png'

background_img = pygame.image.load(os.path.join(art_dir, background_img_path))
yellow = pygame.image.load(os.path.join(art_dir, yellow_img_path))
blue = pygame.image.load(os.path.join(art_dir, blue_img_path))
green = pygame.image.load(os.path.join(art_dir, green_img_path))
red = pygame.image.load(os.path.join(art_dir, red_img_path))
pink = pygame.image.load(os.path.join(art_dir, pink_img_path))
orange = pygame.image.load(os.path.join(art_dir, orange_img_path))
lt_blue = pygame.image.load(os.path.join(art_dir, lt_blue_img_path))
purple = pygame.image.load(os.path.join(art_dir, purple_img_path))
teal = pygame.image.load(os.path.join(art_dir, teal_img_path))
lavender = pygame.image.load(os.path.join(art_dir, lavender_img_path))
ball = pygame.image.load(os.path.join(art_dir, ball_img_path))
paddle = pygame.image.load(os.path.join(art_dir, paddle_img_path))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

START_SCORE = 0
START_LIVES = 3
