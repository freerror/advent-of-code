import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc

# Good luck and have fun: https://adventofcode.com/2022

input = aoc.get_inputs(day=8)[0]  # 0 example, 1 puzzle input
lines = input.splitlines()
print(lines)
