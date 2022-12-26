"""
Advent of code 2022: day 10
Its past Christmas, so this year I'm super slow, but its the challenge.

The simulator looks a little more than usual as it includes a timer.

part B is rather different and not easy to understand,
so I'm just going to try something and see if it gives the right answer.

I got the right answer, but I'm not confident on my method
"""

from helper import load_tokens


def simulate_cmd(cmds, pc, timer, xreg):
    """
    given list of commands, program counter, timer & x register
    simulates command
    returns pc, timer, xreg
    """
    cmd = cmds[pc][0]
    if cmd == "noop":
        return pc + 1, timer + 1, xreg
    if cmd == "addx":
        val = int(cmds[pc][1])
        return pc + 1, timer + 2, xreg + val
    assert False


def sim_cmds_for_signal_str(cmds, pc, timer, xreg, tgt_timer):
    """
    As per simulate_cmd() but will simulate until reached tgt_timer or later
    and returns the pc, timer, xreg, xreg at tgt timer
    """
    while timer < tgt_timer:
        old_xreg = xreg
        pc, timer, xreg = simulate_cmd(cmds, pc, timer, xreg)
    # return the value DURING the cycle (ie, the old value)
    return pc, timer, xreg, old_xreg


def day10a(fname):
    cmds = load_tokens(fname)
    pc, timer, xreg = 0, 0, 1
    sample_points = [20, 60, 100, 140, 180, 220]
    total = 0
    for s in sample_points:
        pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, s)
        total += s * result
    return total


def day10b(fname):
    cmds = load_tokens(fname)
    result = ""
    # very inefficient version, just from the start
    for t in range(240):
        if t % 40 == 0:
            result += "\n"
        _, _, _, xreg = sim_cmds_for_signal_str(cmds, 0, 0, 1, t + 1)
        # no idea why t%40, I though it was (t+1)%40
        if abs(t % 40 - xreg) <= 1:
            result += "#"
        else:
            result += "."
    return result


#########

if __name__ == "__main__":
    print("day10a", day10a("input10.txt"))
    print("day10b", day10b("input10.txt"))

#########


def test_simulate_cmds1():
    # trivial
    cmds = load_tokens("test10.txt")
    pc, timer, xreg = 0, 0, 1
    while pc < len(cmds):
        pc, timer, xreg = simulate_cmd(cmds, pc, timer, xreg)
    assert pc == 3
    assert timer == 5
    assert xreg == -1


def test_sim_cmds_for_signal_str():
    cmds = load_tokens("test10b.txt")
    pc, timer, xreg = 0, 0, 1
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 20)
    assert result == 21
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 60)
    assert result == 19
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 100)
    assert result == 18
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 140)
    assert result == 21
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 180)
    assert result == 16
    pc, timer, xreg, result = sim_cmds_for_signal_str(cmds, pc, timer, xreg, 220)
    assert result == 18


def test_day10a():
    assert day10a("test10b.txt") == 13140


# no test for day10b, its done by eye
