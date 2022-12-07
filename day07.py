import os
import time


def dir_size(contents, dir_name, calculated_sizes):
    size = 0
    for c in contents[dir_name]:
        if c.startswith("dir"):
            size += dir_size(
                contents, dir_name + "/" + c.split()[-1], calculated_sizes
            )
        else:
            size += int(c.split()[0])
    calculated_sizes[dir_name] = size
    return size


def solve():
    input_file_contents = open(os.path.join("input", "day07")).read().rstrip()

    contents = dict()
    visit_sequence = []
    for line in input_file_contents.splitlines():
        if line.startswith("$ cd"):
            cd = line.split()[-1]
            if cd == "..":
                visit_sequence = visit_sequence[:-1]
            else:
                visit_sequence.append(cd)
            current_dir = "/".join(visit_sequence)
        elif line == "$ ls":
            contents[current_dir] = []
        else:
            contents[current_dir].append(line)

    calculated_sizes = {}
    total_size = dir_size(contents, "/", calculated_sizes)
    max_size = 100000

    sol_part1 = sum(size for size in calculated_sizes.values() if size <= max_size)
    print("Part 1:", sol_part1)

    avaliable = 70000000
    required = 30000000
    to_free = required - (avaliable - total_size)

    sol_part2 = min(size for size in calculated_sizes.values() if size > to_free)
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
