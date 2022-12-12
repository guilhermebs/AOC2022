import os
import heapq
from collections import defaultdict
import time


def solve():
    input_file_contents = open(os.path.join("input", "day12")).read().rstrip()
    input_file_contents = open(os.path.join("input", "day12_test")).read().rstrip()
    heights = [[c for c in row] for row in input_file_contents.splitlines()]
    start_row, start_col = find_pos(heights, "S")
    objective = find_pos(heights, "E")

    heights = [[ord(c) - ord("a") for c in row] for row in input_file_contents.splitlines()]
    heights[start_row][start_col] = 0
    heights[objective[0]][objective[1]] = ord("z") - ord("a")
    n_rows = len(heights)
    n_cols = len(heights[0])
    print(n_rows, n_cols)

    # A*!
    h = []
    start = (start_row, start_col)
    n_steps = defaultdict(lambda : 1e6)
    heapq.heappush(
            h, 
            (manhattan(start, objective), start)
    )
    n_steps[start] = 0
    while len(h) > 0:
        _, (i, j) = heapq.heappop(h)
        n = n_steps[(i, j)]
        if (i, j) == objective:
            sol_part1 = n
            break
        for (ii, jj) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if ii < 0 or ii >= n_rows or jj < 0 or jj >= n_cols:
                continue
            elif heights[ii][jj] - heights[i][j] > 1:
                continue
            elif n_steps[(ii, jj)] > n + 1:
                heapq.heappush(
                    h,
                    (manhattan((ii, jj), objective) + n + 1, (ii, jj))
                )
                n_steps[(ii, jj)] = n + 1

    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def find_pos(heights, pos):
    i = [i for i, row in enumerate(heights) if pos in row][0]
    j = heights[i].index(pos)
    return i, j


def manhattan(p1, p2):
    return sum(abs(p - q) for p, q in zip(p1, p2))



#def search(start, is_end, can_walk):



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
