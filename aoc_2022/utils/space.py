from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class MultiValueEnm(Enum):
    """
    Enum to allow for multiple values
    See https://stackoverflow.com/questions/43202777/get-enum-name-from-multiple-values-python
    """

    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    def __repr__(self):
        return "<%s.%s: %s>" % (
            self.__class__.__name__,
            self._name_,
            ", ".join([repr(v) for v in self._all_values]),
        )


class Direction(MultiValueEnm):
    UP = "UP", "U", "NORTH", "N"
    DOWN = "DOWN", "D", "EAST", "E"
    RIGHT = "RIGHT", "R", "SOUTH", "S"
    LEFT = "LEFT", "L", "WEST", "W"


@dataclass(frozen=True, eq=True)
class Coordinate:
    x: int
    y: int


def move_from_coordinate(coordinate: Coordinate, direction: Direction, amount: int = 1) -> Coordinate:
    match direction:
        case Direction.UP:
            return Coordinate(coordinate.x, coordinate.y + amount)
        case Direction.RIGHT:
            return Coordinate(coordinate.x + amount, coordinate.y)
        case Direction.DOWN:
            return Coordinate(coordinate.x, coordinate.y - amount)
        case Direction.LEFT:
            return Coordinate(coordinate.x - amount, coordinate.y)
    raise ValueError(f"Direction {direction} not implemented")


def move_multiple_from_coordinate(coordinate: Coordinate, moves: list[tuple[Direction, int]]) -> Coordinate:
    for direction, amount in moves:
        coordinate = move_from_coordinate(coordinate, direction, amount)
    return coordinate


def get_manhattan_distance(first: Coordinate, second: Coordinate) -> int:
    return abs(first.x - second.x) + abs(first.y - second.y)


class Range(NamedTuple):
    start: int
    end: int


def merge_ranges(ranges: list[Range]) -> list[Range]:
    """
    Merges distinct ranges to a new distinct list of ranges
    Ranges do not have any requirements (4, 2) is allowed, not necessarily sorted
    """
    # Makes sure start is always lower or equal to end
    correct_sorted = [Range(x1, x2) if x1 < x2 else Range(x2, x1) for x1, x2 in ranges]
    # Make sure the ranges are sorted on the start
    sorted_ranges = sorted(correct_sorted, key=lambda x: x[0])

    new_ranges: list[Range] = []
    last = sorted_ranges[0]
    for curr in sorted_ranges[1:]:
        # We know last[0] <= curr[0]
        if last.end < curr.start:
            # Completely separate e.g. 0,2 and 3,4
            new_ranges.append(last)
            last = curr
        elif last.end >= curr.end:
            # Curr is envelopped in last e.g. 0,10 and 2,10
            continue
        elif last.end >= curr.start:
            # Overlap on ends e.g. 0,2 and 1,4
            last = Range(last.start, curr.end)
    new_ranges.append(last)
    return new_ranges
