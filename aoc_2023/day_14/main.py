from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from aoc_2023.utils.matrix import BoundedMatrix, rotate_clockwise
from typing import Literal

Boulder = Literal["0"]
Empty = Literal["."]
Rock = Literal["#"]
Item = Boulder | Empty | Rock


class Parabola(BoundedMatrix[Item]):
    def to_string(self) -> str:
        return "".join("".join(row) for row in self.data)

    def __hash__(self) -> str:
        return hash(self.to_string())

    def __eq__(self, other: "Parabola") -> bool:
        return self.data == other.data


TILT_AMOUNT = 1000000000


def load_and_solve_part_1() -> int:
    input = load_file(14)
    return solve_part_1(input)


def solve_part_1(input: str):
    parabola = parse_input(input)
    tilted_north = tilt_parabola(parabola)
    # tilted_north = tilt_parabola_multiple(parabola, 1)
    return get_parabola_load(tilted_north)


def parse_input(input: str) -> list[str]:
    return Parabola([list(v) for v in split_by_newline(input)])


def tilt_parabola(parabola: Parabola) -> Parabola:
    new_columns: list[list[Item]] = []
    for column in parabola.get_columns():
        new_columns.append(tilt_parabola_column(column))
    return Parabola(new_columns).transpose()


def tilt_parabola_column(col: list[Item]) -> list[Item]:
    new_column: list[Item] = []
    open_spots = 0
    for item in col:
        if item == "O":
            new_column.append("O")
        if item == ".":
            open_spots += 1
        if item == "#":
            for _ in range(open_spots):
                new_column.append(".")
            new_column.append("#")
            open_spots = 0
    # If we just end on open spots
    for _ in range(open_spots):
        new_column.append(".")
    return new_column


def get_parabola_load(parabola: Parabola) -> int:
    return sum(get_parabola_load_column(col) for col in parabola.get_columns())


def get_parabola_load_column(col: list[Item]) -> int:
    load = 0
    height = len(col)
    for i, item in enumerate(col):
        if item == "O":
            load += height - i
    return load


def load_and_solve_part_2() -> int:
    input = load_file(14)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    parabola = parse_input(input)
    tilted = tilt_parabola_multiple(parabola, TILT_AMOUNT)
    return get_parabola_load(tilted)


def tilt_parabola_multiple(parabola: Parabola, amount: int) -> Parabola:
    previous: dict[Parabola, int] = {}
    index = 0
    tilted = parabola
    while index < amount:
        tilted = tilt_parabola_four_directions(tilted)
        index += 1
        if last_time := previous.get(tilted):
            cycle = index - last_time
            amount_left = amount - index
            skip_cycles = amount_left // cycle
            index += cycle * skip_cycles
        previous[tilted] = index
    return tilted


def tilt_parabola_four_directions(parabola: Parabola) -> Parabola:
    tilted = parabola
    for _ in range(4):
        tilted = tilt_parabola(tilted)
        tilted = rotate_clockwise(tilted)
    return tilted


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
