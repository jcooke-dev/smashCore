"""
    Consolidate the game state flags into a single class.
"""

from gamestates import GameStates

class GameState:

    def __init__(self):

        self.running = True
        self.cur_state = GameStates.SPLASH
        self.fps_avg = 0.0
        self.loop_time_avg = 0
        self.show_dev_overlay = False
