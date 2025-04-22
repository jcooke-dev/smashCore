"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This maintains a single score's data
"""

from datetime import datetime


class Score:
    """ This maintains a single score's data """

    def __init__(self, scr: int, lvl: int, id: str):

        self.score: int = scr
        self.level: int = lvl
        self.player: str = 'default'
        self.id: str = '---' if len(id) == 0 else id
        self.dt_scored: datetime = datetime.now()

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        if isinstance(other, Score):
            return self.score == other.score and self.level == other.level and self.id == other.id
        return False
