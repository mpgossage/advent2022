"""
Advent of Code 2022: Day14

A wonderful fun day, sand simulation.

Fairly simple, but a lot of by eye testing
"""

from helper import load_lines


def load_walls(fname):
    "returns double list of lines"
    pos2tuple = lambda s: tuple(int(t) for t in s.split(","))
    line2points = lambda l: [pos2tuple(t) for t in l.split("->")]
    return [line2points(l) for l in load_lines(fname)]


def walls_to_grid(walls, sand):
    "converts walls to a grid & returns the grid & the offset sand pos"
    minx, miny = sand
    maxx, maxy = sand
    for wall in walls:
        minx = min(minx, min(w[0] for w in wall))
        maxx = max(maxx, max(w[0] for w in wall))
        miny = min(miny, min(w[1] for w in wall))
        maxy = max(maxy, max(w[1] for w in wall))
    # make a grid of air
    w, h = 1 + maxx - minx, 1 + maxy - miny
    grid = [["."] * w for _ in range(h)]
    for wall in walls:
        # fill the lines into the grid
        for i in range(len(wall) - 1):
            w1, w2 = wall[i], wall[i + 1]
            # line from w1 to w2
            if w1[0] == w2[0]:
                # its vertical
                x, y1, y2 = w1[0], w1[1], w2[1]
                if y1 > y2:
                    y1, y2 = y2, y1
                for y in range(y1, y2 + 1):
                    grid[y - miny][x - minx] = "#"
            else:
                # horizontal
                x1, x2, y = w1[0], w2[0], w1[1]
                if x1 > x2:
                    x1, x2 = x2, x1
                for x in range(x1, x2 + 1):
                    grid[y - miny][x - minx] = "#"
    grid[sand[1] - miny][sand[0] - minx] = "+"
    return grid, (sand[0] - minx, sand[1] - miny)


def print_grid(grid):
    for g in grid:
        print("".join(g))


def drop_sand(grid, sand):
    sx, sy = sand
    # if not able to drop sand error
    if grid[sy][sx] != "+":
        return False
    # simulate:
    h, w = len(grid), len(grid[0])
    # if able to move down do so
    while True:
        # if reached the edge, then its assumed to fall forever
        if sx == 0 or sx == w - 1 or sy == h - 1:
            return False
        if grid[sy + 1][sx] == ".":
            sy += 1
        elif grid[sy + 1][sx - 1] == ".":
            sy += 1
            sx -= 1
        elif grid[sy + 1][sx + 1] == ".":
            sy += 1
            sx += 1
        else:
            # not able to fall, it must be stable, add it
            grid[sy][sx] = "o"
            return True


def day14a(fname):
    walls = load_walls(fname)
    grid, sand = walls_to_grid(walls, (500, 0))
    total = 0
    while drop_sand(grid, sand):
        total += 1
    return total


def add_floor(walls, sand):
    "adds a floor to the walls"
    sx, sy = sand
    # what is the biggest Y value?
    maxy = sy
    for wall in walls:
        maxy = max(maxy, max(w[1] for w in wall))
    floory = maxy + 2
    # assume a triangle (add a bit)
    h = floory - sy
    floorx1, floorx2 = sx - h - 2, sx + h + 2
    return walls + [[(floorx1, floory), (floorx2, floory)]]


def day14b(fname):
    walls = load_walls(fname)
    sand = (500, 0)
    walls = add_floor(walls, sand)
    grid, sand = walls_to_grid(walls, sand)
    total = 0
    while drop_sand(grid, sand):
        total += 1
    return total


#########


def visualise(grid, sand):
    print_grid(grid)
    i = 0
    while True:
        r = drop_sand(grid, sand)
        print(i, r)
        print_grid(grid)
        if r == False:
            break
        i += 1


if __name__ == "__main__":
    walls = load_walls("test14.txt")
    sand = (500, 0)
    print(walls)
    walls = add_floor(walls, sand)
    print(walls)
    grid, sand = walls_to_grid(walls, sand)
    visualise(grid, sand)
    print("day14a", day14a("input14.txt"))
    print("day14b", day14b("input14.txt"))

#########


def test_load_walls():
    walls = load_walls("test14.txt")
    assert len(walls) == 2
    assert walls[0] == [(498, 4), (498, 6), (496, 6)]
    assert walls[1] == [(503, 4), (502, 4), (502, 9), (494, 9)]


# NB: no testing of walls_to_grid(), done by eye


def test_drop_sand():
    walls = load_walls("test14.txt")
    grid, sand = walls_to_grid(walls, (500, 0))

    assert grid[8][6] == "."
    drop_sand(grid, sand)
    assert grid[8][6] == "o"
    drop_sand(grid, sand)
    assert grid[8][6] == "o"
    assert grid[8][5] == "o"
    drop_sand(grid, sand)
    assert grid[8][7] == "o"
    assert grid[8][6] == "o"
    assert grid[8][5] == "o"
    drop_sand(grid, sand)
    drop_sand(grid, sand)
    assert grid[7][6] == "o"
    assert grid[8][4] == "o"
    # rest tested by eye


def test_day14a():
    assert day14a("test14.txt") == 24
