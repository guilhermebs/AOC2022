from dataclasses import dataclass
import os
import re
import time

FREE = "."
WALL = "#"
END = " "

BLOCKS = {
    (0, 1): 1,
    (0, 2): 2,
    (1, 1): 3,
    (2, 0): 4,
    (2, 1): 5,
    (3, 0): 6,
}

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def solve():
    input_file_contents = open(os.path.join("input", "day22")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "test")).read().rstrip()

    monkey_map = input_file_contents.split("\n\n")[0].splitlines()
    # Homogenize widths
    width = max(len(r) for r in monkey_map)
    monkey_map = [r + END * (width - len(r)) for r in monkey_map]

    instructions = [
        (int(a), d) for a, d in re.findall(r"(\d+)(\D?)", input_file_contents.split("\n\n")[1])
    ]
    pos = Position(0, monkey_map[0].index(FREE), 0)

    for ammount, turn_dir in instructions:
        pos = move(monkey_map, pos, ammount)
        pos = turn(pos, turn_dir)

    sol_part1 = 1000 * (pos.y + 1) + 4 * (pos.x + 1) + pos.direction
    print("Part 1:", sol_part1)

    pos = Position(0, monkey_map[0].index(FREE), 0)
    for ammount, turn_dir in instructions:
        pos = move_pt2(monkey_map, pos, ammount)
        pos = turn(pos, turn_dir)

    sol_part2 = 1000 * (pos.y + 1) + 4 * (pos.x + 1) + pos.direction
    print("Part 2:", sol_part2)


@dataclass(frozen=True)
class Position:
    y: int
    x: int
    direction: int


def move(monkey_map, pos, ammount):
    for _ in range(ammount):
        # West
        if pos.direction == 0:
            new_y, new_x = pos.y, next_cell(monkey_map[pos.y], pos.x, 1)
        # South
        elif pos.direction == 1:
            new_y, new_x = next_cell([r[pos.x] for r in monkey_map], pos.y, 1), pos.x
        # East
        elif pos.direction == 2:
            new_y, new_x = pos.y, next_cell(monkey_map[pos.y], pos.x, -1)
        # North
        elif pos.direction == 3:
            new_y, new_x = next_cell([r[pos.x] for r in monkey_map], pos.y, -1), pos.x

        if monkey_map[new_y][new_x] == WALL:
            return pos
        else:
            pos = Position(new_y, new_x, pos.direction)

    return pos


def next_cell(row_or_col, idx, direction):
    for i in range(1, len(row_or_col)):
        next_idx = (idx + i * direction) % len(row_or_col)
        if row_or_col[next_idx] != END:
            return next_idx


def turn(pos, turn_dir):
    if turn_dir == "R":
        new_direction = (pos.direction + 1) % 4
    elif turn_dir == "L":
        new_direction = (pos.direction - 1) % 4
    elif turn_dir == "":
        new_direction = pos.direction
    else:
        raise ValueError("Invalid turn direction")
    return Position(pos.y, pos.x, new_direction)


def move_pt2(monkey_map, pos, ammount):
    N = 50
    for _ in range(ammount):
        if pos.direction == RIGHT:
            next_y, next_x = pos.y, pos.x + 1
        elif pos.direction == DOWN:
            next_y, next_x = pos.y + 1, pos.x
        elif pos.direction == LEFT:
            next_y, next_x = pos.y, pos.x - 1
        elif pos.direction == UP:
            next_y, next_x = pos.y - 1, pos.x

        """
        - 1 2
        - 3 -
        4 5 -
        6 - -
        """

        block_nr = BLOCKS[(pos.y//N, pos.x//N)]
        # if we are in block 1 and go up, we end up in block 6, facing right
        if block_nr == 1 and next_y == -1:
            wraped_y, wraped_x = 3 * N + next_x % N, 0
            wraped_dir = RIGHT
        # if we are in block 1 and go left, we end up in block 4, facing right
        elif block_nr == 1 and next_x == N - 1:
            wraped_y, wraped_x = 3 * N - next_y % N - 1, 0
            wraped_dir = RIGHT
        # if we are in block 2 and go up, we end up in block 6, facing up
        elif block_nr == 2 and next_y == -1:
            wraped_y, wraped_x = 4 * N - 1, next_x % N
            wraped_dir = UP
        # if we are in block 2 and go right, we end up in block 5, going left
        elif block_nr == 2 and next_x == 3 * N:
            wraped_y, wraped_x = 3 * N - next_y % N - 1, 2 * N - 1
            wraped_dir = LEFT
        # if we are in block 2 and go down, we end up in block 3 going left
        elif block_nr == 2 and next_y == N:
            wraped_y, wraped_x = N + next_x % N, 2 * N - 1
            wraped_dir = LEFT
        # if we are in block 3 and go left, we end up in block 4 going down
        elif block_nr == 3 and next_x == N - 1:
            wraped_y, wraped_x = 2 * N, next_y % N
            wraped_dir = DOWN
        # if we are in block 3 and go right, we end up in block 2 going up
        elif block_nr == 3 and next_x == 2 * N:
            wraped_y, wraped_x = N - 1, 2 * N + next_y % N
            wraped_dir = UP
        # if we are in block 4 and go up, we end up in block 3 going right
        elif block_nr == 4 and next_y == 2 * N - 1:
            wraped_y, wraped_x = N + next_x % N, N
            wraped_dir = RIGHT
        # if we are in block 4 and go left, we end up in block 1 going right
        elif block_nr == 4 and next_x == -1:
            wraped_y, wraped_x = N - next_y % N - 1, N
            wraped_dir = RIGHT
        # if we are in block 5 and go right, we end up in block 2 going left
        elif block_nr == 5 and next_x == 2 * N:
            wraped_y, wraped_x = N - next_y % N - 1, 3 * N - 1
            wraped_dir = LEFT
        # if we are in block 5 and go down we end up in block 6 going left
        elif block_nr == 5 and next_y == 3 * N:
            wraped_y, wraped_x = next_x % N + 3 * N, N - 1
            wraped_dir = LEFT
        # if we are in block 6 and go right we end up in block 5 going up
        elif block_nr == 6 and next_x == N:
            wraped_y, wraped_x = 3 * N - 1, next_y % N + N
            wraped_dir = UP
        # if we are in block 6 and go down, we end up in block 2, going down
        elif block_nr == 6 and next_y == 4 * N:
            wraped_y, wraped_x = 0, next_x % N + 2 * N,
            wraped_dir = DOWN
        # if we are in block 6 and go left, we end up in block 1 going down
        elif block_nr == 6 and next_x == -1:
            wraped_y, wraped_x = 0, next_y % N + N
            wraped_dir = DOWN
        # no wraping 
        else:
            wraped_y, wraped_x = next_y, next_x
            wraped_dir = pos.direction

        if monkey_map[wraped_y][wraped_x] == WALL:
            return pos
        wraped_pos = Position(wraped_y, wraped_x, wraped_dir)
        wraped_block_nr = BLOCKS[(wraped_y//N, wraped_x//N)]
        if sorted((block_nr, wraped_block_nr)) in [(1, 5), (2, 4), (3, 6)]:
            raise ValueError("impossible transition!")

        pos = wraped_pos
        assert monkey_map[pos.y][pos.x] != END

    return pos


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
