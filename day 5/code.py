import re


def parse_stacks(stack_rows: list[list[str]]):
    stacks: list[list[str]] = []

    max_stacks = len(stack_rows[0])
    i = 0
    while i < max_stacks:
        stack: list[str] = []
        for row in stack_rows:
            if row[i]:
                stack.append(row[i])
        stack.reverse()
        stacks.append(stack)
        i += 1

    return stacks


def main():
    op_pattern = re.compile(r"(?:e )(\d*)(?: from )(\d*)(?: to )(\d*)")
    with open("day 5/input") as f:
        data = f.read().split("\n\n")
    stack_rows = [re.split(r"    |\B \B", r) for r in data[0].split("\n")][:-1]
    stacks: list[list[str]] = parse_stacks(stack_rows)
    operations = [
        [int(r) for r in op_pattern.search(s).groups()]  # type: ignore
        for s in data[1].splitlines()
    ]

    # # Part 1 - crane only moves one crate at a time
    # for op in operations:
    #     amount = op[0]
    #     src: list[str] = stacks[op[1] - 1]
    #     dest: list[str] = stacks[op[2] - 1]

    #     for _ in range(amount):
    #         crate = src.pop()
    #         dest.append(crate)

    # Part 2 - crane moves multiple crates at a time
    for op in operations:
        amount = op[0]
        src: list[str] = stacks[op[1] - 1]
        dest: list[str] = stacks[op[2] - 1]

        crate = src[-amount:]
        del src[-amount:]
        dest.extend(crate)

    top_row = [re.sub(r"\[|\]", "", r[-1]) for r in stacks]
    print("".join(top_row))


if __name__ == "__main__":
    main()
