import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day03")).read().rstrip()
    rucksacks = input_file_contents.split()
    repeated = []
    for rucksack in rucksacks:
        repeated.extend(
            set(rucksack[:len(rucksack)//2]).intersection(set(rucksack[len(rucksack)//2:]))
        )

    sol_part1 = sum(ord(l) - ord('a') + 1 for l in repeated if l.islower())
    sol_part1 += sum(ord(l) - ord('A') + 27 for l in repeated if l.isupper())
    print("Part 1:", sol_part1)

    badge_items = []
    for i in range(0, len(rucksacks), 3):
        badge_items.extend(
            set(rucksacks[i]).intersection(rucksacks[i+1], rucksacks[i+2])
        )
    sol_part2 = sum(ord(l) - ord('a') + 1 for l in badge_items if l.islower())
    sol_part2 += sum(ord(l) - ord('A') + 27 for l in badge_items if l.isupper())
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
