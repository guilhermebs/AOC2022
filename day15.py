import os
import time
import re
from dataclasses import dataclass, field
from typing import List


def solve():
    input_file_contents = open(os.path.join("input", "day15")).read().rstrip()

    sensors: List[Sensor] = []

    regex = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    for line in input_file_contents.splitlines():
        m = re.match(regex, line)
        sensors.append(Sensor(
            (int(m.group(1)), int(m.group(2))),
            (int(m.group(3)), int(m.group(4))),
            )
        )

    line_number = 2000000
    sol_part1 = sum(interval[1] - interval[0] for interval in 
                    find_covered_intervals(sensors, line_number))
    print("Part 1:", sol_part1)

    max_coord = 4000000
    for y in range(0, max_coord):
        if y % 1000 == 0:
            print(y, end="\r")
        interval = find_covered_intervals(sensors, y)
        if len(interval) > 1 or interval[0][0] > 0 or interval[0][1] < max_coord:
            interval = sorted(interval)
            break
    if len(interval) > 1:
        x = interval[0][1] + 1
    if len(interval) == 1:
        if interval[0][0] > 0:
            x = 0
        if interval[0][1] < max_coord:
            x = max_coord
    sol_part2 = y + x * max_coord
    print("Part 2:", sol_part2)


@dataclass
class Sensor:
    position: tuple
    closest_beacon: tuple
    dist2closest: int = field(init=False)

    def __post_init__(self):
        self.dist2closest = sum(abs(p - b) for p, b in zip(self.position, self.closest_beacon))


def find_covered_intervals(sensors, line_y):
    intervals_covered = []
    for sensor in sensors:
        x_range = sensor.dist2closest - abs(sensor.position[1] - line_y)
        if x_range > 0:
            start, end = sensor.position[0] - x_range, sensor.position[0] + x_range
            intervals_covered.append(
                (start, end)
            )
    return merge_intervals(intervals_covered)


def merge_intervals(intervals):
    while True:
        removed = []
        merged_intervals = []
        for i, (i_start, i_end) in enumerate(intervals):
            if i in removed:
                continue
            for j, (j_start, j_end) in enumerate(intervals[i+1:]):
                if j + i + 1 in removed:
                    continue
                if (i_start <= j_start <= i_end or
                        i_start <= j_end <= i_end or
                        j_start <= i_start <= j_end or
                        j_start <= i_end <= j_end):
                    start = min(i_start, j_start)
                    end = max(i_end, j_end)
                    merged_intervals.append((start, end))
                    removed.append(j + i + 1)
                    break
            else:
                merged_intervals.append((i_start, i_end))
        intervals = merged_intervals
        if len(removed) == 0:
            break

    return intervals

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
