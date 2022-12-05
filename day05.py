import os
import time
import re


def read_crates(crates_str):
    crates = [[] for i in range(9)]
    for line in crates_str.splitlines()[:-1]:
        if line == "":
            break
        for i, c in enumerate(line[1::4]):
            if c != " ":
                crates[i].append(c)

    return crates


def solve():
    input_file_contents = open(os.path.join("input", "day05")).read().rstrip()

    crates_str, instructions = input_file_contents.split("\n\n")

    crates = read_crates(crates_str)
    instruction_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for instruction in instructions.splitlines():
        match = instruction_re.match(instruction)
        ammount = int(match.group(1))
        from_ = int(match.group(2)) - 1
        to = int(match.group(3)) - 1

        for i in range(ammount):
            crates[to].insert(0, crates[from_].pop(0))

    sol_part1 = ''.join(c[0] for c in crates)
    print("Part 1:", sol_part1)

    crates = read_crates(crates_str)
    for instruction in instructions.splitlines():
        match = instruction_re.match(instruction)
        ammount = int(match.group(1))
        from_ = int(match.group(2)) - 1
        to = int(match.group(3)) - 1

        crates[to] = crates[from_][:ammount] + crates[to]
        crates[from_] = crates[from_][ammount:]

    sol_part2 = ''.join(c[0] for c in crates)
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
