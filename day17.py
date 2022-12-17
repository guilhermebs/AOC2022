import os
import time
from itertools import cycle, chain

ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

CAVE_WIDTH = 7


def solve():
    input_file_contents = open(os.path.join("input", "day17")).read().rstrip()

    wind_directions = input_file_contents
    rocks = [
        tuple(chain.from_iterable(
            [[(len(r.splitlines()) - i - 1, j) for j, c in enumerate(line) if c == "#"] for i, line in enumerate(r.splitlines())]
        ))
        for r in ROCKS.split("\n\n")
    ]

    total_height, _ = simulate(rocks, wind_directions, 2022)
    sol_part1 = total_height
    print("Part 1:", sol_part1)

    total_height, _ = simulate(rocks, wind_directions, 1000000000000)
    sol_part2 = total_height
    print("Part 2:", sol_part2)


def simulate(rocks, wind_directions, n_rocks):
    rocks_iter = cycle(rocks)
    wind_iter = cycle(wind_directions)
    wind_i = -1
    total_height = 0
    cave = set()
    falls = []
    for r in range(n_rocks):
        rock = next(rocks_iter)
        start_coords = tuple((total_height + 3 + ri, 2 + rj) for ri, rj in rock)
        rock_coords = start_coords
        while True:
            wind = next(wind_iter)
            wind_i = (wind_i + 1) % len(wind_directions)
            if wind == ">":
                moved = tuple((rc[0], rc[1] + 1) for rc in rock_coords)
            elif wind == "<":
                moved = tuple((rc[0], rc[1] - 1) for rc in rock_coords)
            else:
                raise ValueError("Unexpected wind!")
            if not collides(cave, moved):
                rock_coords = moved
            moved = tuple((rc[0] - 1, rc[1]) for rc in rock_coords)
            if collides(cave, moved):
                break
            else:
                rock_coords = moved
                falls.append((None, wind_i, r % len(rocks), None))

        cave |= set(rock_coords)
        
        new_total_height = max(total_height, max(r[0] for r in rock_coords) + 1)
        falls.append((
            tuple((fc - sc) for fc, sc in zip(rock_coords[0], start_coords[0])),
            wind_i, r % len(rocks), new_total_height - total_height
        ))
        # If the total height changes, we can have a false positive
        if total_height != new_total_height:
            total_height = new_total_height
            continue
        for p in range(len(wind_directions), len(falls) - len(wind_directions), len(wind_directions)):
            for f1, f2 in zip(falls[::-1][:p], falls[::-1][p:]):
                if f1 != f2:
                    break
            else:
                height_delta = [f[3] for f in falls[-p::] if f[3] is not None]
                rocks_in_cyle = len(height_delta)
                print("Cycle detected with period:", rocks_in_cyle, "in iteration", r)
                remaining = n_rocks - r - 1
                total_height += (remaining // rocks_in_cyle) * sum(height_delta)
                total_height += sum(height_delta[:remaining % rocks_in_cyle])
                return total_height, cave

    return total_height, cave


def collides(cave, rock):
    if any(r[1] < 0 for r in rock) or any(r[1] >= CAVE_WIDTH for r in rock):
        return True

    if any(r[0] < 0 for r in rock):
        return True

    if any(r in cave for r in rock):
        return True

    return False


def print_cave(cave, total_height):
    cave_print = [["." for _ in range(CAVE_WIDTH)] for _ in range(total_height)]
    for r in cave:
        cave_print[r[0]][r[1]] = "#"
    print("\n".join(''.join(row) for row in cave_print[::-1]))


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
