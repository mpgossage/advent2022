"""
Advent of code 2022: Day 13

Rules look a little complex, but not too difficult looking.

Expecting part two to be more processing.
Its generally ok, but it needs a sort with a comparison fn (which I built).
But python 3 removed this, so I need to investigate python
"""

import functools
from helper import load_file


def load_pairs(fname):
    file = load_file(fname)
    result = []
    for s in file.split("\n\n"):
        a = s.split("\n")
        result.append((eval(a[0]), eval(a[1])))
    return result


def compare_lists(a, b):
    "compares the list and returns 1,0,-1 for good, unknown, bad"
    if type(a) == int and type(b) == int:
        if a < b:
            return 1
        elif a > b:
            return -1
        return 0
    elif type(a) == list and type(b) == list:
        # zip will combine the shorter items
        for p in zip(a, b):
            v = compare_lists(p[0], p[1])
            if v != 0:
                return v
        # compare length(its actually comparing the length)
        return compare_lists(len(a), len(b))
    elif type(a) == list and type(b) == int:
        return compare_lists(a, [b])
    elif type(a) == int and type(b) == list:
        return compare_lists([a], b)
    print(a, b)
    assert False


def day13a(fname):
    pairs = load_pairs(fname)
    # note 1+idx as idx is 0 based
    return sum(1 + idx for idx, p in enumerate(pairs) if compare_lists(p[0], p[1]) == 1)


def day13b(fname):
    pairs = load_pairs(fname)
    divider_a, divider_b = [[2]], [[6]]
    packets = [divider_a, divider_b]
    for p in pairs:
        packets += list(p)
    ##    print("unsorted")
    ##    for p in packets:
    ##        print(p)
    packets.sort(reverse=True, key=functools.cmp_to_key(compare_lists))
    ##    print("sorted")
    ##    for p in packets:
    ##        print(p)
    return (packets.index(divider_a) + 1) * (packets.index(divider_b) + 1)


########

if __name__ == "__main__":
    print("day13a", day13a("input13.txt"))
    print("day13b", day13b("input13.txt"))

########


def test_load_pairs():
    pairs = load_pairs("test13.txt")
    assert len(pairs) == 8

    assert pairs[0][0] == [1, 1, 3, 1, 1]
    assert pairs[0][1] == [1, 1, 5, 1, 1]
    assert pairs[3][0] == [[4, 4], 4, 4]
    assert pairs[5][0] == []
    assert pairs[6][0] == [[[]]]
    assert pairs[6][1] == [[]]


def test_compare_lists():
    # smaller = good
    assert compare_lists(1, 1) == 0
    assert compare_lists(10, 1) == -1
    assert compare_lists(1, 10) == 1

    # not using raw data, but testing examples
    assert compare_lists([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == 1
    assert compare_lists([[1], [2, 3, 4]], [[1], 4]) == 1
    assert compare_lists([9], [[8, 7, 6]]) == -1
    assert compare_lists([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == 1
    assert compare_lists([7, 7, 7, 7], [7, 7, 7]) == -1
    assert compare_lists([], [3]) == 1
    assert compare_lists([[[]]], [[]]) == -1
    assert (
        compare_lists(
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        )
        == -1
    )

    # extra
    assert (
        compare_lists([1, 1, 3, 1, 1], [1, 1, 5, 10, 100]) == 1
    )  # later doesn't matter


def test_day13a():
    assert day13a("test13.txt") == 13


def test_day13b():
    assert day13b("test13.txt") == 140
