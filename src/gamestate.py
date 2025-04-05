"""
    Consolidate the game state flags into a single class.
"""

from gamestates import GameStates
from motionmodels import MotionModels

class GameState:

    def __init__(self):

        self.running = True
        self.cur_state = GameStates.SPLASH
        self.fps_avg = 0.0
        self.loop_time_avg = 0
        self.show_dev_overlay = False
        self.motion_model = MotionModels.VECTOR_1
        self.tick_time = 0