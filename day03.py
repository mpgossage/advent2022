"""
Advent of Code 2022: day 3
Time taken ~20 mins

Overall quite simple, its a shame that I did not anticipate part B,
so I could not reuse a lot of code
"""
import pytest
from helper import *


def check_rucksack(sack):
    ln = len(sack) // 2
    sacka, sackb = sack[:ln], sack[ln:]
    dup = {c for c in sacka if c in sackb}
    return dup


def get_priority(item):
    if item.islower():
        return 1 + ord(item) - ord("a")
    if item.isupper():
        return 27 + ord(item) - ord("A")


def get_priorities(items):
    return sum(get_priority(i) for i in items)


def day03a(fname):
    sacks = load_lines(fname)
    totals = sum(get_priorities(check_rucksack(sack)) for sack in sacks)
    return totals


def find_dup3(sacka, sackb, sackc):
    return {i for i in sacka if i in sackb and i in sackc}


def day03b(fname):
    sacks = load_lines(fname)
    num_sacks = len(sacks)
    totals = 0
    for i in range(num_sacks // 3):
        team = sacks[i * 3 : i * 3 + 3]
        totals += get_priorities(find_dup3(team[0], team[1], team[2]))
    return totals


###############


if __name__ == "__main__":
    print("day03a", day03a("input03.txt"))
    print("day03b", day03b("input03.txt"))


###############


def test_check_rucksack():
    assert check_rucksack("aaabbb") == set()
    assert check_rucksack("aaaAAA") == set()
    assert check_rucksack("aaaAAa") == {"a"}
    assert check_rucksack("vJrwpWtwJgWrhcsFMMfFFhFp") == {"p"}


def test_get_priority():
    assert get_priority("a") == 1
    assert get_priority("z") == 26
    assert get_priority("A") == 27
    assert get_priority("Z") == 52


def test_day03a():
    assert day03a("test03.txt") == 157


def test_day03b():
    assert day03b("test03.txt") == 70
