"""
    Constants to be used throughout the application
"""

from src.levels import Levels


GAME_NAME = "SmashCore"

# width and height of game board
WIDTH, HEIGHT = 1200, 800

INITIAL_FPS = 60

PAD_WIDTH, PAD_HEIGHT = 200, 20
PADDLE_START_POSITION_OFFSET = 10
PAD_MOVE_LEFT = 25
PAD_MOVE_RIGHT = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)

START_SCORE = 0
START_LIVES = 3

# default start level
START_LEVEL = Levels.LevelName.SMASHCORE_1
