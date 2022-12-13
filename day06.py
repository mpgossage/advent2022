"""
Advent of code day 6
Less than 30 minutes for this one,
I was able to modify my part a code to support part b with no issue
"""
from helper import *


def find_marker(s, marker_ln=4):
    ln = len(s)
    for i in range(ln + 1 - marker_ln):
        sub = s[i : i + marker_ln]
        # is this unique? use a set to test simply
        if len(set(sub)) == marker_ln:
            return i + marker_ln
    assert False


def day06a(fname):
    lines = load_lines(fname)
    return find_marker(lines[0])


def day06b(fname):
    lines = load_lines(fname)
    return find_marker(lines[0], 14)


###########


if __name__ == "__main__":
    print("day06a", day06a("input06.txt"))
    print("day06b", day06b("input06.txt"))

###########


def test_find_marker():
    assert find_marker("abcd") == 4
    assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11


def test_day06a():
    assert day06a("test06.txt") == 7


def test_find_marker2():
    assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
