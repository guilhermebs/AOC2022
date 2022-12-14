import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day20")).read().rstrip()
    seq = [int(x) for x in input_file_contents.splitlines()]
    mixed = mix(seq)
    coords = get_grove_coords(mixed)
    sol_part1 = sum(coords)
    print("Part 1:", sol_part1)

    key = 811589153
    mixed = [x*key for x in seq]
    mixed = mix(mixed, rounds=10)
    coords = get_grove_coords(mixed)
    sol_part2 = sum(coords)
    print("Part 2:", sol_part2)


def mix(seq, rounds=1):
    tot_len = len(seq)
    indices = [idx for idx in range(tot_len)]
    for _ in range(rounds):
        for i, n in enumerate(seq):
            mix_index = indices.index(i)
            indices.pop(mix_index)  # here the length of the list decreases!
            # also, the first and last position are the same!
            move_to = (mix_index + n) % (tot_len - 1)
            indices.insert(move_to, i)

    return [seq[idx] for idx in indices]


def get_grove_coords(seq):
    return [seq[(idx + seq.index(0)) % len(seq)] for idx in (1000, 2000, 3000)]


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
