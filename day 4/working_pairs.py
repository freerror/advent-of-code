def parse_to_range(range_str: str):
    start, end = [int(n) for n in range_str.split("-")]
    return range(start, end + 1)


def partially_overlaps(start: range, end: range) -> bool:
    for n in start:
        if n in end:
            return True
    return False


def fully_overlaps(start: range, end: range) -> bool:
    start_in_end = None
    end_in_start = None
    for n in start:
        if n in end:
            start_in_end = True
        else:
            start_in_end = False
            break
    for n in end:
        if n in start:
            end_in_start = True
        else:
            end_in_start = False
            break
    return start_in_end or end_in_start or False


with open("day 4/input") as f:
    range_pairs = [
        [parse_to_range(s) for s in r.split(",")] for r in f.read().split("\n") if r
    ]

full_overlaps = 0
partial_overlaps = 0

for a, b in range_pairs:
    if fully_overlaps(a, b):
        full_overlaps += 1
    if partially_overlaps(a, b):
        partial_overlaps += 1
# part 1
print(full_overlaps)
# part 2
print(partial_overlaps)
