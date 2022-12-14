from enum import Enum

from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark
from aoc_2022.utils.space import Coordinate, Direction, move_from_coordinate


class Blocker(Enum):
    rock = "rock"
    sand = "sand"


class SandDropsInAbyssException(Exception):
    pass


class SandIsAtSourceException(Exception):
    pass


class State:
    def __init__(self, occupied_spaces: dict[Coordinate, Blocker]):
        self.occupied_spaces = occupied_spaces
        self.bottom = max(coord.y for coord in occupied_spaces.keys()) if occupied_spaces else 0
        self.left = min(coord.x for coord in occupied_spaces.keys()) if occupied_spaces else 0
        self.right = max(coord.x for coord in occupied_spaces.keys()) if occupied_spaces else 0

    def is_occupied(self, coordinate: Coordinate) -> bool:
        return coordinate in self.occupied_spaces.keys()

    def is_in_abyss(self, coordinate: Coordinate) -> bool:
        return coordinate.y > self.bottom

    def add_sand(self, coordinate: Coordinate) -> "State":
        self.occupied_spaces[coordinate] = Blocker.sand
        return self


def merge_state(first: "State", other: "State") -> "State":
    merged_spaces = {**first.occupied_spaces, **other.occupied_spaces}
    return State(merged_spaces)


def get_all_connecting_dots(start: int, end: int) -> list[int]:
    if start == end:
        return [start]
    direction = 1 if end > start else -1
    return list(range(start, end + direction, direction))


def parse_input_line(line: str) -> State:
    parsed_coords = [Coordinate(int(raw.split(",")[0]), int(raw.split(",")[1])) for raw in line.split(" -> ")]
    previous = parsed_coords.pop()

    rock_coordinates: list[Coordinate] = []
    while parsed_coords:
        current = parsed_coords.pop()
        horizontal = get_all_connecting_dots(current.x, previous.x)
        vertical = get_all_connecting_dots(current.y, previous.y)
        for h in horizontal:
            for v in vertical:
                rock_coordinates.append(Coordinate(h, v))
        previous = current
    return State({coord: Blocker.rock for coord in rock_coordinates})


def parse_input(input: str) -> State:
    lines = split_by_newline(input)
    state = State({})
    for line in lines:
        state = merge_state(state, parse_input_line(line))
    return state


def drop_level(coordinate: Coordinate, state: State) -> Coordinate | None:
    go_down = move_from_coordinate(coordinate, Direction.UP)  # Down is higher X
    if not state.is_occupied(go_down):
        return go_down
    go_down_left = move_from_coordinate(go_down, Direction.LEFT)
    if not state.is_occupied(go_down_left):
        return go_down_left
    go_down_right = move_from_coordinate(go_down, Direction.RIGHT)
    if not state.is_occupied(go_down_right):
        return go_down_right
    return None


def simulate_endless_sand_drop(state: State) -> State:
    sand_coordinate = Coordinate(500, 0)
    while True:
        dropped_sand = drop_level(sand_coordinate, state)
        if dropped_sand is None:
            return state.add_sand(sand_coordinate)
        if state.is_in_abyss(dropped_sand):
            raise SandDropsInAbyssException()
        sand_coordinate = dropped_sand


def simulate_endless_sand(state: State):
    count = 0
    while True:
        try:
            state = simulate_endless_sand_drop(state)
        except SandDropsInAbyssException:
            break
        count += 1
    return count


def add_bottom(state: State) -> State:
    start = state.left - state.bottom - 100  # Probably 3 is enough but more is better
    end = state.right + state.bottom + 100  # Probably 3 is enough but more is better
    two_under_bottom = state.bottom + 2

    bottom_coordinate = [Coordinate(x, two_under_bottom) for x in range(start, end + 1)]
    return merge_state(state, State({coord: Blocker.rock for coord in bottom_coordinate}))


def simulate_sand_drop_with_bottom(state: State) -> State:
    start = Coordinate(500, 0)
    sand_coordinate = start
    while True:
        dropped_sand = drop_level(sand_coordinate, state)
        if dropped_sand is None:
            if sand_coordinate == start:
                raise SandIsAtSourceException()
            return state.add_sand(sand_coordinate)
        sand_coordinate = dropped_sand


def simulate_sand_with_bottom(state: State):
    count = 0
    while True:
        try:
            state = simulate_sand_drop_with_bottom(state)
        except SandIsAtSourceException:
            count += 1
            break
        count += 1
    return count


def load_and_solve_part_1() -> int:
    input = load_file(14)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    state = parse_input(input)
    count = simulate_endless_sand(state)
    return count


def load_and_solve_part_2() -> int:
    input = load_file(14)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    state = parse_input(input)
    state = add_bottom(state)
    count = simulate_sand_with_bottom(state)
    return count


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
