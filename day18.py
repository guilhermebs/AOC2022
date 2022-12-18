import os
import time
from collections import deque


def solve():
    input_file_contents = open(os.path.join("input", "day18")).read().rstrip()

    all_cubes = set(tuple(int(c) for c in line.split(",")) for line in input_file_contents.splitlines())
    n_exposed_faces, empty_cubes = exposed_faces(all_cubes)

    sol_part1 = n_exposed_faces
    print("Part 1:", sol_part1)

    bounding_box = tuple([
        tuple(min(c[i] for c in all_cubes) for i in range(3)),
        tuple(max(c[i] for c in all_cubes) for i in range(3))
    ])

    # starting at an empty cube, do BFS search. If we ever go outside the
    # bounding box, it is connected. Otherwise stop
    known_outside = set()
    known_inside = set()
    for i, empty_c in enumerate(empty_cubes):
        is_out, searched = connected_to_outside(
            empty_c, all_cubes, bounding_box, known_outside, known_inside
        )
        if is_out:
            known_outside |= searched
        else:
            known_inside |= searched

    sol_part2, _ = exposed_faces(all_cubes | known_inside)
    print("Part 2:", sol_part2)

def exposed_faces(all_cubes):
    n_exposed_faces = 0
    empty_cubes = []
    for cube in all_cubes:
        for i in range(3):
            for sign in [+1, -1]:
                coords = list(cube)
                coords[i] += sign
                coords = tuple(coords)
                if coords not in all_cubes:
                    n_exposed_faces += 1
                    empty_cubes.append(coords)

    return n_exposed_faces, empty_cubes


def connected_to_outside(empty_space, all_cubes, bounding_box, known_outside, known_inside):
    seen = set([empty_space])
    queue = deque([empty_space])
    while len(queue) > 0:
        coords = queue.popleft()
        if coords in known_inside:
            return False, seen
        if coords in known_outside:
            return True, seen
        if any(c < bbmin or c > bbmax for c, bbmin, bbmax in zip(coords, bounding_box[0], bounding_box[1])):
            return True, seen
        else:
            for i in range(3):
                for sign in (-1, 1):
                    neighbour = list(coords)
                    neighbour[i] += sign
                    neighbour = tuple(neighbour)
                    if neighbour not in all_cubes and neighbour not in seen:
                        queue.append(neighbour)
                        seen |= set([neighbour])

    return False, seen


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
