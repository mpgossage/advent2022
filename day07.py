"""
Advent of Code 2022: day 7
Oh wow, today looks interesting.
Not mathematically hard, just a challenge to parse.

Turns out I'm very rusty on recursion and so my getting directories too much longer than it should

There was also a bug in my directory adding code which broke everything.

This too much too long, several hours.
"""

from helper import *


def parse_directory(fname):
    tree = {}
    path = []
    lines = load_lines(fname)
    while lines:
        l = lines.pop(0)
        ##        print(l)
        if l == "$ ls":
            # list directory
            d = []
            while len(lines) > 0 and lines[0][0] != "$":
                d.append(lines.pop(0))
            tr = convert_to_directory(d)
            ##            print("current dir",tr)
            # add to the correct loction
            if len(path) == 0:
                tree = tr
            else:
                ##                print("add", tree, path)
                tree_to_add, path_to_add = tree, path[:]
                while len(path_to_add) > 1:
                    tree_to_add = tree_to_add[path_to_add[0]]
                    path_to_add.pop(0)
                tree_to_add[path_to_add[0]] = tr
        else:
            tokens = l.split()
            if tokens[2] == "..":
                path = path[:-1]
            elif tokens[2] == "/":
                path = []
            else:
                path.append(tokens[2])
    ##            print("path", path)
    return tree


def convert_to_directory(lines):
    result = {}
    for l in lines:
        a, b = l.split()
        if a == "dir":
            result[b] = {}
        else:
            result[b] = int(a)
    return result


def _get_directory_sizes(tree, result):
    total = 0
    # add all items up
    for k, v in tree.items():
        if isinstance(v, int):
            total += v
        else:
            # tree so recurse
            total += _get_directory_sizes(v, result)
    result.append(total)
    return total


def get_directory_sizes(tree):
    result = []
    _get_directory_sizes(tree, result)
    return result


def day07a(fname):
    sizes = get_directory_sizes(parse_directory(fname))
    return sum((sz for sz in sizes if sz <= 100000))


def day07b(fname):
    sizes = get_directory_sizes(parse_directory(fname))
    total_size, required_size = 70000000, 30000000
    used_size = max(sizes)
    current_space = total_size - used_size
    amount_to_delete = required_size - current_space
    return min((sz for sz in sizes if sz >= amount_to_delete))


###########################

if __name__ == "__main__":
    ##    print("day07a", day07a("test07.txt"))
    print("day07a", day07a("input07.txt"))
    print("day07b", day07b("input07.txt"))

###########################


def test_convert_to_directory():
    d = convert_to_directory("dir a,14848514 b.txt,8504156 c.dat,dir d".split(","))
    assert len(d) == 4
    assert d["a"] == {}
    assert d["b.txt"] == 14848514
    assert d["c.dat"] == 8504156
    assert d["d"] == {}


def test_parse_directory():
    d = parse_directory("test07.txt")
    assert len(d) == 4
    assert len(d["a"]) == 4
    assert len(d["a"]["e"]) == 1
    assert d["a"]["e"]["i"] == 584
    assert len(d["d"]) == 4


def test_get_directory_sizes():
    d = parse_directory("test07.txt")
    sizes = get_directory_sizes(d)
    assert len(sizes) == 4
    assert 584 in sizes
    assert 94853 in sizes
    assert 24933642 in sizes
    assert 48381165 in sizes


def test_day07a():
    assert day07a("test07.txt") == 95437


def test_day07b():
    assert day07b("test07.txt") == 24933642
