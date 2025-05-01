"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: Constants to be used throughout the application
"""

GAME_NAME = "SmashCore"

CLOSE_TO_ZERO = 0.00001 # for float comparisons to zero

# width and height of game board
WIDTH, HEIGHT = 1200, 800

INITIAL_FPS_SIMPLE = 60
MAX_FPS_VECTOR = 250 # note this should work out to a whole number of clock.tick ms for the loop

SPLASH_TIME_SECS = 2

PAD_WIDTH, PAD_HEIGHT = 150, 20
PADDLE_START_POSITION_OFFSET = 10
PADDLE_KEY_SPEED = 1.0 # base arrow key-control paddle speed

BALL_RADIUS = 15
BALL_SPEED_SIMPLE = 6 # initial speed for SIMPLE_1 model
BALL_SPEED_VECTOR = 0.55 # initial speed for VECTOR_1 model

BALL_SPEED_LEVEL_INCREMENT = 0.10 # incremental factor for initial ball speed upon level clear

BALL_SPEED_STEP = 0.012 # the speed added to the ball for brick breaks
BALL_SPEED_STEP_INCREMENT = 0.006 # the BALL_SPEED_STEP increment controlled and shown via dev overlay and keys
WORLD_GRAVITY_ACC = 0.0 # the magnitude of gravityAcc vector
WORLD_GRAVITY_ACC_INCREMENT = 0.00005 # the WORLD_GRAVITY_ACC increment controlled and shown via dev overlay and keys
PADDLE_IMPULSE = 0.0 # the magnitude of the vertical 'push' vel vector the paddle imparts to the ball
PADDLE_IMPULSE_INCREMENT = 0.02 # the PADDLE_IMPULSE increment controlled and shown via dev overlay and keys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (100, 100, 100)
DARK_BLUE = (36, 90, 190)
LIGHT_BLUE = (0, 176, 240)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
PURPLE = (102, 51, 153)
PINK = (254, 0, 127)

BRICK_SOLIDS = [DARK_BLUE, LIGHT_BLUE, RED, ORANGE, YELLOW, GREEN, PURPLE, PINK]

START_SCORE = 0
START_LIVES = 3
LEADERBOARD_SIZE = 10
SCORE_INITIALS_MAX = 3

SLIDER_WIDTH = 700
SLIDER_HEIGHT = 15
KNOB_RADIUS = 20

MUSIC_VOLUME_INITIAL = 1.0
SFX_VOLUME_INITIAL = 0.5
MUSIC_VOLUME_STEP = 0.125
SFX_VOLUME_STEP = 0.125

EFFECT_BRICK_PLAIN_DESTROY_DURATION = 40 # lifetime of fading plain Brick after destruction, in ms
EFFECT_BRICK_PLAIN_DESTROY_INFLATION = 0.25 # rect inflation of fading plain Brick after destruction
EFFECT_BRICK_PLAIN_DESTROY_FADE = True # fade the destroyed Brick?

EFFECT_BRICK_IMAGE_DESTROY_DURATION = 160 # lifetime of animating image Brick after destruction, in ms
EFFECT_BRICK_IMAGE_DESTROY_INFLATION = 0.0 # rect inflation of image Brick after destruction
EFFECT_BRICK_IMAGE_DESTROY_FADE = False # fade the destroyed Brick? -- not yet working for images
