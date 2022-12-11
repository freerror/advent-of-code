from dataclasses import dataclass
from itertools import product
import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def parse_monkeys(lines: list[str]):
    monkeys: list[Monkey] = []
    for i in range(len(lines)):
        if lines[i].startswith("Monkey"):
            items = [int(w) for w in lines[i + 1].split(":")[1].split(", ")]
            pre_mod = lines[i + 2].split(":")[1]
            mod = 0
            op = ""
            sqr = False
            if "*" in pre_mod:
                pre_mod = pre_mod.split("* ")[1]
                if pre_mod == "old":
                    sqr = True
                else:
                    mod = int(pre_mod)
                op = "*"
            elif "+" in pre_mod:
                pre_mod = pre_mod.split("+ ")[1]
                if pre_mod == "old":
                    sqr = True
                else:
                    mod = int(pre_mod)
                op = "+"
            test = int(lines[i + 3].split("by ")[1])
            dest_1 = int(lines[i + 4].split("monkey ")[1])
            dest_2 = int(lines[i + 5].split("monkey ")[1])
            monkeys.append(
                Monkey(
                    items=items,
                    sqr=sqr,
                    worry_op=op,
                    worry_mod=mod,
                    test_divisor=test,
                    dest=(dest_1, dest_2),
                )
            )
    return monkeys


@dataclass
class Monkey:
    items: list[int]
    sqr: bool
    worry_op: str
    worry_mod: int
    test_divisor: int
    dest: tuple[int, int]
    volume: int = 0

    def do_turn(
        self, monkeys: list["Monkey"], relief_divisor=1, common_divisor=0
    ):
        new_items: list[int] = []
        destinations = []
        for item in self.items:
            self.volume += 1
            new_item = item
            if self.sqr:
                if self.worry_op == "+":
                    new_item = item + item
                elif self.worry_op == "*":
                    new_item = item * item
            else:
                if self.worry_op == "+":
                    new_item = item + self.worry_mod
                elif self.worry_op == "*":
                    new_item = item * self.worry_mod
            new_item = new_item // relief_divisor
            if common_divisor:
                new_item = new_item % common_divisor
            new_items.append(new_item)
            if new_item % self.test_divisor == 0:
                destinations.append(self.dest[0])
            else:
                destinations.append(self.dest[1])
        self.items = []
        pass_items(new_items, monkeys, destinations)
        return destinations


def pass_items(
    items: list[int], monkeys: list[Monkey], destinations: list[int]
):
    for item, dest in zip(items, destinations):
        monkeys[dest].items.append(item)


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    lines = input.splitlines()

    # Part 1
    monkeys = parse_monkeys(lines)

    rounds = range(0, 20)

    for _ in rounds:
        for monkey in monkeys:
            monkey.do_turn(monkeys, relief_divisor=3)

    volumes = []
    for monkey in monkeys:
        volumes.append(monkey.volume)
    volumes = sorted(volumes)
    part_1_solution = volumes[-1] * volumes[-2]

    # Part 2
    monkeys = parse_monkeys(lines)

    # Used to reduce memory usage
    all_test_divisors = []
    for monkey in monkeys:
        all_test_divisors.append(monkey.test_divisor)
    common_divisor = math.prod(all_test_divisors)

    rounds = range(0, 10000)

    for _ in rounds:
        for monkey in monkeys:
            monkey.do_turn(monkeys, common_divisor=common_divisor)
    volumes = []
    for monkey in monkeys:
        volumes.append(monkey.volume)
    volumes = sorted(volumes)
    part_2_solution = volumes[-1] * volumes[-2]

    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(11, solve_puzzle)


if __name__ == "__main__":
    main()
