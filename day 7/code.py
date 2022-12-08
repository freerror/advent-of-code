from dataclasses import dataclass, field
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc

# Good luck and have fun: https://adventofcode.com/2022

lines = aoc.get_inputs(day=7)[0].splitlines()

# Part 1 - total size of directories who's size is <= 100_000
# Part 2 -


@dataclass
class Dir:
    name: str
    size: int
    parent: "Dir"
    children: list["Dir"] = field(default_factory=list)

    def __repr__(self):
        return f"{self.parent if self.parent else ''}{'/' if self.parent else ''}{self.name}"


def get_total_dir_size(base: Dir):
    total_size = 0
    for child in base.children:
        total_size += get_total_dir_size(child)
    total_size += base.size
    return total_size


def try_as_int(string: str):
    try:
        return int(string)
    except:
        return string


cwd = Dir("", 0, None)  # type: ignore
base = None
seen_dirs = []

for line in lines:
    tokens: list[str] = line.split(" ")
    if tokens[0] == "$":
        # command
        if tokens[1] == "cd":
            # up dir
            if tokens[2] == "..":
                cwd = cwd.parent
                continue
            # into dir
            new_dir = Dir(tokens[2], 0, cwd)
            seen_dirs.append(new_dir)
            if base == None:
                base = new_dir
            if new_dir.name not in [c.name for c in cwd.children]:
                cwd.children.append(new_dir)
            prev_dir = cwd
            cwd = new_dir
            cwd.parent = prev_dir
    elif isinstance(size := try_as_int(tokens[0]), int):
        # dir contents
        cwd.size += size


totals = []

to_reduce = 0
for dir in seen_dirs:
    size = get_total_dir_size(dir)
    # # part 1
    # if size <= 100_000:
    #     totals.append(size)

    # part 2
    totals.append(size)
    if dir.name == "/":
        to_reduce = 30_000_000 - (70_000_000 - size)
    totals.append(size)
part_1_total = sum(totals)
part_2_candidates = sorted([d for d in totals if d >= to_reduce])
print(sorted(part_2_candidates))
