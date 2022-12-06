from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark

Rucksack = str
RucksackDuo = tuple[Rucksack, Rucksack]


def parse_input(input: str) -> list[RucksackDuo]:
    rucksacks = split_by_newline(input)
    return [split_rucksacks_in_two(line) for line in rucksacks]


def split_rucksacks_in_two(line: str) -> RucksackDuo:
    length = len(line) // 2
    return line[:length], line[length:]


def find_common_item_type(duo: RucksackDuo) -> str:
    common = set(duo[0]) & set(duo[1])
    if len(common) > 1:
        raise ValueError("More than one item type in common")
    if not common:
        raise ValueError("No common item type found")
    return common.pop()


def score_item_type(char: str) -> int:
    ascii_value = ord(char)
    # ord('a') = 97
    if ascii_value > ord("a"):
        return ascii_value - ord("a") + 1
    # ord('A') = 65
    return ascii_value - ord("A") + 1 + 26


def score_mismatch(duo: RucksackDuo) -> int:
    common = find_common_item_type(duo)
    return score_item_type(common)


def load_and_solve_part_1() -> int:
    input = load_file(3)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    rucksack_duos = parse_input(input)
    return sum(score_mismatch(duo) for duo in rucksack_duos)


def load_and_solve_part_2() -> int:
    input = load_file(3)
    return solve_part_2(input)


def find_common_badge(*rucksacks: Rucksack) -> str:
    common = set(rucksacks[0])
    for subset in rucksacks[1:]:
        common &= set(subset)
    if len(common) > 1:
        raise ValueError("More than one item type in common")
    if not common:
        raise ValueError("No common item type found")
    return common.pop()


def find_and_score_common_badge(elf_group: list[Rucksack]) -> int:
    common_letter = find_common_badge(*elf_group)
    return score_item_type(common_letter)


def solve_part_2(input: str) -> int:
    rucksacks: list[Rucksack] = split_by_newline(input)
    elf_groups = [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]
    return sum(find_and_score_common_badge(group) for group in elf_groups)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
