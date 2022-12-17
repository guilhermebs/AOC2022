from dataclasses import dataclass
import os
import re
import time
from typing import Dict, List, Set, Tuple


def solve():
    input_file_contents = open(os.path.join("input", "day16")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "day16_example")).read().rstrip()
    valves: Dict[str, Valve] = {}
    regex = re.compile(r"Valve (\w+) has flow rate=(\d+);")
    for line in input_file_contents.splitlines():
        m = regex.match(line)
        neighbours = [n.strip(",") for n in line.split()[9:]]
        valves[m.group(1)] = Valve(m.group(1), int(m.group(2)), neighbours)

    # Search!
    end_time = 30
    states: List[State] = [State("AA", 0, set(), 0, None, [])]
    max_pressure = 0
    while len(states) > 0:
        s = states.pop()
        if s.pressure_at_end > max_pressure:
            max_pressure = s.pressure_at_end
        if s.time < end_time:
            v = valves[s.room]
            if s.room not in s.open_valves and v.flowrate > 0:
                states.append(State(
                    s.room,
                    s.time + 1,
                    s.open_valves | set([s.room]),
                    s.pressure_at_end + ((end_time - (s.time + 1)) * v.flowrate),
                    s.room,
                    s.history + [s.room]
                ))
            # Go to another room
            for n in v.neighbours:
                # Don't just visit a room and go back without opening the valve
                if n == s.prev_room:
                    continue
                new_state = State(
                    n,
                    s.time + 1,
                    s.open_valves,
                    s.pressure_at_end,
                    s.room,
                    s.history + [s.room]
                )
                if heuristic(valves, end_time, new_state) >= max_pressure:
                    states.append(new_state)

    sol_part1 = max_pressure
    print("Part 1:", sol_part1)

    # Search!
    end_time = 26
    states: List[State] = [(None, State(("AA", "AA"), 0, set(), 0, (None, None), []))]
    max_pressure = 0
    while len(states) > 0:
        _, s = states.pop()
        if s.pressure_at_end > max_pressure:
            max_pressure = s.pressure_at_end
            # prune
            states = [(h, s) for h, s in states if h >= max_pressure]
        if s.time < end_time:
            new_rooms = list(s.room)
            inserted = []
            for r1 in [s.room[0]] + valves[s.room[0]].neighbours:
                valves_opened_r1 = set()
                additional_pressure_r1 = 0
                if r1 in s.prev_room:
                    continue
                new_rooms[0] = r1
                v1 = valves[r1]
                if r1 == s.room[0] and r1 not in s.open_valves and v1.flowrate > 0:
                    valves_opened_r1 = set([r1])
                    additional_pressure_r1 = (end_time - (s.time + 1)) * v1.flowrate
                elif r1 == s.room[0]:
                    continue
                for r2 in [s.room[1]] + valves[s.room[1]].neighbours:
                    valves_opened_r2 = set()
                    additional_pressure_r2 = 0
                    if r2 in s.prev_room:
                        continue
                    new_rooms[1] = r2
                    v2 = valves[r2]
                    if tuple(new_rooms) in inserted:
                        continue
                    if r2 == s.room[1] and r2 not in (s.open_valves | valves_opened_r1) and v2.flowrate > 0:
                        valves_opened_r2 = set([r2])
                        additional_pressure_r2 = (end_time - (s.time + 1)) * v2.flowrate
                    elif r2 == s.room[1]:
                        continue
                    new_state = State(
                        tuple(new_rooms),
                        s.time + 1,
                        s.open_valves | valves_opened_r1 | valves_opened_r2,
                        s.pressure_at_end + additional_pressure_r1 + additional_pressure_r2,
                        s.room,
                    )
                    inserted.append(tuple(new_rooms))
                    if (h := heuristic(valves, end_time, new_state, True)) >= max_pressure:
                        states.append((h, new_state))

    sol_part2 = max_pressure
    print("Part 2:", sol_part2)


@dataclass
class Valve:
    name: str
    flowrate: int
    neighbours: List[str]


@dataclass
class State:
    room: str
    time: int
    open_valves: Set[str]
    pressure_at_end: int
    prev_room: str
    history: List[str] = None


def heuristic(valves, end_time, state, pt2=False) -> int:
    result = state.pressure_at_end
    not_open = set(valves.keys()) - set(state.open_valves)
    sorted_rooms = iter(sorted(not_open, key=lambda x: valves[x].flowrate, reverse=True))
    htime = 1
    nloop = 2 if pt2 else 1
    while state.time + htime < end_time:
        for _ in range(nloop):
            try:
                result += (end_time - (state.time + htime)) * valves[next(sorted_rooms)].flowrate
            except StopIteration:
                return result
        htime += 2
    return result


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
