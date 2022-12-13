import sys
import math
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils import letters_to_numbers as letters
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def path_find(start, end, topo):
    sx, sy = start
    ex, ey = end
    queue = [start]
    x_cols = len(topo[0])
    y_rows = len(topo)
    steps = [[math.inf] * x_cols for _ in range(y_rows)]
    steps[sy][sx] = 0

    while queue:
        cx, cy = queue.pop(0)

        # check all neighbor directions
        for ax, ay in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = dest = (ax + cx, ay + cy)
            if (
                0 <= nx < x_cols
                and 0 <= ny < y_rows
                and steps[ny][nx] == math.inf
                and topo[ny][nx] - topo[cy][cx] <= 1
            ):
                steps[ny][nx] = steps[cy][cx] + 1
                queue.append(dest)

    return steps[ey][ex]


def print_path(steps, topo):
    lines = [["." for _ in range(len(topo[0]))] for _ in range(len(topo))]
    for x, y in steps:
        lines[y][x] = "#"
    [print(line) for line in lines]


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    lines = input.splitlines()
    topo = []
    start = (0, 0)
    end = (0, 0)
    for y, row in enumerate(lines):
        topo_row = []
        for x, e in enumerate(row):
            if e == "S":
                start = (x, y)
                topo_row.append(0)
            elif e == "E":
                end = (x, y)
                topo_row.append(25)
            else:
                topo_row.append(letters[e])
        topo.append(topo_row)

    # pathfinding

    part_1_solution = path_find(start, end, topo)

    possible_starts = []
    for y, row in enumerate(topo):
        for x, e in enumerate(row):
            if e == 0:
                possible_starts.append((x, y))
    distances = [path_find(start, end, topo) for start in possible_starts]
    part_2_solution = min(distances)
    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(12, solve_puzzle)


if __name__ == "__main__":
    main()
