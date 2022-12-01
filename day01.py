import pytest


def parse_input(fname):
    results = []
    with open(fname) as f:
        t = []
        for line in f:
            line = line.strip()
            if len(line) == 0:
                results.append(t)
                t = []
            else:
                t.append(int(line))
        results.append(t)
    return results


def day01a(fname):
    elves = parse_input(fname)
    totals = (sum(e) for e in elves)
    return max(totals)


def day01b(fname):
    elves = parse_input(fname)
    totals = [sum(e) for e in elves]
    totals.sort(reverse=True)
    return sum(totals[0:3])


################################################################
if __name__ == "__main__":
    ##    print(parse_input("test01.txt"))
    print("day01a", day01a("input01.txt"))
    print("day01b", day01b("input01.txt"))

################################################################


def test_parse():
    results = parse_input("test01.txt")
    assert len(results) == 5
    assert len(results[0]) == 3
    assert results[0][0] == 1000
    assert len(results[4]) == 1


def test_day01a():
    assert day01a("test01.txt") == 24000


def test_day01b():
    assert day01b("test01.txt") == 45000
