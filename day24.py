import itertools
import os
import time

NORTH = "^"
SOUTH = "v"
EAST = ">"
WEST = "<"

DIRECTIONS = (NORTH, SOUTH, EAST, WEST)

MOVE_DIRS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0)
}


def solve():
    input_file_contents = open(os.path.join("input", "day24")).read().rstrip()

    region_size = (
        len(input_file_contents.splitlines()[0]) - 2,
        len(input_file_contents.splitlines()) - 2
    )
    blizzard = [b for b in itertools.chain.from_iterable(
        [(i - 1, j - 1, c) for i, c in enumerate(line) if c in DIRECTIONS]
        for j, line in enumerate(input_file_contents.splitlines())
    )]
    start = (0, -1)
    end = (region_size[0] - 1, region_size[1])

    sol_part1 = find_path(region_size, blizzard, start, end)
    print("Part 1:", sol_part1)

    for _ in range(sol_part1):
        blizzard = update_blizzard(region_size, blizzard)
    return_trip = find_path(region_size, blizzard, end, start)
    for _ in range(return_trip):
        blizzard = update_blizzard(region_size, blizzard)
    back_again = find_path(region_size, blizzard, start, end)
    sol_part2 = sol_part1 + return_trip + back_again
    print("Part 2:", sol_part2)


def update_blizzard(region_size, blizzard):
    def wrap(pos):
        wrap = [pos[0], pos[1], pos[2]]
        for i in range(2):
            if pos[i] >= region_size[i]:
                wrap[i] = 0
            elif pos[i] < 0:
                wrap[i] = region_size[i] - 1
        return tuple(wrap)

    return [wrap((i + MOVE_DIRS[c][0], j + MOVE_DIRS[c][1], c)) for i, j, c in blizzard]


def print_blizzard(region_size, blizzard):
    grid = [["." for i in range(region_size[0])] for j in range(region_size[1])]
    for i, j, c in blizzard:
        grid[j][i] = c
    string = "#." + "#" * region_size[0] + "\n"
    string += "\n".join(["#" + "".join(row) + "#" for row in grid])
    string += "\n" + "#" * region_size[0] + ".#"
    print(string)


def find_path(region_size, blizzard, start, end):
    states = set([start])
    n_steps = 0
    while True:
        next_blizzard = update_blizzard(region_size, blizzard)
        nb_pos = set((i, j) for i, j, _ in next_blizzard)
        new_states = set()
        for pos in states:
            if pos == end:
                return n_steps

            for di, dj in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_pos = pos[0] + di, pos[1] + dj
                if new_pos in (start, end):
                    new_states.add(new_pos)
                    continue
                if new_pos[0] >= region_size[0] or new_pos[0] < 0:
                    continue
                if new_pos[1] >= region_size[1] or new_pos[1] < 0:
                    continue
                if new_pos in nb_pos:
                    continue
                new_states.add(new_pos)

        n_steps += 1
        blizzard = next_blizzard
        states = new_states


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
