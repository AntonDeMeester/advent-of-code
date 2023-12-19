from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from typing import Final

from aoc_2023.utils.space import Direction, Coordinate, move_from_coordinate
from aoc_2023.utils.matrix import BoundedMatrix

VERTICAL: Final = "|"
HORIZONTAL: Final = "-"
DOWN_RIGHT: Final = "\\"
DOWN_LEFT: Final = "/"
EMPTY: Final = "."


class CaveValue:
    def __init__(self, value: str):
        self.value = value
        self.light_count = 0

    def is_lighted(self):
        return self.light_count > 0


class Cave(BoundedMatrix[CaveValue]):
    def visualise(self) -> str:
        return "\n".join("".join("#" if value.is_lighted() else "." for value in line) for line in reversed(self.get_rows()))


LightBeam = tuple[Direction, Coordinate]


def load_and_solve_part_1() -> int:
    input = load_file(16)
    return solve_part_1(input)


def solve_part_1(input: str):
    cave = parse_input(input)
    lighted_cave = light_cave(cave, (Direction.RIGHT, Coordinate(-1, cave.vertical_length() - 1)))
    return count_energised(lighted_cave)


def parse_input(input: str) -> Cave:
    return Cave([[CaveValue(v) for v in line] for line in reversed(split_by_newline(input))])


def light_cave(cave: Cave, start: LightBeam) -> Cave:
    next_steps: list[LightBeam] = [start]
    visited: set[LightBeam] = set()
    while next_steps:
        direction, coord = next_steps.pop(0)
        next_coord = move_from_coordinate(coord, direction)
        if (direction, next_coord) in visited:
            continue
        visited.add((direction, next_coord))
        next_value = cave.get_from_coordinate(next_coord)
        if next_value is None:
            continue
        next_value.light_count += 1
        next_steps.extend(get_options(direction, next_value, next_coord))
    return cave


def get_options(from_: Direction, cave_value: CaveValue, current: Coordinate) -> list[LightBeam]:
    if cave_value.value == EMPTY:
        return [(from_, current)]
    if cave_value.value == VERTICAL:
        if from_ in (Direction.DOWN, Direction.UP):
            return [(from_, current)]
        return [(Direction.DOWN, current), (Direction.UP, current)]
    if cave_value.value == HORIZONTAL:
        if from_ in (Direction.RIGHT, Direction.LEFT):
            return [(from_, current)]
        return [(Direction.RIGHT, current), (Direction.LEFT, current)]
    if cave_value.value == DOWN_RIGHT:
        if from_ == Direction.LEFT:
            return [(Direction.UP, current)]
        if from_ == Direction.DOWN:
            return [(Direction.RIGHT, current)]
        if from_ == Direction.RIGHT:
            return [(Direction.DOWN, current)]
        if from_ == Direction.UP:
            return [(Direction.LEFT, current)]
    if cave_value.value == DOWN_LEFT:
        if from_ == Direction.LEFT:
            return [(Direction.DOWN, current)]
        if from_ == Direction.DOWN:
            return [(Direction.LEFT, current)]
        if from_ == Direction.RIGHT:
            return [(Direction.UP, current)]
        if from_ == Direction.UP:
            return [(Direction.RIGHT, current)]
    raise ValueError("Wrong value")


def count_energised(cave: Cave) -> int:
    return sum(value.is_lighted() for _, _, value in cave)


def load_and_solve_part_2() -> int:
    input = load_file(16)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    cave = parse_input(input)
    lighted_cave = find_most_energised_cave(cave)
    return lighted_cave[0]


def find_most_energised_cave(initial: Cave) -> tuple[int, Cave]:
    most_energised = (0, initial)
    height, width = initial.vertical_length(), initial.horizontal_length()
    for i in range(width):
        # down
        start = (Direction.DOWN, Coordinate(i, height))
        lighted_cave = light_cave(initial.copy(), start)
        energy = count_energised(lighted_cave)
        if energy > most_energised[0]:
            most_energised = (energy, lighted_cave)

        # up
        start = (Direction.UP, Coordinate(i, -1))
        lighted_cave = light_cave(initial.copy(), start)
        energy = count_energised(lighted_cave)
        if energy > most_energised[0]:
            most_energised = (energy, lighted_cave)

    for i in range(height):
        # right
        start = (Direction.RIGHT, Coordinate(-1, i))
        lighted_cave = light_cave(initial.copy(), start)
        energy = count_energised(lighted_cave)
        if energy > most_energised[0]:
            most_energised = (energy, lighted_cave)

        # left
        start = (Direction.LEFT, Coordinate(width, i))
        lighted_cave = light_cave(initial.copy(), start)
        energy = count_energised(lighted_cave)
        if energy > most_energised[0]:
            most_energised = (energy, lighted_cave)

    return most_energised


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
