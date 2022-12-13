from collections import deque
from dataclasses import dataclass

from aoc_2022.utils.matrix import BoundedMatrix
from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark
from aoc_2022.utils.space import Coordinate, Direction, move_from_coordinate

START = "S"
GOAL = "E"
LOWEST = "a"
HIGHEST = "z"


@dataclass(frozen=True)
class Location:
    x: int
    y: int
    cost: int

    @property
    def coordinate(self):
        return Coordinate(self.x, self.y)


def can_go_to(from_: Coordinate, to_: Coordinate, map: BoundedMatrix[str]) -> bool:
    from_height = map.get_from_coordinate(from_)
    to_height = map.get_from_coordinate(to_)
    if from_height is None or to_height is None:
        return False
    if to_height == GOAL:
        return from_height == HIGHEST
    if from_height == START:
        return to_height == LOWEST
    return ord(to_height) - ord(from_height) <= 1


def is_goal(loc: Coordinate, map: BoundedMatrix[str]) -> bool:
    height = map.get_from_coordinate(loc)
    return height == GOAL


def find_goal(map: BoundedMatrix[str]) -> Coordinate:
    for i, j, value in map:
        if value == GOAL:
            return Coordinate(i, j)
    raise ValueError("Could not find goal")


def find_start(map: BoundedMatrix[str]) -> Coordinate:
    for i, j, value in map:
        if value == START:
            return Coordinate(i, j)
    raise ValueError("Could not find start")


def initialse(map: BoundedMatrix[str]) -> Location:
    start = find_start(map)
    return Location(start.x, start.y, 0)


def solve_puzzle_upwards(map: BoundedMatrix[str]) -> int:
    directions = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)

    next_steps = deque([initialse(map)])
    visited: dict[Coordinate, Location] = {}
    min_cost = int(1e10)

    while next_steps:
        current = next_steps.popleft()
        for d in directions:
            next_coord = move_from_coordinate(current.coordinate, d)
            if not can_go_to(current.coordinate, next_coord, map):
                continue
            new_cost = current.cost + 1
            if is_goal(next_coord, map):
                min_cost = min(new_cost, min_cost)
                continue
            if next_coord in visited:
                old_loc = visited[next_coord]
                if new_cost >= old_loc.cost:
                    continue
                next_steps.remove(old_loc)
            new_loc = Location(
                next_coord.x,
                next_coord.y,
                new_cost,
            )
            visited[next_coord] = new_loc
            next_steps.append(new_loc)
    return min_cost


def is_goal_down(loc: Coordinate, map: BoundedMatrix[str]) -> bool:
    height = map.get_from_coordinate(loc)
    return height == LOWEST or height == START


def can_go_to_down(from_: Coordinate, to_: Coordinate, map: BoundedMatrix[str]) -> bool:
    from_height = map.get_from_coordinate(from_)
    to_height = map.get_from_coordinate(to_)
    if from_height is None or to_height is None:
        return False
    if to_height == START:
        to_height = LOWEST

    if from_height == GOAL:
        return to_height == HIGHEST
    return ord(from_height) - ord(to_height) <= 1


def initialse_down(map: BoundedMatrix[str]) -> Location:
    end = find_goal(map)
    return Location(end.x, end.y, 0)


def solve_puzzle_downwards(map: BoundedMatrix[str]) -> int:
    directions = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)

    next_steps = deque([initialse_down(map)])
    visited: dict[Coordinate, Location] = {}
    min_cost = int(1e10)

    while next_steps:
        current = next_steps.popleft()
        for d in directions:
            next_coord = move_from_coordinate(current.coordinate, d)
            if not can_go_to_down(current.coordinate, next_coord, map):
                continue
            new_cost = current.cost + 1
            if is_goal_down(next_coord, map):
                min_cost = min(new_cost, min_cost)
                continue
            if next_coord in visited:
                old_loc = visited[next_coord]
                if new_cost >= old_loc.cost:
                    continue
                next_steps.remove(old_loc)
            new_loc = Location(
                next_coord.x,
                next_coord.y,
                new_cost,
            )
            visited[next_coord] = new_loc
            next_steps.append(new_loc)
    return min_cost


def parse_input(input: str) -> BoundedMatrix[str]:
    lines = split_by_newline(input)
    return BoundedMatrix([list(line) for line in lines])


def load_and_solve_part_1() -> int:
    input = load_file(12)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    map = parse_input(input)
    return solve_puzzle_upwards(map)


def load_and_solve_part_2() -> int:
    input = load_file(12)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    map = parse_input(input)
    return solve_puzzle_downwards(map)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
