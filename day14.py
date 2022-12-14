import os
import time
import copy
from itertools import chain


def solve():
    input_file_contents = open(os.path.join("input", "day14")).read().rstrip()

    scans = []
    for line in input_file_contents.splitlines():
        scans.append([tuple(int(i) for i in s.split(",")) for s in line.split(" -> ")])

    xmin = min(s[0] for s in chain.from_iterable(scans))
    xmax = max(s[0] for s in chain.from_iterable(scans))
    ymin = 0
    ymax = max(s[1] for s in chain.from_iterable(scans))

    cave_map = [[0 for i in range(xmin, xmax+1)] for j in range(ymin, ymax+1)]
    sizey, sizex = len(cave_map), len(cave_map[0])

    for scan in scans:
        for (xs, ys), (xe, ye) in zip(scan, scan[1:]):
            if (xs, ys) > (xe, ye):
                (xs, ys), (xe, ye) = (xe, ye), (xs, ys)
            if xs == xe:
                for y in range(ys, ye + 1):
                    cave_map[y][xs - xmin] = 1
            elif ys == ye:
                for x in range(xs - xmin, xe - xmin + 1):
                    cave_map[ys][x] = 1
            else:
                raise ValueError("Invalid scan!")

    sand_cave = copy.deepcopy(cave_map)
    while add_sand(sand_cave, (500 - xmin, 0)):
        pass

    sol_part1 = sum(t == 2 for t in chain.from_iterable(sand_cave))
    print("Part 1:", sol_part1)

    sand_cave2 = []
    # Add sides
    pad_len = 2 * ((sizey + 2 - sizex//2) + 1)
    pad = [0 for i in range(pad_len)]
    for row in cave_map:
        sand_cave2.append(pad + row + pad)
    # Add floor
    sand_cave2.append([0 for i in sand_cave2[0]])
    sand_cave2.append([1 for i in sand_cave2[0]])

    sand_cave2[0][500 - (xmin - pad_len)] = 2
    while add_sand(sand_cave2, (500 - (xmin - pad_len), 0)):
        pass

    sol_part2 = sum(t == 2 for t in chain.from_iterable(sand_cave2))
    print("Part 2:", sol_part2)


def cave_string(cave_map):
    chars = [".", "#", "o"]
    return "\n".join([''.join([chars[t] for t in row]) for row in cave_map])


def add_sand(cave_map, start_pos):
    x, y = start_pos
    while True:
        if y == len(cave_map) or x == 0 or x == len(cave_map[0]):
            return False

        for xd, yd in [(x, y+1), (x-1, y+1), (x+1, y+1)]:
            if cave_map[yd][xd] == 0:
                x, y = xd, yd
                break
        else:
            cave_map[y][x] = 2
            return (x, y) != start_pos


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
