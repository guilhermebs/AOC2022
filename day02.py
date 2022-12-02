import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day02")).read().rstrip()

    score = 0
    shape_score = {"X": 1, "Y": 2, "Z": 3}
    win = [("A", "Y"), ("B", "Z"), ("C", "X")]
    draw = [("A", "X"), ("B", "Y"), ("C", "Z")]

    for game in input_file_contents.split("\n"):
        p1, p2 = game.split()
        score += shape_score[p2]
        if (p1, p2) in win:
            score += 6
        elif (p1, p2) in draw:
            score += 3

    sol_part1 = score
    print("Part 1:", sol_part1)

    win_play = dict(win)
    draw_play = dict(draw)
    lose_play = {"A": "Z", "B": "X", "C": "Y"}
    score = 0
    for game in input_file_contents.split("\n"):
        p1, res = game.split()
        if res == "X":
            p2 = lose_play[p1]
        elif res == "Y":
            p2 = draw_play[p1]
            score += 3
        else:
            p2 = win_play[p1]
            score += 6
        score += shape_score[p2]

    sol_part2 = score
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
