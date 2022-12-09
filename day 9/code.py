import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils import try_int, Vec, lrg
import aoc

# Good luck and have fun: https://adventofcode.com/2022

input = aoc.get_inputs(day=9)[1]  # 0 example, 1 puzzle input
moves = [[try_int(v) for v in m.split(" ")] for m in input.splitlines()]

num_of_knots = 10
rope = [Vec(0, 0) for _ in range(num_of_knots)]
head = rope[0]
tail = rope[-1]
tail_positions = set([(tail.x, tail.y)])

for direction, amount in moves:
    for _ in range(amount):
        if direction == "U":
            head.y += 1
        elif direction == "R":
            head.x += 1
        elif direction == "D":
            head.y -= 1
        elif direction == "L":
            head.x -= 1
        for i in lrg(1, rope):
            # Used below from someone elses working Part 2 solution to troubleshoot why mine
            # wasn't.  During development of my solution, I believed the "key"
            # was simply moving the tail to the head's previous location but
            # only after it was greater than 1 away, this worked for Part 1. In
            # part 2 I realized it was just a max move of 1 toward the head,
            # but I kept a copy of the whole rope form it's previous state
            # around, thinking I still needed it, and the bug in my version was
            # referring to this copy.
            # For the below, thanks to https://www.reddit.com/user/threeys/ :
            # ```
            # x_dist = rope[i - 1].x - rope[i].x
            # y_dist = rope[i - 1].y - rope[i].y
            # if abs(x_dist) > 1 or abs(y_dist) > 1:
            #     rope[i].x += min(max(x_dist, -1), 1)
            #     rope[i].y += min(max(y_dist, -1), 1)
            # ```

            cur = rope[i]
            next = rope[i - 1]
            if abs(next.x - cur.x) > 1 or abs(next.y - cur.y) > 1:
                if next.x > cur.x:
                    cur.x += 1
                elif next.x < cur.x:
                    cur.x -= 1
                if next.y > cur.y:
                    cur.y += 1
                elif next.y < cur.y:
                    cur.y -= 1
        tail_positions.add((tail.x, tail.y))
print(len(tail_positions))
