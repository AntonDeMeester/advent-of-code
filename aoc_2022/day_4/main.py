from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains(self, other: "Range") -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlap(self, other: "Range") -> bool:
        common = set(range(other.start, other.end + 1)) & set(range(self.start, self.end + 1))
        return bool(common)


def load_and_solve_part_1() -> int:
    input = load_file(4)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    elf_pairs = parse_input(input)
    return sum(one.contains(two) or two.contains(one) for one, two in elf_pairs)


def parse_input(input: str) -> list[tuple[Range, Range]]:
    list_of_duos = split_by_newline(input)
    return [parse_duo(line) for line in list_of_duos]


def parse_duo(line: str) -> tuple[Range, Range]:
    one, two = line.split(",")
    return (Range(int(one.split("-")[0]), int(one.split("-")[1])), Range(int(two.split("-")[0]), int(two.split("-")[1])))


def load_and_solve_part_2() -> int:
    input = load_file(4)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    elf_pairs = parse_input(input)
    return sum(one.overlap(two) for one, two in elf_pairs)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
