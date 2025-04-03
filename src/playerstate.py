"""
    Consolidate the player state data into a single class.
"""

import constants


class PlayerState:

    def __init__(self):

        self.lives = constants.START_LIVES
        self.score = 0
