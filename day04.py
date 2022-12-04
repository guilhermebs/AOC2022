import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day04")).read().rstrip()

    fully_contained = 0
    overlap = 0
    for line in input_file_contents.splitlines():
        elves = line.split(",")
        elves = [[int(i) for i in elve.split("-")] for elve in elves]
        if elves[0][0] <= elves[1][0] and elves[0][1] >= elves[1][1]:
            fully_contained += 1
        elif elves[1][0] <= elves[0][0] and elves[1][1] >= elves[0][1]:
            fully_contained += 1

        if elves[0][1] < elves[1][0] or elves[1][1] < elves[0][0]:
            pass
        else:
            overlap += 1

    sol_part1 = fully_contained
    print("Part 1:", sol_part1)

    sol_part2 = overlap
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
