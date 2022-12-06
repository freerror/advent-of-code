from collections import Counter

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_compartments(items: str):
    half = len(items) // 2
    return items[:half], items[half:]


def get_chr_priority(char: str):
    pri = 0
    for n in range(52):
        if letters[n] == char:
            pri = n + 1  # priority is 1-52 not 0-51
            break
    return pri


with open("day 3/input") as f:
    rucksacks = f.read().split("\n")
# rucksacks = ["abcdeb", "abcdefgh"]

# part 1 - sum of all item types' priorities in both compartments of each rucksack
items_in_both: list[int] = []
for rucksack in rucksacks:
    a, b = get_compartments(rucksack)
    items_in_both.extend([get_chr_priority(c) for c in set(a) if c in set(b)])
print(sum(items_in_both))

# part 2 - priority of the item type common to all 3 of 3 line groups, summed for all 3 line groups
badge_priorities_found: list[int] = []
groups = [rucksacks[r : r + 3] for r in range(0, len(rucksacks) - 1, 3)]
for item_types in groups:
    set_1 = set(item_types[0])
    set_2 = set(item_types[1])
    set_3 = set(item_types[2])
    for item in set_1:
        if item in set_2 and item in set_3:
            badge_priorities_found.append(get_chr_priority(item))
print(sum(badge_priorities_found))
