from collections import Counter
from dataclasses import dataclass
import itertools
import os
import time
from typing import NewType, Tuple


Direction = NewType("Direction", Tuple[int, int])


@dataclass(frozen=True)
class Move:
    direction: Direction
    free_tiles: Tuple[Direction, Direction, Direction]


MOVES = (
    Move(( 0,-1), (( 1,-1), ( 0,-1), (-1,-1))),
    Move(( 0, 1), (( 1, 1), ( 0, 1), (-1, 1))),
    Move((-1, 0), ((-1,-1), (-1, 0), (-1, 1))),
    Move(( 1, 0), (( 1,-1), ( 1, 0), ( 1, 1))),
)


def solve():
    input_file_contents = open(os.path.join("input", "day23")).read().rstrip()

    start_positions = set(itertools.chain.from_iterable(
            [(i, j) for i, c in enumerate(row) if c == "#"]
            for j, row in enumerate(input_file_contents.splitlines())
    ))

    elve_positions = start_positions
    for i in range(10):
        im = i % len(MOVES)
        proposed = propose_moves(elve_positions, im)
        elve_positions = move_elves(proposed)

    sol_part1 = count_empty_tiles(elve_positions)
    print("Part 1:", sol_part1)

    new_positions = start_positions
    elve_positions = None
    i = 0
    while new_positions != elve_positions:
        elve_positions = new_positions
        proposed = propose_moves(elve_positions, i % len(MOVES))
        new_positions = move_elves(proposed)
        i += 1

    sol_part2 = i
    print("Part 2:", sol_part2)


def print_positions(elve_positions):
    bb = get_bounding_box(elve_positions)
    print("\n".join(
        "".join("#" if (i, j) in elve_positions else "." for i in range(bb[0][0], bb[1][0] + 1)) + f" {j}"
        for j in range(bb[0][1], bb[1][1] + 1)
    ))


def get_bounding_box(elve_positions):
    return (
        (min(i for i, _ in elve_positions), min(j for _, j in elve_positions)),
        (max(i for i, _ in elve_positions), max(j for _, j in elve_positions)),
    )


def propose_moves(elve_positions, prefered_move):
    result = []
    for elve in elve_positions:
        if all(
                (elve[0] + i, elve[1] + j) not in elve_positions
                for i, j in itertools.product(range(-1, 2), range(-1, 2)) if not (i == j == 0)):
            result.append((elve, elve))
            continue
        for im in range(len(MOVES)):
            move = MOVES[(prefered_move + im) % len(MOVES)]
            if all((elve[0] + i, elve[1] + j) not in elve_positions for i, j in move.free_tiles):
                result.append((
                    elve,
                    (elve[0] + move.direction[0], elve[1] + move.direction[1])
                ))
                break
        # all directions busy
        else:
            result.append((elve, elve))

    return result


def move_elves(propose_moves):
    new_positions = []
    proposed_count = Counter(p[1] for p in propose_moves)
    for elve, new_pos in propose_moves:
        if proposed_count[new_pos] == 1:
            new_positions.append(new_pos)
        else:
            new_positions.append(elve)

    assert len(set(new_positions)) == len(propose_moves)
    return set(new_positions)


def count_empty_tiles(elve_positions):
    bb = get_bounding_box(elve_positions)
    area = (bb[1][0] - bb[0][0] + 1) * (bb[1][1] - bb[0][1] + 1)
    return area - len(elve_positions)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
