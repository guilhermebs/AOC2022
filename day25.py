import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day25")).read().rstrip()

    total = sum(snafu2decimal(n) for n in input_file_contents.splitlines())

    sol_part1 = decimal2snafu(total)
    print("Part 1:", sol_part1)


def snafu2decimal(number):
    result = 0
    for i, n in enumerate(number[::-1]):
        if n in ('2', '1', '0'):
            result += int(n) * 5**i
        elif n == '-':
            result -= 5**i
        elif n == '=':
            result -= 2 * 5**i
    return result


def decimal2snafu(number):
    base5 = []
    while number:
        base5.append(number % 5)
        number //= 5
    snafu = [0 for _ in range(len(base5) + 1)]
    for i, d in enumerate(base5):
        if d < 3:
            val = snafu[i] + d
            if val < 3:
                snafu[i] = val
            else:
                snafu[i] = val - 5
                snafu[i + 1] = 1
        elif d >= 3:
            snafu[i] += d - 5
            snafu[i + 1] = 1

    if snafu[-1] == 0:
        snafu = snafu[:-1]

    return "".join(str(d).replace("-1", "-").replace("-2", "=") for d in snafu[::-1])


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
