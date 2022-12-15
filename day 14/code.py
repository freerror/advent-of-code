import re
import sys
from pathlib import Path
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def can_move(dest, wall_rocks, floor_level=None):
    dx, dy = dest
    if floor_level and dy == floor_level:
        return False
    elif (dx, dy) in wall_rocks:
        return False
    return True


def parse_rocks(rock_walls):
    wall_rocks = []
    for wall in rock_walls:
        i = -1
        # append the first rock for each wall
        wall_rocks.append((wall[0][0], wall[0][1]))
        for x, y in wall:
            i += 1
            try:
                dist_x = wall[i + 1][0] - x
                dist_y = wall[i + 1][1] - y
                step_x = (1 if dist_x > 0 else -1) if dist_x else 0
                step_y = (1 if dist_y > 0 else -1) if dist_y else 0
                amount = max(abs(dist_x), abs(dist_y))
                for j in range(1, amount + 1):
                    wall_rocks.append((x + (step_x * j), y + (step_y * j)))
            except IndexError:
                break
    return wall_rocks


def plot_animation(wall_rocks, sand):
    x = []
    y = []
    sx = []
    sy = []
    for a, b in wall_rocks:
        x.append(a)
        y.append(b)
    for a, b in sand:
        sx.append(a)
        sy.append(b)

    fig = plt.figure()
    plt.xlim(300, 700)
    plt.ylim(0, 170)
    plt.axis("equal")
    plt.gca().invert_yaxis()
    (graph,) = plt.plot(x, y, "s")
    (graph_2,) = plt.plot([], [], "s")

    def animate(i):
        graph_2.set_data(sx[: i + 1], sy[: i + 1])
        return graph

    ani = FuncAnimation(fig, animate, frames=23610, interval=0.01)

    plt.show()


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    rock_walls = [
        [[int(a) for a in p.split(",")] for p in r.split(" -> ")]
        for r in input.splitlines()
    ]
    wall_rocks = parse_rocks(rock_walls)
    sand = []
    blocked = set(wall_rocks)
    floor_level = max([r[1] for r in wall_rocks]) + 2
    # # part 1
    # floor_level = None
    sand_src = (500, 0)

    i = 0
    unit = sand_src
    # check = 0
    while True:
        # # Part 1
        # if check > 1000:
        #     break
        # time.sleep(0.1)
        dest = (unit[0], unit[1] + 1)
        if can_move(dest, blocked, floor_level):
            # print(f"move to {dest}")
            unit = dest
            # check += 1
            continue
        else:
            dest = (dest[0] - 1, dest[1])
        if can_move(dest, blocked, floor_level):
            # print(f"move to {dest}")
            unit = dest
            # check += 1
            continue
        else:
            dest = (dest[0] + 2, dest[1])
        if can_move(dest, blocked, floor_level):
            # print(f"move to {dest}")
            unit = dest
            # check += 1
            continue
        else:
            # print(f"stopped at {unit}")
            # Part 2
            i += 1
            if unit == sand_src:
                break
            blocked.add(unit)
            sand.append(unit)
            unit = sand_src
            # check = 0

    part_1_solution = "done"
    part_2_solution = i

    plot_animation(wall_rocks, sand)

    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(14, solve_puzzle)


if __name__ == "__main__":
    main()
