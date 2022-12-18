"""Note: Does not work for part 2"""


from itertools import count
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def get_shapes():
    # tuple coords of each rock shape
    sheet = (
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
    )
    plus = (
        (1, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (1, 2),
    )
    bend = (
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
    )
    beam = (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
    )
    box = (
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
    )
    return (sheet, plus, bend, beam, box)


def coords_from_origin(shape, origin):
    coords = []
    for c in shape:
        coords.append((c[0] + origin[0], c[1] + origin[1]))
    return set(coords)


def collision(origin, shape, crown):
    shape_coords = coords_from_origin(shape, origin)
    for c in shape_coords:
        if not (-1 < c[0] < 7):
            return True
        if c in crown:
            return True
    return False


def clean_up_crown(crown, current_max, limit=80):
    """Remove any coords below a certain point"""
    y = current_max - limit
    new_crown = set()
    for c in crown:
        if c[1] > y:
            new_crown.add(c)
    return new_crown


def test_clean():
    old_crown = {
        (0, -1),
        (1, -1),
        (2, -1),
        (3, -1),
        (4, -1),
        (5, -1),
        (6, -1),
        (0, 5000),
        (1, 5000),
    }
    current_max = max([c[1] for c in old_crown])
    new_crown = clean_up_crown(old_crown, current_max)
    assert new_crown == {(0, 5000), (1, 5000)}


def update_crown(crown, origin, shape):
    s = coords_from_origin(shape, origin)
    new_crown = crown | s
    return new_crown


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    dis_lookup = {"<": -1, ">": 1}
    dis = [dis_lookup[d] for d in input.splitlines()[0]]
    shapes = get_shapes()

    crown = {
        (0, -1),
        (1, -1),
        (2, -1),
        (3, -1),
        (4, -1),
        (5, -1),
        (6, -1),
    }
    x_rests = []
    # drops = range(1_000_000_000_000)
    # drops = range(500_000)
    drops = range(12_000)
    # drops = range(2022)
    j = -1
    current_max = -1
    last_full_row = 0
    last_repeat = 0
    end_totals = 0
    end_start = 0
    end_end = 0
    for i in drops:
        # sys.stdout.write(f"\r{i}")
        # sys.stdout.flush()
        shape = shapes[i % len(shapes)]
        origin = (2, current_max + 4)
        while True:
            j += 1
            d = dis[j % len(dis)]
            # attempt to displace
            if not collision(
                try_origin := (origin[0] + d, origin[1]), shape, crown
            ):
                origin = try_origin
            if not collision(
                try_origin := (origin[0], origin[1] - 1), shape, crown
            ):
                origin = try_origin
            else:
                x_rests.append(origin[0])
                crown = update_crown(crown, origin, shape)
                current_max = m = max([c[1] for c in crown])

                # Hack to find the the repeating period. Just watched for the
                # row to repeat
                if all((c, m) in crown for c in range(7)):
                    if ind := i - last_full_row == 800:
                        print(
                            "i since last repeat:",
                            (i - last_full_row),
                            "| i:",
                            i,
                            "| i change:",
                            i - last_repeat,
                            "| max height:",
                            m,
                        )
                        last_repeat = i
                        end_start = m

                    last_full_row = i
                crown = clean_up_crown(crown, current_max)
                break
        if end_start:
            end_end = m
            end_totals += 1
            if end_totals == 2800:  # manually found remaining drops
                break

    print()
    # return max(set([c[1] for c in crown])) + 1, 0
    return end_end - end_start, 0


def main():
    aoc.solve_day(17, solve_puzzle)


if __name__ == "__main__":
    main()
