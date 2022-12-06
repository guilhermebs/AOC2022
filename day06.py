import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day06")).read().rstrip()

    for i in range(4, len(input_file_contents)):
        if len(set(input_file_contents[i-4:i])) == 4:
            sol_part1 = i
            break

    print("Part 1:", sol_part1)

    for i in range(14, len(input_file_contents)):
        if len(set(input_file_contents[i-14:i])) == 14:
            sol_part2 = i
            break

    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
