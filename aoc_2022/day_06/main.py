from aoc_2022.utils.parsing import load_file
from aoc_2022.utils.run import run_and_benchmark


def find_marker(input: str, distinct_chars: int) -> int:
    for i in range(distinct_chars, len(input)):
        seq = input[i - distinct_chars : i]
        if len(set(seq)) == distinct_chars:
            return i
    raise ValueError(f"Could not find the marker for {input}")


def load_and_solve_part_1() -> int:
    input = load_file(6)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    return find_marker(input, 4)


def load_and_solve_part_2() -> int:
    input = load_file(6)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    return find_marker(input, 14)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
