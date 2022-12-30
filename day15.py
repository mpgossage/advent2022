"""
Advent of code 2022: Day15

Another interesting item.
Half of me shouts "grid and visualise it"
The other half shouts "y=2,000,000, thats going to be huge"

A quick glance at the input shows x going between 10878-3999794
This is not a grid questions, we will need to do it abstract.

Failed on first attempt as I did not do the discard :-(

Part two also caused issues because of performance.
Its taking almost 1 second per line, with 4 million lines well...

Added a new feature to helper for a packed range of numbers.
Solved the issue in ~40 seconds, which is not too bad.

Looking at https://chasingdings.com/2022/12/15/advent-of-code-day-15-beacon-exclusion-zone/
gave me some other ideas, but I'm happy with my solution.
"""

from helper import load_lines, remove_set
import time
import cProfile


def load_sensors(fname):
    "returns [(sx,sy,bx,by)...]"

    def parse_line(line):
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
        line = line.replace("x=", "").replace(", y=", " ").replace(":", "")
        tokens = line.split()
        return (int(tokens[2]), int(tokens[3]), int(tokens[8]), int(tokens[9]))

    return [parse_line(l) for l in load_lines(fname)]


def determine_clear_zone(sensor, y):
    """
    Given sx,sy,bx,by and the Y value we care about
    determine the min-x,max-x (inclusive) which the sensor knows is clear
    returns None or tuple
    """
    sx, sy, bx, by = sensor
    dist = abs(sx - bx) + abs(sy - by)
    # we know that there is no beacons within dist of the sensor
    # (other than the known one)
    size = dist - abs(sy - y)  # number of units either side
    if size < 0:
        return None
    return (sx - size, sx + size)


def day15a(fname, yval):
    # keep it simple: put into a set to count the unique elements
    result = set()
    sensors = load_sensors(fname)
    for sensor in sensors:
        r = determine_clear_zone(sensor, yval)
        ##        print(sensor,r)
        if r:
            result |= set(range(r[0], r[1] + 1))

    for sensor in sensors:
        # remove any beacons which occur in this line
        _, _, bx, by = sensor
        if by == yval:
            ##            print("discard",bx,by)
            result.discard(bx)

    ##    print(result)
    return len(result)


def day15b(fname, limits):
    # again a set, but its going to be rather more complex
    sensors = load_sensors(fname)
    start = time.time()
    ##    for y in range(limits+1):
    for y in range(30):
        if y % 10 == 0:
            print(y, time.time() - start)
        line = set(range(limits + 1))  # 0..limits(inclusive)
        ##        print(f"y={y} pre-line={line}")
        for sensor in sensors:
            res = determine_clear_zone(sensor, y)
            if res:
                ##                print(f"removing {res[0]}...{res[1]}")
                line -= set(range(res[0], res[1] + 1))  # remove all the items
                if len(line) < 1:
                    break
        ##        print(f"y={y} end-line={line}")
        if len(line) > 0:
            x = line.pop()  # according to spec there should only be one item
            ##            print("found",x,y)
            return x * 4000000 + y


def day15b2(fname, limits):
    # not using a set, 4 million item sets break stuff
    sensors = load_sensors(fname)
    start = time.time()
    for y in range(limits + 1):
        if y % 100000 == 0:
            print(f"y={y} {time.time()-start}")
        # line is a list of (lower,upper) limits
        line = [(0, limits)]
        for sensor in sensors:
            res = determine_clear_zone(sensor, y)
            if res:
                # remove items listed
                line = remove_set(line, res[0], res[1])
                if len(line) == 0:
                    break
        if len(line) > 0:
            x = line[0][0]
            print("found", line, x)
            return x * 4000000 + y


##############


def perf_fn():
    print("day15b", day15b("input15.txt", 4000000))


if __name__ == "__main__":
    ##    print("day15a_test",day15a("test15.txt",10))
    print("day15a", day15a("input15.txt", 2000000))
    print("day15b_test", day15b("test15.txt", 20))
    print("day15b2_test", day15b2("test15.txt", 20))
    ##    print("day15b",day15b("input15.txt",4000000))
    ##    cProfile.run('perf_fn()')
    print("day15b2", day15b2("input15.txt", 4000000))

##############


def test_load_sensors():
    sensors = load_sensors("test15.txt")
    assert len(sensors) == 14
    assert sensors[0] == (2, 18, -2, 15)
    assert sensors[13] == (20, 1, 15, 3)


def test_determine_clear_zone():
    # example sensor
    sensor = (8, 7, 2, 10)
    # for y =7 it should cover -1,17
    assert determine_clear_zone(sensor, 7) == (-1, 17)
    # for y=-2, should only clear x=8, also for y=16
    assert determine_clear_zone(sensor, -2) == (8, 8)
    assert determine_clear_zone(sensor, 16) == (8, 8)
    # for y=-3 & y=17 no info
    assert determine_clear_zone(sensor, -3) == None
    assert determine_clear_zone(sensor, 17) == None


def test_day15a():
    assert day15a("test15.txt", 10) == 26


def test_day15b():
    assert day15b("test15.txt", 20) == 56000011


def test_day15b2():
    assert day15b2("test15.txt", 20) == 56000011
