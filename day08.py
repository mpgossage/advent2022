"""
Advent of Code 2022: day 8
After yesterdays nightmare, today is a nice simple grid

part two is a little more complex.
Was planning build a generator, but found that list comprehension worked fine.

"""
from helper import load_int_grid


def is_visible(grid, x, y):
    ly, lx = len(grid), len(grid[0])
    val = grid[y][x]
    # check up: if any are equal/taller hidden
    # so if none are equal/taller, its visible
    if any(grid[i][x] >= val for i in range(y)) == False:
        return True
    # similar for the rest
    if any(grid[y][i] >= val for i in range(x)) == False:
        return True
    if any(grid[i][x] >= val for i in range(y + 1, ly)) == False:
        return True
    if any(grid[y][i] >= val for i in range(x + 1, lx)) == False:
        return True
    # all taller, so its hidden
    return False


def day08a(fname):
    grid = load_int_grid(fname)
    ly, lx = len(grid), len(grid[0])
    visible = 0
    for y in range(ly):
        visible += sum((is_visible(grid, x, y) for x in range(lx)))
    return visible


def get_view_distance(height, arr):
    """gets the view distance.
    Takes the first item and an array or generator"""
    total = 0
    for a in arr:
        total += 1
        if a >= height:
            break
    return total


def get_view_value(grid, x, y):
    "returns the value for a given cell"
    ly, lx = len(grid), len(grid[0])
    val = grid[y][x]
    up = (grid[i][x] for i in range(y - 1, -1, -1))
    down = (grid[i][x] for i in range(y + 1, ly))
    left = (grid[y][i] for i in range(x - 1, -1, -1))
    right = (grid[y][i] for i in range(x + 1, lx))
    return (
        get_view_distance(val, up)
        * get_view_distance(val, down)
        * get_view_distance(val, left)
        * get_view_distance(val, right)
    )


def day08b(fname):
    grid = load_int_grid(fname)
    ly, lx = len(grid), len(grid[0])
    best = -1
    for y in range(ly):
        best = max(best, max(get_view_value(grid, x, y) for x in range(lx)))
    return best


#####################

if __name__ == "__main__":
    print("day08a", day08a("input08.txt"))
    print("day08b", day08b("input08.txt"))

#####################


def test_is_visible():
    grid = load_int_grid("test08.txt")
    # sanity tests
    assert is_visible(grid, 0, 0) == True
    assert is_visible(grid, 0, 4) == True
    assert is_visible(grid, 4, 0) == True
    assert is_visible(grid, 4, 4) == True
    # cases listed in example
    assert is_visible(grid, 1, 1) == True
    assert is_visible(grid, 2, 1) == True
    assert is_visible(grid, 3, 1) == False
    assert is_visible(grid, 1, 2) == True
    assert is_visible(grid, 2, 2) == False
    assert is_visible(grid, 3, 2) == True
    assert is_visible(grid, 1, 3) == False
    assert is_visible(grid, 2, 3) == True
    assert is_visible(grid, 3, 3) == False


def test_day08a():
    assert day08a("test08.txt") == 21


def test_get_view_dist():
    # edge
    assert get_view_distance(5, []) == 0
    # examples from problem
    assert get_view_distance(5, [3]) == 1
    assert get_view_distance(5, [1, 2]) == 2
    assert get_view_distance(5, [3, 5, 3]) == 2
    assert get_view_distance(5, [5, 2]) == 1
    assert get_view_distance(5, [3, 5, 3]) == 2
    assert get_view_distance(5, [4, 9]) == 2
    assert get_view_distance(5, [3]) == 1
    assert get_view_distance(5, [3, 3]) == 2


def test_get_view_value():
    grid = load_int_grid("test08.txt")
    # sanity
    assert get_view_value(grid, 0, 0) == 0
    assert get_view_value(grid, 4, 4) == 0
    # examples
    assert get_view_value(grid, 2, 1) == 4
    assert get_view_value(grid, 2, 3) == 8


def test_day08b():
    assert day08b("test08.txt") == 8
