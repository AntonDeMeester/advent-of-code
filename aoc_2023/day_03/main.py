from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from aoc_2023.utils.matrix import BoundedMatrix
from aoc_2023.utils.space import Coordinate

Schematic = BoundedMatrix[str | int | None]
GEAR_SYMBOL = "*"


def load_and_solve_part_1() -> int:
    input = load_file(3)
    return solve_part_1(input)


def solve_part_1(input: str):
    parsed_schematic = parse_input(input)
    numbers_with_symbols = find_numbers_with_symbols(parsed_schematic)
    return sum(numbers_with_symbols)


def parse_input(input: str) -> Schematic:
    """
    We parse each number, but we repeat if a number > 10
    e.g. 123...5. will be [123, 123, 123, None, None, None, 5, None]
    """
    lines = split_by_newline(input)
    parsed_lines: list[list[str | int | None]] = []
    for line in lines:
        parsed_line: list[str | int | None] = []
        index = 0
        while index < len(line):
            char = line[index]
            if char == ".":
                parsed_line.append(None)
                index += 1
            elif not char.isnumeric():
                parsed_line.append(char)
                index += 1
            else:
                # if it's a number
                value = int(char)
                count = 1
                index += 1
                while index < len(line):
                    char = line[index]
                    if not char.isnumeric():
                        break
                    value = value * 10 + int(char)
                    index += 1
                    count += 1
                for _ in range(count):
                    parsed_line.append(value)
        parsed_lines.append(parsed_line)
    return BoundedMatrix(parsed_lines)


def find_numbers_with_symbols(schematic: Schematic) -> list[int]:
    result: list[int] = []
    found_symbol = False
    last_y = -1
    for x, y, value in schematic:
        if last_y != y:
            found_symbol = False
        last_y = y
        if not isinstance(value, int):
            found_symbol = False
            continue
        if found_symbol:
            continue
        surrounding = schematic.get_adjecent_values(Coordinate(x, y))
        if any(isinstance(value, str) for value in surrounding):
            found_symbol = True
            result.append(value)
    return result


def load_and_solve_part_2() -> int:
    input = load_file(3)
    return solve_part_2(input)


def solve_part_2(input: list[str]) -> int:
    parsed_schematic = parse_input(input)
    gear_ratios = find_gear_ratios(parsed_schematic)
    return sum(gear_ratios)


def find_gear_ratios(schematic: Schematic) -> list[int]:
    result: list[int] = []
    for x, y, value in schematic:
        if value != GEAR_SYMBOL:
            continue
        surroundings = schematic.get_adjecent_values(Coordinate(x, y))
        numbers: list[int] = []
        numbers.extend(get_different_numbers(surroundings[:3]))
        numbers.extend(get_different_numbers([surroundings[3], None, surroundings[4]]))
        numbers.extend(get_different_numbers(surroundings[5:]))

        if len(numbers) == 2:
            result.append(numbers[0] * numbers[1])
    return result


def get_different_numbers(values: list[int]) -> list[int]:
    """
    Get the different values from a horizontal line
    For example:
    [1, None, 2] gives [1, 2]
    [111, 111, 111] gives [111]
    """
    if is_value(values[0]):
        if is_value(values[1]):
            return [values[0]]
        if is_value(values[2]):
            return [values[0], values[2]]
        return [values[0]]
    if is_value(values[1]):
        return [values[1]]
    if is_value(values[2]):
        return [values[2]]
    return []


def is_value(value) -> bool:
    return isinstance(value, int)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
