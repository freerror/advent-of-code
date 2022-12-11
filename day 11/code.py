import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    lines = input.splitlines()

    # WORK HERE!

    part_1_solution = "TBC"
    part_2_solution = "TBC"
    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(11, solve_puzzle)


if __name__ == "__main__":
    main()
