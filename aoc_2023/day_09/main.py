from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark


def load_and_solve_part_1() -> int:
    input = load_file(9)
    return solve_part_1(input)


def solve_part_1(input: str):
    sequences = parse_input(input)
    solutions = [predict_next_sequence(seq) for seq in sequences]
    return sum(solutions)


def parse_input(input: str) -> list[list[int]]:
    lines = split_by_newline(input)
    return [[int(value) for value in line.split()] for line in lines]


def predict_next_sequence(sequence: list[int]) -> int:
    differences: list[list[sequence]] = [sequence]
    while not all(value == 0 for value in differences[-1]):
        current = differences[-1]
        new_list = [current[i + 1] - current[i] for i in range(len(current) - 1)]
        differences.append(new_list)

    last = 0
    for seq in reversed(differences):
        last = seq[-1] + last
    return last


def load_and_solve_part_2() -> int:
    input = load_file(9)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    sequences = parse_input(input)
    solutions = [predict_previous_sequence(seq) for seq in sequences]
    return sum(solutions)


def predict_previous_sequence(sequence: list[int]) -> int:
    differences: list[list[sequence]] = [sequence]
    while not all(value == 0 for value in differences[-1]):
        current = differences[-1]
        new_list = [current[i + 1] - current[i] for i in range(len(current) - 1)]
        differences.append(new_list)

    prev = 0
    for seq in reversed(differences):
        prev = seq[0] - prev
    return prev


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
