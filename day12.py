import os
from collections import deque
import time


def find_pos(heights, pos):
    i = [i for i, row in enumerate(heights) if pos in row][0]
    j = heights[i].index(pos)
    return i, j


def solve():
    input_file_contents = open(os.path.join("input", "day12")).read().rstrip()
    heights = [[c for c in row] for row in input_file_contents.splitlines()]
    start_row, start_col = find_pos(heights, "S")
    objective = find_pos(heights, "E")
    print(start_row, start_col, objective)

    heights = [[ord(c) - ord("a") for c in row] for row in input_file_contents.splitlines()]
    heights[start_row][start_col] = 0
    heights[objective[0]][objective[1]] = 0
    n_rows = len(heights)
    n_cols = len(heights[0])
    print(heights)

    # BFS!
    costs = deque([0])
    queue = deque([(start_row, start_col)])
    while len(queue) > 0:
        i, j = queue.popleft()
        n = costs.popleft()
        if (i, j) == objective:
            sol_part1 = n
            break
        for ii in range(max(i-1, 0), min(i+2, n_rows)):
            for jj in range(max(j-1, 0), min(j+2, n_cols)):
                if heights[ii][jj] - heights[ii][jj] >= 1:
                    pass
                if (ii, jj) == (i, j) or ((ii, jj) in queue):
                    pass
                queue.append((ii, jj))
                costs.append(n+1)

    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
