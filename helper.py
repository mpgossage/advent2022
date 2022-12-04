"""
Advent of Code 2022: helpers
"""


def load_lines(fname):
    with open(fname) as f:
        return [l.strip("\n") for l in f.readlines()]


def load_tokens(fname):
    with open(fname) as f:
        return [l.strip("\n").split() for l in f.readlines()]


##################


def test_load_tokens():
    arr = load_tokens("test02.txt")
    assert len(arr) == 3
    assert len(arr[0]) == 2
    assert arr[0][0] == "A"
    assert arr[0][1] == "Y"
