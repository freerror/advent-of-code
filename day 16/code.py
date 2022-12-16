from collections import deque
from dataclasses import dataclass, field
import re
import sys
from pathlib import Path


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


def find_max_pressure(start: Valve, time_limit):
    queue = [start]
    on = []
    elapsed = 0
    pressure = 0

    while queue and elapsed < time_limit:
        cur_valve = queue.pop(0)
        if cur_valve.flow_rate > 0 and cur_valve not in on:
            on.append(cur_valve)
            # turning a valve on costs 1
            elapsed += 1
        for valve in on:
            pressure += valve.flow_rate

        options = cur_valve.neighbors
        n_valve = max([n for n in options if n not in on])

        # getting to a new dest costs 1
        queue.append(n_valve)
        elapsed += 1
    return "Barf"


def parse_input(input_str):
    valves = {}
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
        v: Valve
        v.neighbors = [valves[n] for n in v.neighbor_names]
    return valves["AA"]


def search(start: Valve, time_limit=30):
    time = 0
    seen = {}
    curr = start
    pressure = int(0)
    horizon = deque([(curr, time, frozenset())])
    while horizon:
        curr, time, on = horizon.popleft()

        if seen.get((curr, time, on)):
            continue

        if time == time_limit:
            yield curr, time, pressure

        seen[(curr, time, on)] = True

        # move
        for n in curr.neighbors:
            horizon.append((n, time + 1, on))  # type: ignore

        # turn on
        if curr not in on:
            horizon.append((curr, time + 1, on | frozenset([curr])))  # type: ignore


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    start = parse_input(input)

    for x in search(start):
        print(x)


def main():
    aoc.solve_day(16, solve_puzzle)


if __name__ == "__main__":
    main()
