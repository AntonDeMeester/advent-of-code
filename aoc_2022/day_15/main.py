import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.regex import NUMBER_REGEX
from aoc_2022.utils.run import run_and_benchmark
from aoc_2022.utils.space import Coordinate, Direction, Range, get_manhattan_distance, merge_ranges, move_from_coordinate


class Occupation(Enum):
    sensor = "sensor"
    beacon = "beacon"
    not_beacon = "not_beacon"


class Map:
    def __init__(self, target_row: int):
        self.not_beacon_rows: dict[int, list[Range]] = defaultdict(list)
        self.static_places: dict[Coordinate, Occupation] = {}
        self.target_row = target_row

    def add_static(self, coordinate: Coordinate, value: Occupation) -> "Map":
        self.static_places[coordinate] = value
        return self

    def add_not_beacon_row(self, from_: Coordinate, to_: Coordinate) -> "Map":
        if from_.y != to_.y:
            raise ValueError("Can only add rows")
        row = from_.y
        if row != self.target_row:
            # Skip
            return self
        self.not_beacon_rows[row] = merge_ranges([*self.not_beacon_rows[row], Range(from_.x, to_.x)])
        return self

    def get_not_becaons_places_in_row(self, row: int) -> int:
        non_beacon_rows = self.not_beacon_rows[row]
        non_beacon_count = sum(x2 - x1 + 1 for x1, x2 in non_beacon_rows)
        static_count = sum(1 for coord in self.static_places.keys() if coord.y == row)
        return non_beacon_count - static_count


@dataclass(frozen=True)
class Sensor:
    sensor: Coordinate
    closest_beacon: Coordinate

    @property
    def distance(self):
        return get_manhattan_distance(self.sensor, self.closest_beacon)

    def __str__(self) -> str:
        first = f"Sensor at x={self.sensor.x}, y={self.sensor.y}:"
        second = f"closest beacon is at x={self.closest_beacon.x}, y={self.closest_beacon.y}"
        return f"{first} {second}"


def parse_line(line: str) -> Sensor:
    pattern = f"Sensor at x=({NUMBER_REGEX}), y=({NUMBER_REGEX}): closest beacon is at x=({NUMBER_REGEX}), y=({NUMBER_REGEX})"
    parsed = re.match(pattern, line)
    assert parsed is not None
    return Sensor(Coordinate(int(parsed[1]), int(parsed[2])), Coordinate(int(parsed[3]), int(parsed[4])))


def parse_input(input: str) -> list[Sensor]:
    lines = split_by_newline(input)
    return [parse_line(line) for line in lines]


def process_sensor(sensor: Sensor, map: Map) -> Map:
    map = map.add_static(sensor.sensor, Occupation.sensor)
    map = map.add_static(sensor.closest_beacon, Occupation.beacon)

    distance = get_manhattan_distance(sensor.sensor, sensor.closest_beacon)
    distance_to_row = abs(map.target_row - sensor.sensor.y)

    if distance_to_row > distance:
        return map

    x_diff = distance - distance_to_row
    up_or_down_of_sensor = Coordinate(sensor.sensor.x, map.target_row)
    left = move_from_coordinate(up_or_down_of_sensor, Direction.LEFT, x_diff)
    right = move_from_coordinate(up_or_down_of_sensor, Direction.RIGHT, x_diff)

    return map.add_not_beacon_row(left, right)


def generate_map(sensors: list[Sensor], target_row: int) -> Map:
    map = Map(target_row)
    for sens in sensors:
        map = process_sensor(sens, map)
    return map


def load_and_solve_part_1() -> int:
    y = 2000000
    input = load_file(15)
    return solve_part_1(input, y)


def solve_part_1(input: str, row: int) -> int:
    sensors = parse_input(input)
    map = generate_map(sensors, row)
    return map.get_not_becaons_places_in_row(row)


# Part 2


def generate_edge_nodes(sensor: Sensor) -> set[Coordinate]:
    edges: set[Coordinate] = set()
    just_beyond_distance = sensor.distance + 1
    for x in range(0, just_beyond_distance + 1):
        y = just_beyond_distance - x

        top = move_from_coordinate(sensor.sensor, Direction.UP, y)
        edges.add(move_from_coordinate(top, Direction.LEFT, x))
        edges.add(move_from_coordinate(top, Direction.RIGHT, x))

        bottom = move_from_coordinate(sensor.sensor, Direction.DOWN, y)
        edges.add(move_from_coordinate(bottom, Direction.LEFT, x))
        edges.add(move_from_coordinate(bottom, Direction.RIGHT, x))

    return edges


def is_edge_node_taken(edge: Coordinate, sensor: Sensor) -> bool:
    return get_manhattan_distance(edge, sensor.sensor) <= sensor.distance


def is_edge_out_of_bounds(edge: Coordinate, middle: int) -> bool:
    return edge.x < 0 or edge.y < 0 or edge.x > middle * 2 or edge.y > middle * 2


def is_open_edge_node(edge: Coordinate, sensors: list[Sensor], search_index: int, middle: int) -> bool:
    if is_edge_out_of_bounds(edge, middle):
        return False
    for i, sensor in enumerate(sensors):
        if i == search_index:
            continue
        if is_edge_node_taken(edge, sensor):
            return False
    return True


def find_broken_beacon(sensors: list[Sensor], middle: int) -> Coordinate:
    for search_index, search_sensor in enumerate(sensors):
        edge_nodes = generate_edge_nodes(search_sensor)
        for edge in edge_nodes:
            if is_open_edge_node(edge, sensors, search_index, middle):
                return edge
    raise ValueError("Couldn't find open spot")


def load_and_solve_part_2() -> int:
    input = load_file(15)
    return solve_part_2(input, 2000000)


def score_broken_beacon(coordinate: Coordinate) -> int:
    return coordinate.x * 4000000 + coordinate.y


def solve_part_2(input: str, middle: int) -> int:
    sensors = parse_input(input)
    broken_beacon = find_broken_beacon(sensors, middle)
    return score_broken_beacon(broken_beacon)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
