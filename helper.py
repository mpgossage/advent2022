"""
Advent of Code 2022: helpers
"""


def load_file(fname):
    with open(fname) as f:
        return f.read()


def load_lines(fname):
    with open(fname) as f:
        return [l.strip("\n") for l in f.readlines()]


def load_tokens(fname, sep=None):
    with open(fname) as f:
        return [l.strip("\n").split(sep) for l in f.readlines()]


def load_int_grid(fname):
    """loads a 2d grid of numbers and returns a Y-X grid.
    so grid[y][x] is the item you want"""
    grid = []
    with open(fname) as f:
        for l in f.readlines():
            grid.append([int(a) for a in l.strip("\n")])
    return grid


##################


def test_load_tokens():
    arr = load_tokens("test02.txt")
    assert len(arr) == 3
    assert len(arr[0]) == 2
    assert arr[0][0] == "A"
    assert arr[0][1] == "Y"


def test_load_tokens_with_sep():
    arr = load_tokens("test04.txt", ",")
    assert len(arr) == 6
    assert len(arr[0]) == 2
    assert arr[0][0] == "2-4"
    assert arr[0][1] == "6-8"


def test_load_int_grid():
    grid = load_int_grid("test08.txt")
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert len(grid[4]) == 5
    assert grid[0][0] == 3
    assert grid[0][4] == 3
    assert grid[2][2] == 3
    assert grid[4][0] == 3
    assert grid[4][4] == 0
