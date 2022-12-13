from itertools import zip_longest
from math import prod
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent.parent))
import utils
import aoc

# Good luck and have fun: https://adventofcode.com/2022


def merge_and_sort(left, right) -> list[int]:
    """Merges two lists, sorting in the process
    Returns a new merged list

    Run's in overall linear O(n) time
    """
    li = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if is_sorted(left[i], right[j]) == 1:
            li.append(left[i])
            i += 1
        else:
            li.append(right[j])
            j += 1

    while i < len(left):
        li.append(left[i])
        i += 1

    while j < len(right):
        li.append(right[j])
        j += 1

    return li


def merge_sort(unsorted_list: list[int]) -> list[int]:
    """Sorts a list in ascending order and return new sorted list

    Divide: Find the midpoint of list and divide into sublist
    Conquer: Recursively sort the sublists from previous step
    Combine: Merge the sorted sublists from previous

    Takes overall, O(n log n)
    """

    if len(unsorted_list) <= 1:
        return unsorted_list

    half = len(unsorted_list) // 2
    left = merge_sort(unsorted_list[:half])
    right = merge_sort(unsorted_list[half:])

    return merge_and_sort(left, right)


def is_list(x):
    return isinstance(x, list)


def get_list(x):
    if is_list(x):
        return x
    else:
        return [x]


def is_sorted(left, right) -> int:
    left = get_list(left)
    right = get_list(right)
    for a, b in zip_longest(left, right):
        if a is None:
            return 1
        elif b is None:
            return -1
        elif isinstance(a, int) and isinstance(b, int):
            if a < b:
                return 1
            elif a > b:
                return -1
            else:  # a == b
                continue
        else:
            sort = is_sorted(get_list(a), get_list(b))
            if sort == -1:
                return -1
            elif sort == 1:
                return 1
            else:  # a == b or lists ran out
                continue
    return 0


def solve_puzzle(input: str):
    """Main Puzzle Function"""
    lines = [line.replace("\n", ",") for line in input.split("\n\n")]
    pairs = []
    for line in lines:
        pairs.append(eval(line))

    in_ord = []
    i = 0
    for left, right in pairs:
        i += 1
        sort = is_sorted(left, right)
        if sort == 1:
            in_ord.append(i)

    # Part 2 merge sort
    packets = []
    decoder_packets = [[[2]], [[6]]]
    packets.extend(decoder_packets)
    for left, right in pairs:
        packets.extend([left, right])
    sorted_packets = merge_sort(packets)

    decoder_key_indices = [
        i + 1 for i, v in enumerate(sorted_packets) if v in decoder_packets
    ]

    part_1_solution = sum(in_ord)
    part_2_solution = prod(decoder_key_indices)
    return part_1_solution, part_2_solution


def main():
    aoc.solve_day(13, solve_puzzle)


if __name__ == "__main__":
    main()
