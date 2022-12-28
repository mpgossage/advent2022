"""
Advent of code 2022: day 12
Its another grid & a pathfinder, looks ok.
I'm thinking just going directly for it with minimal tests.
Going to start with a BFS and if needed use a best-first-search.
I know these algols so well I can write it first time without needing to debug

Part two will need me to split the function up a bit.
I also have two options:
1. for each square which is 'a', find its route
2. work backwards from 'z' and get all values of 'a'
I will take option 1, its less efficient, but would be simpler to build

Total code was a half hours work, nice and easy
"""

from helper import load_lines


def load_grid(fname):
    grid = [list(l) for l in load_lines(fname)]
    # find start & end, and turn values into 0..25
    h, w = len(grid), len(grid[0])
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "S":
                start = (x, y)
                grid[y][x] = 0
            elif grid[y][x] == "E":
                end = (x, y)
                grid[y][x] = 25
            else:
                grid[y][x] = ord(grid[y][x]) - ord("a")
    return grid, start, end


def bfs(grid, start, end):
    # keep it simple: BFS
    h, w = len(grid), len(grid[0])
    costs = []
    high_cost = w * h
    for y in range(h):
        costs.append([high_cost] * w)
    costs[start[1]][start[0]] = 0
    todo = [start]
    while todo:
        x, y = todo.pop(0)
        cst = costs[y][x]
        hgt = grid[y][x]
        # check adjacent:
        # must be valid, must be max 1 unit higher, must cost more than current
        if y > 0 and grid[y - 1][x] <= hgt + 1 and costs[y - 1][x] > cst + 1:
            costs[y - 1][x] = cst + 1
            todo.append((x, y - 1))
        if y < h - 1 and grid[y + 1][x] <= hgt + 1 and costs[y + 1][x] > cst + 1:
            costs[y + 1][x] = cst + 1
            todo.append((x, y + 1))
        if x > 0 and grid[y][x - 1] <= hgt + 1 and costs[y][x - 1] > cst + 1:
            costs[y][x - 1] = cst + 1
            todo.append((x - 1, y))
        if x < w - 1 and grid[y][x + 1] <= hgt + 1 and costs[y][x + 1] > cst + 1:
            costs[y][x + 1] = cst + 1
            todo.append((x + 1, y))
    return costs[end[1]][end[0]]


def day12a(fname):
    grid, start, end = load_grid(fname)
    return bfs(grid, start, end)


def day12b(fname):
    grid, _, end = load_grid(fname)
    h, w = len(grid), len(grid[0])
    # now find all possible start points and the best price
    all_points = ((x, y) for x in range(w) for y in range(h))
    return min(bfs(grid, pos, end) for pos in all_points if grid[pos[1]][pos[0]] == 0)


########

if __name__ == "__main__":
    print("day12a", day12a("input12.txt"))
    print("day12b", day12b("input12.txt"))

########


def test_day12a():
    assert day12a("test12.txt") == 31


def test_day12b():
    assert day12b("test12.txt") == 29
