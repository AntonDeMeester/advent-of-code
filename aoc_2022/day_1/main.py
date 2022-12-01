from aoc_2022.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2022.utils.run import run_and_benchmark


def load_and_solve_part_1() -> int:
    input = load_file(1)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    calories_by_elf = parse_elves_calories(input)
    return max([sum(elf) for elf in calories_by_elf])


def parse_elves_calories(input: str) -> list[list[int]]:
    string_by_elves = split_by_double_newline(input)
    return [[int(number) for number in split_by_newline(elf)] for elf in string_by_elves]


def load_and_solve_part_2() -> int:
    input = load_file(1)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    calories_by_elf = parse_elves_calories(input)
    sorted_calories_by_elf = sorted(calories_by_elf, key=lambda x: sum(x), reverse=True)
    return sum([sum(elf) for elf in sorted_calories_by_elf[:3]])


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
