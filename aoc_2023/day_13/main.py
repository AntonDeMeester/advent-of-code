from typing import Literal
from dataclasses import dataclass

from aoc_2023.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from aoc_2023.utils.matrix import BoundedMatrix
import math

Value = Literal[".", "#"]
Area = BoundedMatrix[Value]


@dataclass
class Symmetry:
    start: int
    end: int

    def __post_init__(self):
        self.length = int((self.end - self.start + 1) / 2)


def load_and_solve_part_1() -> int:
    input = load_file(13)
    return solve_part_1(input)


def solve_part_1(input: str):
    areas = parse_input(input)
    solutions = [solve_area(area) for area in areas]
    return sum(100 * h + v for v, h in solutions)


def parse_input(input: str) -> list[Area]:
    areas = split_by_double_newline(input)
    matrixes = [Area(split_by_newline(area)) for area in areas]
    return matrixes


def solve_area(area: Area) -> tuple[int, int]:
    vertical = find_area_symmetry(area)
    horizontal = find_area_symmetry(area.transpose())
    return (vertical, horizontal)


def find_area_symmetry(area: Area) -> int:
    possible_symmetries = find_row_symmetries(area.get_row(0))
    correct_symmetries = [symm for symm in possible_symmetries if check_symmetries(symm, area)]
    return find_symmetry_amount(correct_symmetries[0] if correct_symmetries else None)


def find_row_symmetries(row: list[Value]) -> list[Symmetry]:
    possible_symmetries: list[Symmetry] = []
    # Check from start
    start = 0
    for end in range(1, len(row), 2):
        symmetry_length = int((end - start + 1) / 2)
        for step in range(symmetry_length):
            first, last = row[start + step], row[end - step]
            if first != last:
                break
        else:
            possible_symmetries.append(Symmetry(start, end))
    # Check from end
    end = len(row) - 1
    for start in range(end - 1, -1, -2):
        symmetry_length = int((end - start + 1) / 2)
        for step in range(symmetry_length):
            first, last = row[start + step], row[end - step]
            if first != last:
                break
        else:
            possible_symmetries.append(Symmetry(start, end))
    return possible_symmetries


def check_symmetries(symm: Symmetry, area: Area) -> bool:
    for row in area.get_rows()[1:]:
        for step in range(symm.length):
            first, last = row[symm.start + step], row[symm.end - step]
            if first != last:
                return False
    return True


def find_symmetry_amount(symmetry: Symmetry | None) -> int:
    if not symmetry:
        return 0
    return symmetry.start + symmetry.length


def load_and_solve_part_2() -> int:
    input = load_file(13)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    areas = parse_input(input)
    solutions = [solve_area_with_one_off(area) for area in areas]
    return sum(100 * h + v for v, h in solutions)


def solve_area_with_one_off(area: Area) -> tuple[int, int]:
    vertical = find_symmetry_with_one_off(area)
    horizontal = find_symmetry_with_one_off(area.transpose())
    return (vertical, horizontal)


def find_symmetry_with_one_off(area: Area) -> int:
    symmetry = find_row_symmetries_with_one_off(area)
    return find_symmetry_amount(symmetry)


def find_row_symmetries_with_one_off(area: Area) -> Symmetry | None:
    # Check from start
    start = 0
    for end in range(1, area.horizontal_length(), 2):
        if check_if_symmetry_is_one_off(area, end, True):
            return Symmetry(start, end)
    # Check from end
    end = area.horizontal_length() - 1
    for start in range(end - 1, -1, -2):
        if check_if_symmetry_is_one_off(area, start, False):
            return Symmetry(start, end)
    return None


def check_if_symmetry_is_one_off(area: Area, end: int, forward: bool) -> bool:
    differences = 0
    direction = 1 if forward else -1
    start = 0 if forward else (area.horizontal_length() - 1)
    length = int(abs(end - start) / 2)
    for row in area.get_rows():
        for step in range(length + 1):
            first, last = row[start + step * direction], row[end - step * direction]
            if first != last:
                differences += 1
            if differences > 1:
                return False
    return differences == 1


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
