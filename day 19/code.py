from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
import math
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022
@dataclass
class Bot(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class Recipe:
    type: Bot
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclass
class BP:
    idx: int
    recipes: list[Recipe]


def parse_input(input: str):
    lines = input.splitlines()
    bps = []
    pattern = re.compile(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    for line in lines:
        match = pattern.match(line)
        if match:
            (
                idx,
                ore_ore,
                clay_ore,
                obs_ore,
                obs_clay,
                geo_ore,
                geo_obs,
            ) = match.groups()
            bps.append(
                BP(
                    int(idx),
                    [
                        Recipe(Bot.ORE, int(ore_ore)),
                        Recipe(Bot.CLAY, int(clay_ore)),
                        Recipe(
                            Bot.OBSIDIAN, ore=int(obs_ore), clay=int(obs_clay)
                        ),
                        Recipe(
                            Bot.GEODE, ore=int(geo_ore), obsidian=int(geo_obs)
                        ),
                    ],
                )
            )
    return bps


Workers = namedtuple("Workers", ["ore", "clay", "obsidian", "geode"])
Bank = namedtuple("Bank", ["ore", "clay", "obsidian", "geode"])


def dfs(bp: BP, max_spend, cache, time, bots: Workers, bank: Bank):
    if time == 0:
        return bank[3]

    key = tuple([time, *bots, *bank])
    if key in cache:
        return cache[key]

    max_val = bank[3] + bots[3] * time

    for recipe in bp.recipes:
        if recipe.type != Bot.GEODE and (
            recipe.ore >= max_spend["ore"]
            or recipe.clay >= max_spend["clay"]
            or recipe.obsidian >= max_spend["obsidian"]
        ):
            continue

        wait = 0
        for recipe_qty, bank_qty, workers in (
            (recipe.ore, bank.ore, bots.ore),
            (recipe.clay, bank.clay, bots.clay),
            (recipe.obsidian, bank.obsidian, bots.obsidian),
        ):
            if workers == 0:
                break
            wait = max(wait, math.ceil((recipe_qty - bank_qty) / workers))
        else:
            time_remaining = time - wait - 1
            if time_remaining <= 0:
                continue
            bots_ = [x for x in bots]
            bank_ = [
                qty + btype * (wait + 1) for qty, btype, in zip(bank, bots)
            ]
            for t, amount in enumerate(
                (recipe.ore, recipe.clay, recipe.obsidian)
            ):
                bank_[t] -= amount
            bots_[int(recipe.type.value)] += 1
            for i in range(3):
                bank_[i] = min(bank_[i], max_spend[i] * time_remaining)
            bank_ = Bank(bank_[0], bank_[1], bank_[2], bank_[3])
            bots_ = Workers(bots_[0], bots_[1], bots_[2], bots_[3])
            max_val = max(
                max_val,
                dfs(bp, max_spend, cache, time_remaining, bots_, bank_),
            )

    cache[key] = max_val
    return max_val


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    bps = parse_input(input)
    total = 0
    for bp in bps:
        max_spend = {}
        for recipe in bp.recipes:
            max_spend["ore"] = max(recipe.ore, max_spend.get("ore", 0))
            max_spend["clay"] = max(recipe.clay, max_spend.get("clay", 0))
            max_spend["obsidian"] = max(
                recipe.obsidian, max_spend.get("obsidian", 0)
            )
        v = dfs(bp, max_spend, {}, 24, Workers(1, 0, 0, 0), Bank(0, 0, 0, 0))
        total += bp.idx * v

    return total, 0

    # Example build process:
    # ore(pre)->clay->clay->clay->obsidian->clay->obsidian->geode->geode
    # borrowed ideas from hyper-neutrino:
    # - optimize around max spend and consider unusable resources
    # - memoized dfs


def main():
    aoc.solve_day(19, solve_puzzle)


if __name__ == "__main__":
    main()
