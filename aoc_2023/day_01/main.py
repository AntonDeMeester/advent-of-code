from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark


def load_and_solve_part_1() -> int:
    input = load_file(1)
    return solve_part_1(input)


def solve_part_1(input: list[str]) -> int:
    lines = split_by_newline(input)
    results = [combine_number(line) for line in lines]
    return sum(results)


def combine_number(line: str) -> int:
    first = find_first_number(line)
    last = find_last_number(line)
    return first * 10 + last


def find_first_number(line: str) -> int:
    for char in line:
        if char.isnumeric():
            return int(char)
    raise ValueError(f"Cannot find number in line. {line}")


def find_last_number(line: str) -> int:
    for char in reversed(line):
        if char.isnumeric():
            return int(char)
    raise ValueError(f"Cannot find number in line. {line}")

def load_and_solve_part_2() -> int:
    input = load_file(1)
    return solve_part_2(input)


def solve_part_2(input: list[str]) -> int:
    lines = split_by_newline(input)
    results = [combine_complex_number(line) for line in lines]
    return sum(results)


def combine_complex_number(line: str) -> int:
    first = find_first_complex_number(line)
    last = find_last_complex_number(line)
    return first * 10 + last

NUMBER_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def find_first_complex_number(line: str) -> int:
    for i in range(len(line)):
        char = line[i]
        if char.isnumeric():
            return int(char)
        substring = line[i:]
        for word in NUMBER_MAP.keys():
            if substring.startswith(word):
                return NUMBER_MAP[word]
    raise ValueError(f"Cannot find number in line. {line}")


def find_last_complex_number(line: str) -> int:
    for i in reversed(range(len(line))):
        char = line[i]
        if char.isnumeric():
            return int(char)
        substring = line[i:]
        for word in NUMBER_MAP.keys():
            if substring.startswith(word):
                return NUMBER_MAP[word]
    raise ValueError(f"Cannot find number in line. {line}")

if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
