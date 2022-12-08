import os
import time
import numpy as np


def solve():
    input_file_contents = open(os.path.join("input", "day08")).read().rstrip()

    trees = []
    for line in input_file_contents.splitlines():
        trees.append([int(i) for i in line])

    trees = np.array(trees)

    visible = []
    for i, row in enumerate(trees):
        for j, t in enumerate(row):
            if (all(t > row[:j]) or all(t > row[j+1:]) or
                    all(t > trees[:i, j]) or all(t > trees[i+1:, j])):
                visible.append((i, j))

    sol_part1 = len(set(visible))
    print("Part 1:", sol_part1)

    cones = []
    for x, y in visible:
        cone = 1
        for inc in (1, -1):
            i = inc
            while 0 <= i+x < trees.shape[0] and trees[i+x, y] < trees[x, y]:
                i += inc
            j = inc
            while 0 <= j+y < trees.shape[1] and trees[x, j+y] < trees[x, y]:
                j += inc
            cone *= (abs(i)-(i+x < 0 or i+x >= trees.shape[1])) *\
                    (abs(j)-(j+y < 0 or j+y >= trees.shape[1]))

        cones.append(cone)

    sol_part2 = max(cones)
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
