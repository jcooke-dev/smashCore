"""
    Consolidate the game state flags into a single class.
"""

from gamestates import GameStates

class GameState:

    def __init__(self):

        self.running = True
        self.cur_state = GameStates.SPLASH
