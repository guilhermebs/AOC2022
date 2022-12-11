import os
import time
import copy
import re


def solve():
    input_file_contents = open(os.path.join("input", "day11")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "day11_example")).read().rstrip()

    monkeys = []
    items = []
    for description in input_file_contents.split("\n\n"):
        m, wlevels = read_monkey_description(description)
        monkeys.append(m)
        items.append(wlevels)

    sol_part1 = calc_monkey_business(monkeys, items, 20)
    print("Part 1:", sol_part1)

    sol_part2 = calc_monkey_business(monkeys, items, 20, is_part1=False)
    print("Part 2:", sol_part2)


def calc_monkey_business(monkeys, init_items, rounds, is_part1=True):
    items = copy.deepcopy(init_items)
    inspect_counts = [0 for m in monkeys]
    for r in range(rounds):
        for i, m, wlevels in zip(range(len(monkeys)), monkeys, items):
            for w in wlevels:
                inspect_counts[i] = inspect_counts[i] + 1
                w, t = m.process_item(w, is_part1=is_part1)
                items[t].append(w)
            wlevels.clear()

    inspect_counts = sorted(inspect_counts, reverse=True)
    return inspect_counts[0] * inspect_counts[1]


_operation_re = re.compile(r"new = old ([+\*]) (.*)")


def read_monkey_description(description):
    lines = description.splitlines()
    items = [int(n.strip(",")) for n in lines[1].split()[2:]]
    operation_match = _operation_re.search(lines[2])

    if operation_match.group(2) == "old":
        if operation_match.group(1) == "+":
            operation = lambda x: x + x
        elif operation_match.group(1) == "*":
            operation = lambda x: x * x;
        else:
            raise ValueError("Invalid operation!")
    else:
        const = int(operation_match.group(2))
        if operation_match.group(1) == "+":
            operation = lambda x: x + const
        elif operation_match.group(1) == "*":
            operation = lambda x: x * const
        else:
            raise ValueError("Invalid operation!")

    divisible_by = int(lines[3].split()[-1])

    target_monkey_true = int(lines[4].split()[-1])
    target_monkey_false = int(lines[5].split()[-1])

    return (
        Monkey(operation, divisible_by, target_monkey_true, target_monkey_false),
        items
    )


class Monkey:
    def __init__(self, operation, divisible_by, target_monkey_true, target_monkey_false):
        self.operation = operation
        self.divisible_by = divisible_by
        self.target_monkey_true = target_monkey_true
        self.target_monkey_false = target_monkey_false

    def process_item(self, wlevel, is_part1=True):
        wlevel = self.operation(wlevel)
        if is_part1:
            wlevel = wlevel // 3
        if (wlevel % self.divisible_by) == 0:
            target = self.target_monkey_true
        else:
            target = self.target_monkey_false

        return (wlevel, target)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
