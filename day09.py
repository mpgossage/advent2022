"""
Advent of Code 2022: day 9
This is a simulation system, doesn't look too hard, but might be difficult to unit test

Part 2 looks interesting I think my simulation will work, but lets test.
The sim worked fine first time.

Plus it turned out it was faily easy to unit test
"""

from helper import load_tokens


def load_positions(fname):
    "loads a file and returns a list of all the positions"
    px, py = 0, 0
    result = [(px, py)]
    tokens = load_tokens(fname)
    for direct, dist in tokens:
        if direct == "U":
            dx, dy = 0, -1
        elif direct == "D":
            dx, dy = 0, +1
        elif direct == "L":
            dx, dy = -1, 0
        elif direct == "R":
            dx, dy = +1, 0
        for t in range(int(dist)):
            px += dx
            py += dy
            result.append((px, py))
    return result


def simulate_tail(head, tail):
    "returns the new tail"
    hx, hy = head
    tx, ty = tail
    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
        if hx < tx:
            tx -= 1
        elif hx > tx:
            tx += 1
        if hy < ty:
            ty -= 1
        elif hy > ty:
            ty += 1
    return (tx, ty)


def simulate_tail_movement(positions):
    tail = positions[0]
    result = []
    for h in positions:
        tail = simulate_tail(h, tail)
        result.append(tail)
    return result


def day09a(fname):
    poss = load_positions(fname)
    tails = simulate_tail_movement(poss)
    return len(set(tails))


def simulate_long_tail_movement(positions, ln):
    result = []
    # note: we dont realy care about all the positions, just the last one
    # but returning all for testing
    for i in range(ln):
        positions = simulate_tail_movement(positions)
        result.append(positions)
    return result


def day09b(fname):
    poss = load_positions(fname)
    tails = simulate_long_tail_movement(poss, 9)
    return len(set(tails[-1]))


################

if __name__ == "__main__":
    print("day09a", day09a("input09.txt"))
    print("day09b", day09b("input09.txt"))

################


def test_load_positions():
    poss = load_positions("test09.txt")
    assert len(poss) == 25  # 24 steps+first step
    # not going to do every step, just a few
    assert poss[0] == (0, 0)
    assert poss[4] == (4, 0)
    assert poss[5] == (4, -1)
    assert poss[8] == (4, -4)
    assert poss[-1] == (2, -2)


def test_simulate_tail_movement():
    poss = load_positions("test09.txt")
    tails = simulate_tail_movement(poss)
    assert len(tails) == 25
    assert tails[0] == (0, 0)
    assert tails[-1] == (1, -2)


def test_day09a():
    assert day09a("test09.txt") == 13


def test_simulate_long_tail_movement():
    poss = load_positions("test09.txt")
    tails = simulate_long_tail_movement(poss, 9)
    # for this we will look at last point of the tail
    assert poss[-1] == (2, -2)
    assert tails[0][-1] == (1, -2)
    assert tails[1][-1] == (2, -2)
    assert tails[2][-1] == (3, -2)
    assert tails[3][-1] == (2, -2)
    assert tails[4][-1] == (1, -1)
    assert tails[5][-1] == (0, 0)
    assert tails[6][-1] == (0, 0)
    assert tails[7][-1] == (0, 0)
    assert tails[8][-1] == (0, 0)


def test_day09b():
    assert day09b("test09.txt") == 1
    assert day09b("test09b.txt") == 36


def test_simulate_long_tail_movement2():
    # much longer version
    poss = load_positions("test09b.txt")
    tails = simulate_long_tail_movement(poss, 9)
    # for this we will look at last point of the tail
    assert poss[-1] == (-11, -15)
    assert tails[0][-1] == (-11, -14)
    assert tails[1][-1] == (-11, -13)
    assert tails[2][-1] == (-11, -12)
    assert tails[3][-1] == (-11, -11)
    assert tails[4][-1] == (-11, -10)
    assert tails[5][-1] == (-11, -9)
    assert tails[6][-1] == (-11, -8)
    assert tails[7][-1] == (-11, -7)
    assert tails[8][-1] == (-11, -6)
