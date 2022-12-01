import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day01")).read().rstrip()

    elves = []
    for elve in input_file_contents.split("\n\n"):
        elves.append([int(c) for c in elve.split()])

    total_cal = [sum(c) for c in elves]
    sol_part1 = max(total_cal)
    print("Part 1:", sol_part1)

    sol_part2 = sum(sorted(total_cal)[-3:])
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
