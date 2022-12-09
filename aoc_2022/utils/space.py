from dataclasses import dataclass
from enum import Enum


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
