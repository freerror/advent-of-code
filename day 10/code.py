from dataclasses import dataclass, field
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc

# Good luck and have fun: https://adventofcode.com/2022

input = aoc.get_inputs(day=10)[1]  # 0 example, 1 puzzle input
lines = input.splitlines()


@dataclass
class CRT:
    instructions: list[tuple[str, int]] = field(default_factory=list)
    x = 1
    cycle = 0
    row = 0
    p1_rows = (20, 60, 100, 140, 180, 220)
    p2_rows = (40, 80, 120, 160, 200, 240)
    crt_rows: list = field(default_factory=list)
    signal_strengths: list = field(default_factory=list)
    check: list = field(default_factory=list)

    def __post_init__(self):
        for _ in range(0, 6):
            self.crt_rows.append(["."] * 40)

    def check_cycle(self):
        if self.cycle in self.p1_rows:
            self.signal_strengths.append(self.x * self.cycle)
            self.check.append((self.cycle, self.x))
        if self.cycle in self.p2_rows:
            self.row += 1

    def perform_cycle(self, type: str, value=None):
        if type == "noop" or type == "addx_0":
            self.cycle += 1
            self.check_cycle()
        elif type == "addx_1":
            self.cycle += 1
            self.check_cycle()
            self.x += value or 0

        col = self.cycle - (self.row * 40)
        pixels = (self.x - 1, self.x, self.x + 1)
        if col in pixels:
            self.crt_rows[self.row][col] = "#"

    def parse_instructions(self, lines: list[str]):
        for line in lines:
            if line.startswith("noop"):
                self.instructions.append(("noop", 0))
                continue
            elif line.startswith("addx"):
                _, v = line.split()
                self.instructions.append(("addx", int(v)))
        for instr, value in self.instructions:
            if instr == "noop":
                self.perform_cycle("noop")
            elif instr == "addx":
                self.perform_cycle("addx_0")
                self.perform_cycle("addx_1", value)

    def render(self):
        output = ""
        for row in self.crt_rows:
            output += "".join(row) + "\n"
        return output


def main():
    crt = CRT()
    crt.parse_instructions(lines)
    print(crt.check)
    print(sum(crt.signal_strengths))
    print(crt.render())


if __name__ == "__main__":
    main()
