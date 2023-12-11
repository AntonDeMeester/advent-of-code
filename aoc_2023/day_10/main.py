from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from aoc_2023.utils.matrix import BoundedMatrix
from aoc_2023.utils.space import Coordinate, move_from_coordinate, Direction

START_REAL_VALUE = "|"


class Pipe:
    def __init__(self, value: str, coord: Coordinate):
        self.coord = coord
        self.value = value
        self.distance_from_start: int | None = None
        self.is_linked_to_start = False
        self.is_start = False

    def __hash__(self):
        return hash(self.coord)

    def __str__(self):
        return f"{self.value} at ({self.coord.x}, {self.coord.y}) at distance {self.distance_from_start or -1}"

    def __repr__(self):
        return f"{self.value} at ({self.coord.x}, {self.coord.y}) at distance {self.distance_from_start or -1}"


class PipeMap(BoundedMatrix[Pipe]):
    def get_linked_pipes(self, pipe: Pipe) -> list[Pipe]:
        north, east, south, west = False, False, False, False
        if pipe.value == "|":
            north, south = True, True
        elif pipe.value == "-":
            east, west = True, True
        elif pipe.value == "L":
            north, east = True, True
        elif pipe.value == "J":
            north, west = True, True
        elif pipe.value == "7":
            south, west = True, True
        elif pipe.value == "F":
            south, east = True, True

        connecting: list[Pipe] = []
        if north:
            north_value = self.get_from_coordinate(move_from_coordinate(pipe.coord, Direction.UP))
            if north_value is not None:
                connecting.append(north_value)
        if east:
            east_value = self.get_from_coordinate(move_from_coordinate(pipe.coord, Direction.RIGHT))
            if east_value is not None:
                connecting.append(east_value)
        if south:
            south_value = self.get_from_coordinate(move_from_coordinate(pipe.coord, Direction.DOWN))
            if south_value is not None:
                connecting.append(south_value)
        if west:
            west_value = self.get_from_coordinate(move_from_coordinate(pipe.coord, Direction.LEFT))
            if west_value is not None:
                connecting.append(west_value)

        return connecting


def load_and_solve_part_1() -> int:
    input = load_file(10)
    return solve_part_1(input)


def solve_part_1(input: str):
    pipe_map = parse_input(input)
    furthest = get_furthers_coordinate(pipe_map)
    return furthest.distance_from_start


def parse_input(input: str) -> list[list[int]]:
    lines = split_by_newline(input)
    return PipeMap([[Pipe(value, Coordinate(i, j)) for i, value in enumerate(line)] for j, line in enumerate(reversed(lines))])


def get_furthers_coordinate(pipe_map: PipeMap) -> Pipe:
    start = get_start_node(pipe_map)
    nodes = find_connecting_to_start(start, pipe_map)
    visited = {start}
    while nodes:
        current = nodes.pop(0)
        visited.add(current)
        connected = pipe_map.get_linked_pipes(current)
        for conn in connected:
            if conn.distance_from_start is None:
                conn.distance_from_start = current.distance_from_start + 1
            else:
                conn.distance_from_start = min(current.distance_from_start + 1, conn.distance_from_start)
                current.distance_from_start = min(conn.distance_from_start + 1, current.distance_from_start)

            if conn not in visited:
                nodes.append(conn)
    return max((pipe for _, _, pipe in pipe_map), key=lambda pipe: pipe.distance_from_start or -1)


def get_start_node(pipe_map: PipeMap) -> Pipe:
    for _, _, pipe in pipe_map:
        if pipe.value == "S":
            pipe.distance_from_start = 0
            pipe.is_linked_to_start = True
            return pipe
    raise ValueError("Cannot find start")


def find_connecting_to_start(start: Pipe, pipe_map: PipeMap) -> list[Pipe]:
    results: list[Pipe] = []
    for pipe in pipe_map.get_adjecent_values(start.coord):
        if pipe is None:
            continue
        if start in pipe_map.get_linked_pipes(pipe):
            pipe.distance_from_start = 1
            results.append(pipe)
    return results


def load_and_solve_part_2() -> int:
    input = load_file(10)
    return solve_part_2(input, START_REAL_VALUE)


def solve_part_2(input: str, real_start_value: str) -> int:
    pipe_map = parse_input(input)
    pipe_map = mark_linked_pipes(pipe_map, real_start_value)
    count = get_count_enclosed_pipes(pipe_map)
    return count


def mark_linked_pipes(pipe_map: PipeMap, real_start_value: str) -> PipeMap:
    start = get_start_node(pipe_map)
    nodes = find_connecting_to_start(start, pipe_map)
    start.value = real_start_value
    start.is_start = True
    visited = {start}
    while nodes:
        current = nodes.pop(0)
        visited.add(current)
        current.is_linked_to_start = True
        connected = pipe_map.get_linked_pipes(current)
        for conn in connected:
            if conn not in visited:
                nodes.append(conn)
    return pipe_map


def get_count_enclosed_pipes(pipe_map: PipeMap) -> int:
    count = 0
    for j in range(pipe_map.vertical_length()):
        is_inside = False
        for i in range(pipe_map.horizontal_length()):
            pipe = pipe_map.get(i, j)
            if pipe is None:
                continue
            if not pipe.is_linked_to_start:
                if is_inside:
                    count += 1
                continue
            # We count when we flip from outside to inside. We only consider north connections
            if pipe.value in ("|", "L", "J"):
                is_inside = not is_inside
    return count


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
