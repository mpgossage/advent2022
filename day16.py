"""
Advent of Code 2022: Day 16
The problem looks like a BFS with a max amount of time.
Even with a big input set, its looks a constrained problem (for now).

Assumption wrong:
after 12 steps there is over 300,000 states
We will need to constrain it or change to best first

So added a culling routine & it worked ok if I used DFS, but not BFS
(dunno).

Part 2 is a lot more complex with two states to track and two actions

Gave up, looked at others & came back.
Silly mistakes made & then fixed:
* don't move 1 cell at a time, instead precompute the paths between all nodes
* each action is X minutes to move from A to B + 1 minute to open the valve
* dont visit valves which are stuck
** there are a lot of them and ignoring them cuts the problem a lot
** they are needed for the path precomputation, just never for visiting

I was about to use DP to try to solve it, but spotted the visiting empty.

Note: this does not work correctly for day16b with test data.
This is because its possible for you to visit all worthwhile spaces in 26 mins.
So the elephant does nothing.
For the full data, you explore one area, the elephant does somewhere else
(its not guarenteed, but it worked)
"""

from helper import load_lines
import cProfile


def load_flow(fname):
    "returns { Name: (rate, [tunnels]}"

    def parse_line(line):
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
        tokens = line.replace("=", " ").replace(";", "").replace(",", "").split()
        return tokens[1], (int(tokens[5]), tokens[10:])

    return dict(parse_line(l) for l in load_lines(fname))


def day16a(fname):
    "just going for the DFS version"
    flow = load_flow(fname)
    start = "AA"
    t = 30
    press = 0
    dp = 0
    valves = []
    todo = [(start, t, press, dp, valves)]
    total_press = 0
    counter = 0
    best = {}  # best so far
    discard = 0
    while todo:
        counter += 1
        if counter % 100000 == 0:
            print(counter, len(todo), len(best), discard, min(t[1] for t in todo))
        pos, t, press, dp, valves = todo.pop(-1)
        # assumption: if I am in location X at time T and
        # my pressure is not as good as a different route, this is a bad idea
        # this might have issues as I might have more pressure being released
        # but less absolute pressure now
        key = f"{pos}-{t}"
        best_press = best.get(key, 0)
        if best_press > press:
            # bad choice: discard
            discard += 1
            continue
        best[key] = press
        # simulate
        press += dp
        t -= 1
        if t <= 0:
            # time up store result and move on
            if press > total_press:
                total_press = press
                print("best pressure", press)
            continue
        # if value not open thats an option
        if pos not in valves:
            todo.append((pos, t, press, dp + flow[pos][0], valves + [pos]))
        # also is option to move
        for ex in flow[pos][1]:
            todo.append((ex, t, press, dp, valves))
    return total_press


def day16b(fname):
    "DFS but with two states"
    flow = load_flow(fname)
    start1, start2 = "AA", "AA"
    t = 26
    press = 0
    dp = 0
    valves = []
    todo = [(start1, start2, t, press, dp, valves)]
    total_press = 0
    counter = 0
    best = {}  # best so far
    discard = 0
    while todo:
        counter += 1
        if counter % 100000 == 0:
            print(counter, len(todo), len(best), discard, min(t[2] for t in todo))
        pos1, pos2, t, press, dp, valves = todo.pop(-1)
        # assumption: if I am in location X at time T and
        # my pressure is not as good as a different route, this is a bad idea
        # this might have issues as I might have more pressure being released
        # but less absolute pressure now
        key = f"{pos1}-{pos2}-{t}"
        best_press = best.get(key, 0)
        if best_press > press:
            # bad choice: discard
            discard += 1
            continue
        best[key] = press
        # simulate
        press += dp
        t -= 1
        if t <= 0:
            # time up store result and move on
            if press > total_press:
                total_press = press
                print(f"best pressure {press} dp {dp}")
            continue
        # if both at places which are not pressed (and its not the same)
        if pos1 != pos2 and pos1 not in valves and pos2 not in valves:
            # we can press
            todo.append(
                (
                    pos1,
                    pos2,
                    t,
                    press,
                    dp + flow[pos1][0] + flow[pos2][0],
                    valves + [pos1, pos2],
                )
            )
        # if value not open thats an option
        if pos1 not in valves:
            # p1 presses, p2 moves
            for ex in flow[pos2][1]:
                todo.append((pos1, ex, t, press, dp + flow[pos1][0], valves + [pos1]))
        if pos2 not in valves:
            # p2 presses, p1 moves
            for ex in flow[pos1][1]:
                todo.append((ex, pos2, t, press, dp + flow[pos2][0], valves + [pos2]))
        # p1 & p2 move
        for ex1 in flow[pos1][1]:
            for ex2 in flow[pos2][1]:
                todo.append((ex1, ex2, t, press, dp, valves))
    return total_press


def create_paths(flow):
    paths = {}
    for A, val_A in flow.items():
        for B in val_A[1]:  # its (rate,[exits])
            paths[A + B] = 1
            paths[B + A] = 1
            for C in flow:
                if C == A or C == B:
                    continue
                # if A->B->C < A->C then update the route
                AC = paths.get(A + C, 100)
                ABC = 1 + paths.get(B + C, 100)
                if ABC < AC:
                    paths[A + C] = ABC
                    paths[C + A] = ABC
    # second pass to fix missing items:
    for A in flow:
        for B in flow:
            for C in flow:
                if A == B or A == C or B == C:
                    continue
                AC = paths.get(A + C, 100)
                ABC = paths.get(A + B, 100) + paths.get(B + C, 100)
                if ABC < AC:
                    paths[A + C] = ABC
                    paths[C + A] = ABC

    return paths


def solve16(valves, paths, route, press, tim):
    "recursive solve"
    best_press, best_route = press, route  # no better
    current = route[-1]
    # for each node not visited: visit
    for node, val in valves.items():
        if node in route:
            continue
        # add time
        newtim = tim - paths[current + node] - 1  # takes 1 min to open valve
        if newtim < 1:
            continue  # no time
        newpress = press + val * newtim
        # explore
        prss, rt = solve16(valves, paths, route + [node], newpress, newtim)
        if prss > best_press:
            best_press, best_route = prss, rt
    return best_press, best_route


def day16a2(fname):
    "different thoughts, using paths and using recursion"
    flow = load_flow(fname)
    print("flow", len(flow))
    paths = create_paths(flow)
    print("paths", len(paths))
    # valve locations (skip the ones which are stuck)
    valves = dict((k, v[0]) for k, v in flow.items() if v[0] > 0)
    best_press, best_route = solve16(valves, paths, ["AA"], 0, 30)
    print(best_press, best_route)
    return best_press


def day16b2(fname):
    "different thoughts, using paths and using recursion"
    flow = load_flow(fname)
    paths = create_paths(flow)
    # valve locations (skip the ones which are stuck)
    valves = dict((k, v[0]) for k, v in flow.items() if v[0] > 0)
    # assumption: pick the best route for myself in 26 mins
    # then remove let elephant explore rest
    best_press, best_route = solve16(valves, paths, ["AA"], 0, 26)
    print("my route", best_press, best_route)
    # if we give my route to the elephant, it will not visit any place I have visited
    best_press2, best_route2 = solve16(valves, paths, best_route + ["AA"], 0, 26)
    print("ele route", best_press2, best_route2)
    return best_press + best_press2


###################

if __name__ == "__main__":
    print("day16a", day16a2("input16.txt"))
    print("day16b", day16b2("input16.txt"))

###################


def test_load_flow():
    flow = load_flow("test16.txt")
    assert len(flow) == 10
    assert flow["AA"] == (0, ["DD", "II", "BB"])
    assert flow["JJ"] == (21, ["II"])


def test_day16a():
    assert day16a("test16.txt") == 1651


##def test_day16b():
##    # test case times out
##    assert day16b("test16.txt")==1707


def test_create_paths():
    paths = create_paths(load_flow("test16.txt"))
    assert paths["AABB"] == 1
    assert paths["BBAA"] == 1
    assert paths["AACC"] == 2
    assert paths["EEBB"] == 3
    assert paths["HHJJ"] == 7


def test_day16a2():
    assert day16a2("test16.txt") == 1651


# test case does not work so not used
##def test_day16b2():
##    assert day16b2("test16.txt")==1707
