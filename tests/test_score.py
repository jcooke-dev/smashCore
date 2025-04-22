"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Score class.
"""
from datetime import datetime
from src.score import Score


def test_score_initialization():
    """
    Test score initial state
    :return:
    """
    score = Score(scr=100, lvl=2, id="player1")
    assert score.score == 100
    assert score.level == 2
    assert score.player == "default"
    assert score.id == "player1"
    assert isinstance(score.dt_scored, datetime)


def test_score_initialization_empty_id():
    """
    Test score initial state when id is empty
    :return:
    """
    score = Score(scr=50, lvl=1, id="")
    assert score.id == "---"


def test_score_comparison_lt():
    """
    Test score comparison
    :return:
    """
    score1 = Score(scr=100, lvl=2, id="player1")
    score2 = Score(scr=200, lvl=3, id="player2")
    assert score1.__lt__(score2)


def test_score_comparison_eq():
    """
    Test score equality
    :return:
    """
    score1 = Score(scr=100, lvl=2, id="player1")
    score2 = Score(scr=100, lvl=2, id="player1")
    assert score1.__eq__(score2)


def test_score_comparison_eq_different():
    """
    Test scores not equal
    :return:
    """
    score1 = Score(scr=100, lvl=2, id="player1")
    score2 = Score(scr=100, lvl=3, id="player2")
    assert not score1.__eq__(score2)


def test_score_comparison_eq_different_objects():
    """
    Test scores not equal
    :return:
    """
    score1 = Score(scr=100, lvl=2, id="player1")
    str = ""
    assert not score1.__eq__(str)