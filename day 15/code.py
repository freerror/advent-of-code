from dataclasses import dataclass
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def in_x_ranges(covered_ranges, coord):
    x, _ = coord
    for rng in covered_ranges:
        min, max = rng
        if min[0] <= x <= max[0]:
            return True
    return False


def search_y_range(sensors, beacons, y):
    covered_ranges = []
    max_seen_x = 0
    min_seen_x = 0
    for s, b in zip(sensors, beacons):
        b_dist = abs(s[0] - b[0]) + abs(s[1] - b[1])
        max_x = s[0] + b_dist
        min_x = s[0] - b_dist
        y_dist = abs(s[1] - y)  # Distance from sensor to Y
        if y_dist > b_dist:
            # the target row is not in the range
            continue
        y_max_x = max_x - y_dist
        y_min_x = min_x + y_dist
        covered_ranges.append(((y_min_x, y), (y_max_x, y)))
        if y_max_x > max_seen_x:
            max_seen_x = y_max_x
        if y_min_x < min_seen_x:
            min_seen_x = y_min_x
    return min_seen_x, max_seen_x, covered_ranges


@dataclass
class SensorRange:
    centre: tuple[int, int]
    radius: int

    def get_boundary(self):
        y = self.centre[1] - self.radius - 1  # first pixel of outer border
        while True:
            y_dist = abs(self.centre[1] - y)  # Distance from sensor to Y
            if y_dist > (self.radius + 1):
                # the target row is no longer in the range
                break
            max_x = self.centre[0] + (self.radius + 1)
            min_x = self.centre[0] - (self.radius + 1)
            y_max_x = max_x - y_dist
            y_min_x = min_x + y_dist
            yield ((y_min_x, y), (y_max_x, y))
            y += 1

    def __eq__(self, other: tuple[int, int]):
        ox, oy = other
        sx, sy = self.centre
        dist = abs(sx - ox) + abs(sy - oy)
        if dist <= self.radius:
            return True
        return False


def get_ranges(sensors, beacons):
    ranges: list[SensorRange] = []
    for s, b in zip(sensors, beacons):
        b_dist = abs(s[0] - b[0]) + abs(s[1] - b[1])
        ranges.append(SensorRange((s[0], s[1]), b_dist))
    return ranges


def get_p1_solution(sensors, beacons):
    # y = 10
    y = 2_000_000
    min_seen_x, max_seen_x, covered_ranges = search_y_range(
        sensors, beacons, y
    )
    impossible = 0
    for x in range(min_seen_x, max_seen_x + 1):
        if in_x_ranges(covered_ranges, (x, y)):
            if not (x, y) in beacons and not (x, y) in sensors:
                impossible += 1
    return impossible


def get_p2_solution(sensors, beacons):
    max_xy = 4_000_000
    # max_xy = 20

    ranges = get_ranges(sensors, beacons)
    for range in ranges:
        for pair in range.get_boundary():
            for x, y in pair:
                sys.stdout.write(f"\r({x}, {y})")
                sys.stdout.flush()
                if 0 < x < max_xy and 0 < y < max_xy and (x, y) not in ranges:
                    return x * 4_000_000 + y
    assert False


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    lines = input.splitlines()
    sensors = []
    beacons = []
    for line in lines:
        sx = int(line.split("Sensor at x=")[1].split(", y=")[0])
        sy = int(line.split(", y=")[1].split(": ")[0])
        bx = int(line.split("is at x=")[1].split(", y=")[0])
        by = int(line.split("is at")[1].split(", y=")[1])
        sensors.append((sx, sy))
        beacons.append((bx, by))

    # part_1_solution = get_p1_solution(sensors, beacons)
    part_1_solution = "done"
    part_2_solution = get_p2_solution(sensors, beacons)

    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(15, solve_puzzle)
    # r = [SensorRange((10, 10), 50)]
    # print((3, 3) in r)
    # print((60, 3) in r)


if __name__ == "__main__":
    main()
