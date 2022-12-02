"""
Advent of Code 2022: day 2
Time taken ~40 mins

Part B made my think, then I realised I could just have another lookup
to pick the correct choice.
"""
import pytest
from helper import *


def rps_winner(a, b):
    "returns 1,0,-1 for win/draw/loss for RPS from prespective of 2nd player"
    if a == "A":
        if b == "Y":
            return 1
        elif b == "X":
            return 0
        return -1
    if a == "B":
        if b == "Z":
            return 1
        elif b == "Y":
            return 0
        return -1
    # 'C'
    if b == "X":
        return 1
    elif b == "Z":
        return 0
    return -1


def score_round(a, b):
    "returns the score for the round"
    win = rps_winner(a, b)
    token_val = {"X": 1, "Y": 2, "Z": 3}
    return (win + 1) * 3 + token_val[b]


def score_round_b(a, b):
    "returns the score for the round"
    # more complex as we need to work backwards
    if b == "X":  # must lose
        choices = {"A": "Z", "B": "X", "C": "Y"}
    elif b == "Y":  # must draw
        choices = {"A": "X", "B": "Y", "C": "Z"}
    else:  # must win
        choices = {"A": "Y", "B": "Z", "C": "X"}

    new_choice = choices[a]
    win = rps_winner(a, new_choice)

    token_val = {"X": 1, "Y": 2, "Z": 3}
    return (win + 1) * 3 + token_val[new_choice]


def day02a(fname):
    moves = load_tokens(fname)
    score = sum(score_round(mv[0], mv[1]) for mv in moves)
    return score


def day02b(fname):
    moves = load_tokens(fname)
    score = sum(score_round_b(mv[0], mv[1]) for mv in moves)
    return score


##############

if __name__ == "__main__":
    print("day02a", day02a("input02.txt"))
    print("day02b", day02b("input02.txt"))

##############


def test_score_round():
    assert score_round("A", "Y") == 8
    assert score_round("B", "X") == 1
    assert score_round("C", "Z") == 6


def test_day02a():
    assert day02a("test02.txt") == 15


def test_day02b():
    assert day02b("test02.txt") == 12
