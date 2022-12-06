with open("day 6/input") as f:
    data = f.read()

# Part 1 - count of chars before unique 4 characters in string
# Part 2 - count of chars before unique 14 characters in string

markers: list[tuple[int, str]] = []
for i, c in enumerate(data):
    seq: list[str] = []
    seq.append(c)
    try:
        seq.extend([data[i + n] for n in range(1, 14)])
    except IndexError as _:
        # end of stream
        break

    if len(set(seq)) == 14:
        markers.append((i, "".join(seq)))

processed_chars = len(data[: markers[0][0]]) + 14
print(processed_chars)
