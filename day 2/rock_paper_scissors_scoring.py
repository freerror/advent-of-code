with open("day 2/input") as f:
    data = (
        f.read()
        .replace("A", "1")
        .replace("B", "2")
        .replace("C", "3")
        .replace("X", "1")
        .replace("Y", "2")
        .replace("Z", "3")
    )
    plays = [[int(n) for n in r.split(" ") if n] for r in data.split("\n") if r]

beats = {1: 2, 2: 3, 3: 1}

# Part 1 - assumes 'you' mean's what would be played by you
results: list[int] = []
for them, you in plays:
    if you == them:
        # draw
        results.append(you + 3)
    elif you == beats[them]:
        # win
        results.append(you + 6)
    else:
        # lose
        results.append(you)
print(sum(results))

# Part 2 - assumes 'you' means 1 lose, 2 draw, 3 win
beaten_by = {1: 3, 2: 1, 3: 2}
results = []
for them, you in plays:
    if you == 1:
        # lose
        results.append(beaten_by[them])
    elif you == 2:
        # draw
        results.append(them + 3)
    elif you == 3:
        # win
        results.append(beats[them] + 6)
print(sum(results))
