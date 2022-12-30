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


# extra routines for a continual line set
# format is [(a,b)...] which shows the range a..b
def remove_set(data, rem_start, rem_end):
    "removes rem_st..rem_end from set"
    # simple version: using move/pop
    result = []
    while data:
        start, end = data.pop(-1)
        if start > rem_end or end < rem_start:
            # not touching, move over
            result.append((start, end))
        elif rem_start <= start and rem_end < end:
            # removing the lower section
            result.append((rem_end + 1, end))
        elif rem_end >= end and rem_start > start:
            # removing the upper section
            result.append((start, rem_start - 1))
        elif rem_start > start and rem_end < end:
            # complex one, its inside the range
            result.append((start, rem_start - 1))
            result.append((rem_end + 1, end))
        # else start..end is full inside & we discard
    return result


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


def test_remove_set():
    data = [(0, 100)]
    assert data == [(0, 100)]
    # remove outside: nothing changed
    data = remove_set(data, -10, -1)
    data = remove_set(data, 101, 200)
    assert data == [(0, 100)]
    # remove lower:
    data = remove_set(data, -10, 10)
    assert data == [(11, 100)]
    # remove upper
    data = remove_set(data, 90, 200)
    assert data == [(11, 89)]
    # remove middle
    data = remove_set(data, 50, 60)
    assert data == [(11, 49), (61, 89)]
    # now a few more bits (using set to ignore the order)
    data = remove_set(data, 20, 30)
    assert set(data) == set([(11, 19), (31, 49), (61, 89)])
    data = remove_set(data, 60, 70)
    assert set(data) == set([(11, 19), (31, 49), (71, 89)])
    data = remove_set(data, 20, 70)
    assert set(data) == set([(11, 19), (71, 89)])
