import re
from copy import deepcopy
from dataclasses import dataclass

from aoc_2022.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2022.utils.run import run_and_benchmark

CrateStack = list[str]
Configuration = list[CrateStack]


@dataclass
class Instruction:
    amount: int
    from_: int
    to_: int


def load_and_solve_part_1() -> str:
    input = load_file(5)
    return solve_part_1(input)


def solve_part_1(input: str) -> str:
    initial, instructions = parse_input(input)
    current = initial
    for i in instructions:
        current = execute_instruction_single(current, i)
    return extract_top_boxes(current)


def parse_input(input: str) -> tuple[Configuration, list[Instruction]]:
    initial, instructions = split_by_double_newline(input)
    return (parse_crates(initial), parse_instructions(instructions))


def parse_crates(input: str) -> Configuration:
    box_length = 3
    space_length = 1
    lines = split_by_newline(input)
    number_of_boxes = (len(lines[-1]) // (box_length + space_length)) + 1
    config: Configuration = [[] for _ in range(number_of_boxes)]
    for line in reversed(lines[:-1]):
        i = 0
        box_no = 0
        while i < len(line):
            if line[i : i + box_length] != " " * box_length:
                config[box_no].append(line[i + 1])
            i += box_length + space_length
            box_no += 1
    return config


def parse_instructions(input: str) -> list[Instruction]:
    lines = split_by_newline(input)
    return [parse_one_instruction(line) for line in lines]


def parse_one_instruction(line: str) -> Instruction:
    match_string = r"move (\d+) from (\d+) to (\d+)"
    matched = re.match(match_string, line)
    if matched is None:
        raise ValueError(f"Could not parse instruction {line}")
    return Instruction(int(matched[1]), int(matched[2]), int(matched[3]))


def execute_instruction_single(config: Configuration, instruction: Instruction) -> Configuration:
    new_config = deepcopy(config)
    for _ in range(instruction.amount):
        box_letter = new_config[instruction.from_ - 1].pop()
        new_config[instruction.to_ - 1].append(box_letter)
    return new_config


def execute_instruction_multiple(config: Configuration, instruction: Instruction) -> Configuration:
    new_config = deepcopy(config)
    moved_boxes = new_config[instruction.from_ - 1][-instruction.amount :]
    del new_config[instruction.from_ - 1][-instruction.amount :]
    new_config[instruction.to_ - 1].extend(moved_boxes)
    return new_config


def extract_top_boxes(config: Configuration) -> str:
    return "".join(stack[-1] for stack in config)


def load_and_solve_part_2() -> str:
    input = load_file(5)
    return solve_part_2(input)


def solve_part_2(input: str) -> str:
    initial, instructions = parse_input(input)
    current = initial
    for i in instructions:
        current = execute_instruction_multiple(current, i)
    return extract_top_boxes(current)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
