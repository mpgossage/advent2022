"""
Advent of Code 2022: day 4
Time taken <30 minutes, this was a simple one
"""

import pytest
from helper import *


def parse_input(fname):
    tokens = load_tokens(fname, ",")
    # tokens with be of the form 1-3
    # split them down
    def parser(s):
        parts = s.split("-")
        return int(parts[0]), int(parts[1])

    return [(parser(t[0]), parser(t[1])) for t in tokens]


def is_full_overlap(pair):
    # one line unpack
    (e1start, e1end), (e2start, e2end) = pair
    return (e1start <= e2start and e1end >= e2end) or (
        e2start <= e1start and e2end >= e1end
    )


def is_partial_overlap(pair):
    (e1start, e1end), (e2start, e2end) = pair
    inside = lambda val, start, end: start <= val <= end
    return (
        inside(e1start, e2start, e2end)
        or inside(e1end, e2start, e2end)
        or inside(e2start, e1start, e1end)
        or inside(e2end, e1start, e1end)
    )


def day04a(fname):
    tokens = parse_input(fname)
    return sum((1 for t in tokens if is_full_overlap(t)))


def day04b(fname):
    tokens = parse_input(fname)
    return sum((1 for t in tokens if is_partial_overlap(t)))


###########


if __name__ == "__main__":
    print("day04a", day04a("input04.txt"))
    print("day04b", day04b("input04.txt"))

###########


def test_parse_input():
    tokens = parse_input("test04.txt")
    assert len(tokens) == 6
    assert tokens[0] == ((2, 4), (6, 8))


def test_is_full_overlap():
    # large part A
    assert is_full_overlap(((1, 10), (1, 10))) == True
    assert is_full_overlap(((1, 10), (1, 1))) == True
    assert is_full_overlap(((1, 10), (2, 2))) == True
    assert is_full_overlap(((1, 10), (10, 10))) == True
    # large part B
    assert is_full_overlap(((1, 1), (1, 10))) == True
    assert is_full_overlap(((5, 5), (1, 10))) == True
    assert is_full_overlap(((10, 10), (1, 10))) == True
    # partial overlap
    assert is_full_overlap(((1, 5), (2, 6))) == False
    assert is_full_overlap(((2, 6), (1, 5))) == False
    # no overlap
    assert is_full_overlap(((1, 5), (6, 10))) == False
    assert is_full_overlap(((6, 10), (1, 5))) == False
    # gaps
    assert is_full_overlap(((1, 4), (6, 10))) == False
    assert is_full_overlap(((6, 10), (1, 4))) == False


def test_is_partial_overlap():
    # large part A
    assert is_partial_overlap(((1, 10), (1, 10))) == True
    assert is_partial_overlap(((1, 10), (1, 1))) == True
    assert is_partial_overlap(((1, 10), (2, 2))) == True
    assert is_partial_overlap(((1, 10), (10, 10))) == True
    # large part B
    assert is_partial_overlap(((1, 1), (1, 10))) == True
    assert is_partial_overlap(((5, 5), (1, 10))) == True
    assert is_partial_overlap(((10, 10), (1, 10))) == True
    # partial overlap
    assert is_partial_overlap(((1, 5), (2, 6))) == True
    assert is_partial_overlap(((2, 6), (1, 5))) == True
    # no overlap
    assert is_partial_overlap(((1, 5), (6, 10))) == False
    assert is_partial_overlap(((6, 10), (1, 5))) == False
    # gaps
    assert is_partial_overlap(((1, 4), (6, 10))) == False
    assert is_partial_overlap(((6, 10), (1, 4))) == False


def test_day04a():
    assert day04a("test04.txt") == 2


def test_day04b():
    assert day04b("test04.txt") == 4
