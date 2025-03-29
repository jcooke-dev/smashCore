"""
    Consolidate the game state flags into a single class.
"""

class GameState:

    def __init__(self):
        self.running = True
        self.game_over = False
        self.pause = False
        self.game_start = False

