from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
import heapq
from dataclasses import dataclass

from aoc_2023.utils.space import Direction, Coordinate, move_from_coordinate
from aoc_2023.utils.matrix import BoundedMatrix
from typing import Iterable


class Layout(BoundedMatrix[int]):
    pass


@dataclass
class Road:
    coordinate: Coordinate
    direction: Direction | None
    cost: int
    history: list[Direction]

    def __lt__(self, other: "Road") -> bool:
        return self.cost < other.cost

    def __gt__(self, other: "Road") -> bool:
        return self.cost > other.cost

    def __lte__(self, other: "Road") -> bool:
        return self.cost <= other.cost

    def __gte__(self, other: "Road") -> bool:
        return self.cost >= other.cost


def load_and_solve_part_1() -> int:
    input = load_file(17)
    return solve_part_1(input)


def solve_part_1(input: str):
    layout = parse_input(input)
    optimal = find_optimal_route(layout, Coordinate(0, 0), 1, 3)
    return optimal


def parse_input(input: str) -> Layout:
    return Layout([[int(char) for char in line] for line in split_by_newline(input)])


def find_optimal_route(layout: Layout, start: Coordinate, min_move: int, max_move: int) -> int:
    roads = [Road(start, None, 0, [])]
    visited: set[tuple[Direction, Coordinate]] = set()
    heapq.heapify(roads)
    while roads:
        current = heapq.heappop(roads)
        if is_goal(current.coordinate, layout):
            return current.cost
        if (current.direction, current.coordinate) in visited:
            continue
        visited.add((current.direction, current.coordinate))
        next_roads = get_next_road_options(current, layout, min_move, max_move)
        for next_ in next_roads:
            heapq.heappush(roads, next_)
    raise ValueError("Cannot reach goal")


def get_next_road_options(current: Road, layout: Layout, min_move: int, max_move: int) -> list[Road]:
    """Move min-max spaces to the side"""
    next_road_options: list[Road] = []
    for next_direction in get_turn_directions(current.direction):
        next_cost = current.cost
        next_coordinate = current.coordinate
        next_history = current.history
        # Move min-max forward
        for move in range(1, max_move + 1):
            next_coordinate = move_from_coordinate(next_coordinate, next_direction)
            next_location = layout.get_from_coordinate(next_coordinate)
            if next_location is None:
                break
            next_cost += next_location
            next_history = [*next_history, next_direction]
            if move < min_move:
                continue
            next_road_options.append(
                Road(
                    coordinate=next_coordinate,
                    direction=next_direction,
                    cost=next_cost,
                    history=next_history,
                )
            )
    return next_road_options


def is_goal(coord: Coordinate, layout: Layout) -> bool:
    return (coord.x == layout.horizontal_length() - 1) and (coord.y == layout.vertical_length() - 1)


def get_turn_directions(direction: Direction) -> Iterable[Direction]:
    if direction is None:
        return Direction
    if direction in (Direction.UP, Direction.DOWN):
        return (Direction.RIGHT, Direction.LEFT)
    return (Direction.UP, Direction.DOWN)


def load_and_solve_part_2() -> int:
    input = load_file(17)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    layout = parse_input(input)
    optimal = find_optimal_route(layout, Coordinate(0, 0), 4, 10)
    return optimal


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
