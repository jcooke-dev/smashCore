"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the test harness for the Leaderbaord class.
"""
import pytest

from score import Score
from src import Leaderboard


@pytest.fixture
def score_list():
    score_list: list[Score] = [Score(500, 1, "aaa"),
                           Score(300, 1, "bbb"),
                           Score(100, 1, "ccc"),
                           Score(50, 1, "ddd")]
    return score_list

@pytest.fixture
def score_list_full():
    score_list: list[Score] = [Score(500, 1, "aaa"),
                               Score(300, 1, "bbb"),
                               Score(100, 1, "ccc"),
                               Score(50, 1, "ddd"),
                               Score(350, 1, "eee"),
                               Score(250, 1, "fff"),
                               Score(150, 1, "aaa"),
                               Score(550, 1, "ddd"),
                               Score(560, 1, "ggg"),
                               Score(120, 1, "hhh"),
                               Score(56, 1, "iii"),
                               Score(80, 1, "jjj"),
                               Score(101, 1, "kkk")
                               ]
    return score_list

def test_is_high_score(score_list):
    top_scores = Leaderboard()
    top_scores.l_top_scores = score_list
    assert top_scores.is_high_score(1000)


def test_is_high_score_without_full_list(score_list):
    top_scores = Leaderboard()
    top_scores.l_top_scores = score_list
    assert top_scores.is_high_score(30)


def test_is_not_high_score_with_full_list(score_list_full):
    top_scores = Leaderboard()
    top_scores.l_top_scores = score_list_full
    assert top_scores.is_high_score(30) is False


def test_is_not_high_score_with_full_list_not_min_score(score_list_full):
    top_scores = Leaderboard()
    top_scores.l_top_scores = score_list_full
    assert top_scores.is_high_score(55) is False


def test_is_high_score_with_full_list(score_list_full):
    top_scores = Leaderboard()
    top_scores.l_top_scores = score_list_full
    assert top_scores.is_high_score(400)
