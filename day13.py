import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day13")).read().rstrip()

    pairs = []
    for p in input_file_contents.split("\n\n"):
        pairs.append([eval(line) for line in p.splitlines()])

    right_order = 0
    for i, (left, right) in enumerate(pairs):
        if compare(left, right):
            right_order += i + 1

    sol_part1 = right_order
    print("Part 1:", sol_part1)

    packets = [Packet(p[0]) for p in pairs] + [Packet(p[1]) for p in pairs]
    extension = [Packet([[2]]), Packet([[6]])]
    packets.extend(extension)

    packets = sorted(packets)

    sol_part2 = (packets.index(extension[0]) + 1) * (packets.index(extension[1]) + 1)
    print("Part 2:", sol_part2)


class Packet:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        self.data == other.data

    def __lt__(self, other):
        return compare(self.data, other.data)

    def __repr__(self):
        return self.data.__repr__()


def compare(left, right):
    for il, ir in zip(left, right):
        if isinstance(il, list) or isinstance(ir, list):
            if not isinstance(il, list):
                il = [il]
            if not isinstance(ir, list):
                ir = [ir]
            c = compare(il, ir)
            if c is None:
                continue
            elif c:
                return True
            else:
                return False
        if il < ir:
            return True
        elif il > ir:
            return False

    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False

    return None


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
