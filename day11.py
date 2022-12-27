"""
Advent of code 2022: day 11
Another very interesting day.
going to use simple classes for this

hit a major issue in part two.
600 rounds takes 0.7 seconds
700 rounds takes 4.2 seconds
800 rounds takes 27.4 seconds
Which suggests a serious issue.
There is not a big cpu or memory spike, just a big slowdown

Going to try a completely different approach. Failed & removed it.

Looked at https://chasingdings.com/2022/12/11/advent-of-code-day-11-monkey-in-the-middle/
The issue (which I failed to notice) was that python was hitting bignums rather than long ints
and this was causing all the issues.
The fix involves looking at the input data and noticing that all the checks are vs modulo
2,3,5,7,11,13,17 & 19
If you multiply them together its 9699690.
if X %2 ==0 then (X%9699690) %2 == 0, and so on for each of the other values
by using the modulo 9699690, you can stop the numbers geting too big
"""

from helper import load_lines
import time
import cProfile


class Monkey:
    "empty class which allows storing of any attributes"
    pass


def parse_equation(line):
    tokens = line.split()
    assert len(tokens) == 5
    assert tokens[0] == "new"
    assert tokens[1] == "="
    # so we have old+, old*
    assert tokens[2] == "old"
    if tokens[4] == "old":
        if tokens[3] == "+":
            return lambda x: x + x
        elif tokens[3] == "*":
            return lambda x: x * x
    else:
        val = int(tokens[4])
        if tokens[3] == "+":
            return lambda x: x + val
        elif tokens[3] == "*":
            return lambda x: x * val
    print("unhandled parsing", line)
    assert False


def load_monkeys(fname):
    lines = load_lines(fname)
    # going to be 7 lines per monkey
    monkeys = []
    for i in range((len(lines) + 1) // 7):
        m = Monkey()
        # line 0 "monkey X:" just ignore
        # line 1 "Starting items: 79, 98"
        items = lines[i * 7 + 1].split(":")[1]
        m.items = [int(i) for i in items.split(", ")]
        # line 2 "Operation: new = old + 6"
        operation = lines[i * 7 + 2].split(":")[1]
        m.fn = parse_equation(operation)
        # alternative version
        tokens = operation.split()
        m.op = tokens[3]
        m.op_item = tokens[4] == "old"
        if m.op_item == False:
            m.op_val = int(tokens[4])
        # line 3 "Test: divisible by 23"
        test = lines[i * 7 + 3].split()
        m.divisor = int(test[3])
        # line 4/5 "If true: throw to monkey 1"
        if_true = lines[i * 7 + 4].split()
        if_false = lines[i * 7 + 5].split()
        m.if_true = int(if_true[5])
        m.if_false = int(if_false[5])
        m.inspected = 0
        m.bored = 3

        monkeys.append(m)

    return monkeys


def process_item(monkey, item):
    "processes a single item, returns (item,throw_to)"
    # apply worry & bored
    if monkey.bored == 1:
        # modulo divisor to stop bignum issues
        item = monkey.fn(item) % 9699690
    else:
        item = monkey.fn(item) // monkey.bored
    if item % monkey.divisor == 0:
        return (item, monkey.if_true)
    else:
        return (item, monkey.if_false)


def process_round(monkeys):
    "applied the rules for monkeys"
    for m in monkeys:
        items = (process_item(m, item) for item in m.items)
        m.inspected += len(m.items)
        m.items = []
        for val, throw in items:
            monkeys[throw].items.append(val)


##        items = m.items
##        m.items = []
##        m.inspected += len(items)
##        for i in items:
##            val,throw = process_item(m,i)
##            monkeys[throw].items.append(val)


def day11a(fname):
    monkeys = load_monkeys(fname)
    for d in range(20):
        process_round(monkeys)
    inspections = sorted(m.inspected for m in monkeys)
    return inspections[-1] * inspections[-2]


def day11b(fname, rounds=20):
    monkeys = load_monkeys(fname)
    for m in monkeys:
        m.bored = 1  # don't divide
    for d in range(rounds):
        process_round(monkeys)
    inspections = sorted(m.inspected for m in monkeys)
    return inspections[-1] * inspections[-2]


##############


def perf_fn():
    monkeys = load_monkeys("test11.txt")
    for m in monkeys:
        m.bored = 1  # don't divide

    start = time.time()
    for d in range(10000):
        process_round(monkeys)
        if d % 100 == 0:
            taken = time.time() - start
            print(f"cycle {d} time {taken:.3}")


if __name__ == "__main__":
    print("day11a", day11a("input11.txt"))
    ##    cProfile.run('perf_fn()')
    print("day11b", day11b("input11.txt", 10000))

##############


def test_load_monkeys():
    monkeys = load_monkeys("test11.txt")

    # not checking every attribute
    assert len(monkeys) == 4
    assert monkeys[0].items == [79, 98]
    assert monkeys[1].items == [54, 65, 75, 74]
    # testing operation by just trying a single value
    assert monkeys[0].fn(1) == 19
    assert monkeys[1].fn(1) == 7
    assert monkeys[2].fn(1) == 1
    assert monkeys[3].fn(1) == 4
    # others
    assert monkeys[0].divisor == 23
    assert monkeys[0].if_true == 2
    assert monkeys[0].if_false == 3


def test_process_round():
    monkeys = load_monkeys("test11.txt")
    # sanity tests:
    assert len(monkeys) == 4
    assert len(monkeys[0].items) == 2
    assert len(monkeys[1].items) == 4
    assert len(monkeys[2].items) == 3
    assert len(monkeys[3].items) == 1

    process_round(monkeys)

    assert monkeys[0].items == [20, 23, 27, 26]
    assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]
    assert monkeys[2].items == []
    assert monkeys[3].items == []

    # 19 more rounds
    for i in range(19):
        process_round(monkeys)
    # check items & inspect levels
    assert monkeys[0].items == [10, 12, 14, 26, 34]
    assert monkeys[1].items == [245, 93, 53, 199, 115]
    assert monkeys[2].items == []
    assert monkeys[3].items == []
    assert monkeys[0].inspected == 101
    assert monkeys[1].inspected == 95
    assert monkeys[2].inspected == 7
    assert monkeys[3].inspected == 105


def test_day11a():
    assert day11a("test11.txt") == 10605
