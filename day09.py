import os
import time
import math
import copy


def move_knot(front_knot, back_knot):
    if (abs(back_knot[0] - front_knot[0]) > 1 or
            abs(back_knot[1] - front_knot[1]) > 1):
        for i in range(2):
            if front_knot[i] != back_knot[i]:
                back_knot[i] += int(math.copysign(1, front_knot[i] - back_knot[i]))

def solve():
    input_file_contents = open(os.path.join("input", "day09")).read().rstrip()

    moves = []
    for line in input_file_contents.splitlines():
        direction, steps = line.split(" ")
        moves.append((direction, int(steps)))

    head_position = [0, 0]
    tail_position = [0, 0]
    visited = [tuple(tail_position)]

    for move in moves:
        for _ in range(move[1]):
            last_head_position = copy.deepcopy(head_position)
            if move[0] == "R":
                head_position[0] += 1
            if move[0] == "L":
                head_position[0] -= 1
            if move[0] == "U":
                head_position[1] += 1
            if move[0] == "D":
                head_position[1] -= 1

            if (abs(head_position[0] - tail_position[0]) > 1 or
                    abs(head_position[1] - tail_position[1]) > 1):
                tail_position = last_head_position
                visited.append(tuple(tail_position))

    sol_part1 = len(set(visited))
    print("Part 1:", sol_part1)

    n_knots = 10
    knots_positions = [[0, 0] for _ in range(n_knots)]
    visited = [tuple(knots_positions[-1])]
    for move in moves:
        for _ in range(move[1]):
            if move[0] == "R":
                knots_positions[0][0] += 1
            if move[0] == "L":
                knots_positions[0][0] -= 1
            if move[0] == "U":
                knots_positions[0][1] += 1
            if move[0] == "D":
                knots_positions[0][1] -= 1

            for k_front, k_back in zip(knots_positions, knots_positions[1:]):
                move_knot(k_front, k_back)

            visited.append(tuple(knots_positions[-1]))

    sol_part2 = len(set(visited))
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
