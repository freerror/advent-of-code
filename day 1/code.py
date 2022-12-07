with open("day 1/input") as f:
    data = [[int(n) for n in d.split("\n") if n] for d in f.read().split("\n\n")]
sums = [sum(nums) for nums in data]
# Part 1 - Highest total carried by top elf
print(sorted(sums)[-1])
# Part 2 - Highest total carried by top 3 elves
print(sum(sorted(sums)[-3:]))
