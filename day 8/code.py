import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import aoc

# Good luck and have fun: https://adventofcode.com/2022

input = aoc.get_inputs(day=8)[0]  # 0 example, 1 puzzle input
trees = [[c for c in l] for l in input.splitlines()]

max_x = len(trees[0]) - 1
max_y = len(trees) - 1


def get_height(coord: tuple[int, int]):
    # y (height) is the main list x is the inner list
    val = trees[coord[1]][coord[0]]
    return int(val)


def get_up_vis(coord: tuple[int, int], height: int):
    new_y = coord[1] - 1
    if new_y < 0:
        return True
    n = (coord[0], new_y)
    if get_height(n) < height:
        if get_up_vis(n, height):
            return True
    else:
        return False


def get_right_vis(coord: tuple[int, int], height: int):
    new_x = coord[0] + 1
    if new_x > max_x:
        return True
    n = (new_x, coord[1])
    if get_height(n) < height:
        if get_right_vis(n, height):
            return True
    else:
        return False


def get_down_vis(coord: tuple[int, int], height: int):
    new_y = coord[1] + 1
    if new_y > max_y:
        return True
    n = (coord[0], new_y)
    if get_height(n) < height:
        if get_down_vis(n, height):
            return True
    else:
        return False


def get_left_vis(coord: tuple[int, int], height: int):
    new_x = coord[0] - 1
    if new_x < 0:
        return True
    n = (new_x, coord[1])
    if get_height(n) < height:
        if get_left_vis(n, height):
            return True
    else:
        return False


def visible(coord: tuple[int, int]):
    for fn in (
        get_up_vis,
        get_down_vis,
        get_right_vis,
        get_left_vis,
    ):
        if fn(coord, get_height(coord)):
            return True


def get_up_dist(coord: tuple[int, int], height: int):
    new_y = coord[1] - 1
    if new_y < 0:
        return 0
    n = (coord[0], new_y)
    dist = 1
    if get_height(n) < height:
        dist += get_up_dist(n, height)
    return dist


def get_right_dist(coord: tuple[int, int], height: int):
    new_x = coord[0] + 1
    if new_x > max_x:
        return 0
    dist = 1
    n = (new_x, coord[1])
    if get_height(n) < height:
        dist += get_right_dist(n, height)
    return dist


def get_down_dist(coord: tuple[int, int], height: int):
    new_y = coord[1] + 1
    if new_y > max_y:
        return 0
    dist = 1
    n = (coord[0], new_y)
    if get_height(n) < height:
        dist += get_down_dist(n, height)
    return dist


def get_left_dist(coord: tuple[int, int], height: int):
    new_x = coord[0] - 1
    if new_x < 0:
        return 0
    n = (new_x, coord[1])
    dist = 1
    if get_height(n) < height:
        dist += get_left_dist(n, height)
    return dist


def get_score(coord: tuple[int, int]):
    h = get_height(coord)
    return (
        get_up_dist(coord, h)
        * get_right_dist(coord, h)
        * get_down_dist(coord, h)
        * get_left_dist(coord, h)
    )


# idea: for each item mark it is visible in a data struct list of tuples?
# tuple[int, bool] ??
# progress through every item, maybe we can use it's neighbors values
visible_trees = []
tree_scores = []
for y, row in enumerate(trees):
    for x, tree in enumerate(row):
        tree_coord = (x, y)

        if visible(tree_coord):
            visible_trees.append(tree_coord)

        tree_scores.append(get_score(tree_coord))


# part 1
print(len(visible_trees))

# part 2
print(max(tree_scores))
