from collections import deque
from dataclasses import dataclass, field
import re
import functools
import sys
from pathlib import Path
from typing import FrozenSet


sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbor_names: list[str]
    neighbors: list["Valve"] = field(default_factory=list)

    def __lt__(self, other: "Valve"):
        return self.flow_rate < other.flow_rate

    def __gt__(self, other: "Valve"):
        return self.flow_rate > other.flow_rate

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


def parse_input(input_str):
    valves: dict[str, Valve] = {}
    for line in input_str.strip().split("\n"):
        match = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)",
            line,
        )
        if match:
            name, flow_rate, neighbors_str = match.groups()
            flow_rate = int(flow_rate)
            neighbors = neighbors_str.split(", ")
            valves[name] = Valve(name, flow_rate, neighbors)
    for v in valves.values():
        v.neighbors = [valves[n] for n in v.neighbor_names]
    return valves["AA"], frozenset(valves.values())


@functools.cache
def calc_pressure(steps):
    new_pressure = 0
    on = set()
    for v in steps:
        for o in on:
            new_pressure += o.flow_rate
        if v[0] not in on and v[1] == 1:
            on.add(v[0])
    return new_pressure


@functools.cache
def search(start: Valve, valves: FrozenSet, time_limit=30):
    """Breadth first search approach (incomplete, doesn't work)"""
    actions: tuple[Valve, ...]
    total_valves = len(valves)
    seen = {}
    # each item in queue contains:
    # valve, time, pressure, sequence of valves
    horizon = deque([(start, 0, ())])

    while horizon:
        curr, time, actions = horizon.popleft()

        if seen.get((curr, time, actions)):
            continue

        if time == time_limit and actions:
            yield actions, calc_pressure(actions)
            continue
        if time > time_limit:
            break

        sys.stdout.write(f"\rtime={time} queue={len(horizon)}")
        sys.stdout.flush()

        # turn on
        # if flow rate > 0 and not already turned on
        if curr.flow_rate > 0 and (curr, 1) not in actions:
            new_action = actions + ((curr, 1),)
        else:
            new_action = actions + ((curr, 0),)

        # move
        for n in curr.neighbors:
            # don't stay or backtrack if there are more valves to be opened
            last = actions[-1][0] if actions else curr
            if not (
                n in (curr, last)
                and len(set(a for a in actions if a[1] == 1)) < total_valves
            ):
                # staying at the current valve is valid
                next_ = (n, time + 1, new_action)
                horizon.append(next_)  # type: ignore

        seen[(curr, time, actions)] = True


@functools.cache
def recurse_search(on: frozenset[Valve], curr: Valve, time_left=30):
    """Recursive BFS"""
    if time_left <= 0:
        return 0

    best = 0

    for valve in curr.neighbors:
        res_max = recurse_search(on, valve, time_left - 1)
        best = max(best, res_max)

    if curr not in on and curr.flow_rate > 0 and time_left > 0:
        turned_on = set(on)
        turned_on.add(curr)
        time_left -= 1
        new_sum = time_left * curr.flow_rate

        for valve in curr.neighbors:
            res_max = recurse_search(
                frozenset(turned_on), valve, time_left - 1
            )
            new_pressure = new_sum + res_max
            if new_pressure > best:
                best = new_pressure
            best = max(best, new_pressure)

    return best


@functools.cache
def dual_recurse_search(on: frozenset[Valve], curr: Valve, time_left=30):
    """Recursive search with a friend"""

    if time_left <= 0:
        # Searcher B
        return recurse_search(on, curr, 26)

    best = 0
    for valve in curr.neighbors:
        res_max = dual_recurse_search(on, valve, time_left - 1)
        best = max(best, res_max)

    if curr not in on and curr.flow_rate > 0 and time_left > 0:
        turned_on = set(on)
        turned_on.add(curr)
        time_left -= 1
        new_sum = time_left * curr.flow_rate

        for valve in curr.neighbors:
            res_max = dual_recurse_search(
                frozenset(turned_on), valve, time_left - 1
            )
            new_pressure = new_sum + res_max
            best = max(best, new_pressure)

    return best


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    start, _ = parse_input(input)

    return (
        recurse_search(frozenset(), start),
        dual_recurse_search(frozenset(), start, time_left=26),
    )


def main():
    aoc.solve_day(16, solve_puzzle)


if __name__ == "__main__":
    main()
