from collections import namedtuple
import copy
from dataclasses import dataclass
from functools import reduce
import heapq
from math import ceil
import os
import time
from typing import List

MATERIALS: List[str] = [
    "ore",
    "clay",
    "obsidian",
    "geode"
]

Recipe = namedtuple("Recipe", MATERIALS)

Minerals = namedtuple("Minerals", MATERIALS)

Robots = namedtuple("Robots", MATERIALS)


def solve():
    input_file_contents = open(os.path.join("input", "day19")).read().rstrip()

    all_blueprints = []
    for line in input_file_contents.splitlines():
        recipes = []
        for recipe_str in line.split(": ")[1].split(". "):
            recipe = {m: 0 for m in MATERIALS}
            recipe_words = recipe_str.split()
            recipe |= {n.strip("."): int(a) for n, a in zip(recipe_words[5::3], recipe_words[4::3])}
            recipes.append(Recipe(**recipe))
        all_blueprints.append(recipes)

    sol_part1 = sum(
        (i+1) * max_geode_collected(recipes, 24)
        for i, recipes in enumerate(all_blueprints)
    )
    print("Part 1:", sol_part1)

    sol_part2 = reduce(
        lambda x, y: x*y, (max_geode_collected(recipes, 32) for recipes in all_blueprints[:3])
    )
    print("Part 2:", sol_part2)


@dataclass(eq=True, frozen=True, order=True)
class State:
    t: int
    robots: Robots
    minerals: Minerals

    def descendents(self, recipes: List[Recipe], max_t):
        result = set()
        for robot_idx, requirements in enumerate(recipes):
            if any(req > 0 and rob == 0 for req, rob in zip(requirements, self.robots)):
                continue
            else:
                time2build = max(
                    int(ceil((req - mnr)/rob)) + 1 if rob > 0 else 0 for req, mnr, rob in
                    zip(requirements, self.minerals, self.robots)
                )
                time2build = max(time2build, 1)

                if self.t + time2build >= max_t:
                    time2end = max_t - self.t
                    new_minerals = Minerals(
                        *tuple(mnr + rob * time2end for mnr, rob in
                            zip(self.minerals, self.robots))
                    )
                    result.add(State(max_t, self.robots, new_minerals))
                    continue

                new_minerals = Minerals(
                    *tuple(mnr + rob * time2build - req for req, mnr, rob in
                           zip(requirements, self.minerals, self.robots))
                )
                new_robots = list(self.robots)
                new_robots[robot_idx] += 1
                result.add(State(self.t + time2build, Robots(*new_robots), new_minerals))

        return result

    def heuristic(self, max_t):
        # we build one geode robot every minute until the end
        time_left = max_t - self.t
        return self.minerals.geode + self.robots.geode * time_left + 1/2*time_left*(time_left - 1)


def max_geode_collected(recipes, max_t):
    robots = Robots(ore=1, clay=0, obsidian=0, geode=0)
    minerals = Minerals(ore=0, clay=0, obsidian=0, geode=0)
    init_state = State(0, robots, minerals)
    states = [
        (-init_state.heuristic(max_t), init_state)
    ]
    heapq.heapify(states)
    seen = set()
    max_geodes = 0
    while len(states) > 0:
        h, s = heapq.heappop(states)
        if s.minerals.geode > max_geodes:
            max_geodes = s.minerals.geode
        if s.t == max_t:
            continue
        if -h <= max_geodes:
            break

        descendents = s.descendents(recipes, max_t)
        for ds in descendents - seen:
            if (h := ds.heuristic(max_t)) > max_geodes:
                heapq.heappush(states, (-h, ds))
                seen.add(ds)

    return max_geodes



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
