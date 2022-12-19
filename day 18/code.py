from dataclasses import dataclass, field
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


@dataclass
class Voxel:
    x: int
    y: int
    z: int
    neighbors: list["Voxel"] = field(default_factory=list)
    adjacencies: list["Voxel"] = field(default_factory=list)
    air_blocks: list["Voxel"] = field(default_factory=list)

    @property
    def exposed_faces(self):
        return len(self.air_blocks)

    def parse_neighbors(self, others: list["Voxel"]):
        for v in self.adjacencies:
            if v in others:
                self.neighbors.append(v)
            else:
                self.air_blocks.append(v)

    def parse_adjacencies(self):
        pos_x = Voxel(self.x + 1, self.y, self.z)
        pos_y = Voxel(self.x, self.y + 1, self.z)
        pos_z = Voxel(self.x, self.y, self.z + 1)
        neg_x = Voxel(self.x - 1, self.y, self.z)
        neg_y = Voxel(self.x, self.y - 1, self.z)
        neg_z = Voxel(self.x, self.y, self.z - 1)
        self.adjacencies = [pos_x, pos_y, pos_z, neg_x, neg_y, neg_z]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    voxels = [
        Voxel(int(v[0]), int(v[1]), int(v[2]))
        for v in [i.split(",") for i in input.splitlines()]
    ]

    surface_area = 0
    for v in voxels:
        v.parse_adjacencies()
        v.parse_neighbors(voxels)
        surface_area += v.exposed_faces

    return surface_area, 0


def main():
    aoc.solve_day(18, solve_puzzle)


if __name__ == "__main__":
    main()
