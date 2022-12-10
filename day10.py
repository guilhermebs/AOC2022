import os
import time


def register_cycle(cycle, x_val, signal_strength):
    cycle += 1
    if (cycle + 20) % 40 == 0:
        signal_strength += x_val * cycle
    return cycle, signal_strength


def draw_crt(cycle, x_val, crt):
    row = cycle // 40
    col = cycle % 40
    if abs(col - x_val) <= 1:
        crt[row][col] = "#"


def solve():
    input_file_contents = open(os.path.join("input", "day10")).read().rstrip()
    cycle = 0
    signal_strength = 0
    x_val = 1
    for line in input_file_contents.splitlines():
        if line == "noop":
            cycle, signal_strength = register_cycle(cycle, x_val, signal_strength)
        else:
            cycle, signal_strength = register_cycle(cycle, x_val, signal_strength)
            cycle, signal_strength = register_cycle(cycle, x_val, signal_strength)
            x_val += int(line.split()[1])

    sol_part1 = signal_strength
    print("Part 1:", sol_part1)

    crt = [["." for i in range(40)] for j in range(6)]
    cycle = 0
    signal_strength = 0
    x_val = 1
    for line in input_file_contents.splitlines():
        if line == "noop":
            draw_crt(cycle, x_val, crt)
            cycle += 1
        else:
            draw_crt(cycle, x_val, crt)
            cycle += 1
            draw_crt(cycle, x_val, crt)
            cycle += 1
            x_val += int(line.split()[1])

    sol_part2 = "\n".join(''.join(row) for row in crt)
    print(f"Part 2:\n{sol_part2}")


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
