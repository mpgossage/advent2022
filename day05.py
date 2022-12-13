"""
Advent of Code 2022: day 5
This is going to be a fun day, just looking at the puzzle input!
Took about 1h, and a lot of that was the initial parsing.
As I was working through I foresaw what part B would be,
but I did not write code to support this kind of switch
"""

from helper import *


def parse_input(fname):
    """
    parses the input file and returns the stacks & the commands

    """
    lines = load_lines(fname)
    # find the empty line to mark the seperation between stacks and commands
    split_index = lines.index("")

    stacks = []
    # looking at the numeric line to determine how many stacks their are
    num_stacks = len(lines[split_index - 1].split())
    for s in range(num_stacks):
        stack = ""
        # looking from bottom/top to count the items
        for line in range(split_index - 2, -1, -1):
            # NB: arg2 is -1 as we want to reach 0
            # relying on character position
            c = lines[line][4 * s + 1]
            if c != " ":
                stack += c
        stacks.append(stack)

    commands = lines[split_index + 1 :]

    def parse_command(s):
        "turns 'move 1 from 2 to 1' into (1,2,1)"
        a = s.split()
        return (int(a[1]), int(a[3]), int(a[5]))

    commands = [parse_command(c) for c in commands]

    return stacks, commands


def apply_command(stacks, amount, from_idx, to_idx):
    result = stacks[:]
    for i in range(amount):
        v = result[from_idx][-1]
        result[from_idx] = result[from_idx][:-1]
        result[to_idx] = result[to_idx] + v
    return result


def apply_commands(stacks, commands):
    "applies the commands (converting from 1 index to 0 index)"
    result = stacks
    for c in commands:
        result = apply_command(result, c[0], c[1] - 1, c[2] - 1)
    return result


def day05a(fname):
    stacks, commands = parse_input(fname)
    result = apply_commands(stacks, commands)
    return "".join((s[-1] for s in result))


def apply_command2(stacks, amount, from_idx, to_idx):
    result = stacks[:]
    result[to_idx] = result[to_idx] + result[from_idx][-amount:]
    result[from_idx] = result[from_idx][:-amount]
    return result


def apply_commands2(stacks, commands):
    "applies the commands (converting from 1 index to 0 index)"
    result = stacks
    for c in commands:
        result = apply_command2(result, c[0], c[1] - 1, c[2] - 1)
    return result


def day05b(fname):
    stacks, commands = parse_input(fname)
    result = apply_commands2(stacks, commands)
    return "".join((s[-1] for s in result))


##################

if __name__ == "__main__":
    print("day05a", day05a("input05.txt"))
    print("day05b", day05b("input05.txt"))


##################


def test_parse_input():
    stacks, commands = parse_input("test05.txt")
    assert len(stacks) == 3
    assert stacks[0] == "ZN"
    assert stacks[1] == "MCD"
    assert len(commands) == 4
    assert commands[0] == (1, 2, 1)
    assert commands[3] == (1, 1, 2)


def test_apply_command():
    stacks = ["ABC", "DEF", "GHI"]
    assert apply_command(stacks, 1, 1, 0) == ["ABCF", "DE", "GHI"]


def test_apply_commands():
    stacks, commands = parse_input("test05.txt")
    result = apply_commands(stacks, commands)
    assert result == ["C", "M", "PDNZ"]


def test_day05a():
    assert day05a("test05.txt") == "CMZ"


def test_day05b():
    assert day05b("test05.txt") == "MCD"
