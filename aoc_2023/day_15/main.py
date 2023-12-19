from aoc_2023.utils.parsing import load_file
from aoc_2023.utils.run import run_and_benchmark
from typing import Literal, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Step:
    label: str
    type_: Literal["-", "="]
    focal_point: Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.label}{self.type_}{self.focal_point or ''}"


BoxConfiguration = dict[int, list[Step]]


def load_and_solve_part_1() -> int:
    input = load_file(15)
    return solve_part_1(input)


def solve_part_1(input: str):
    steps = parse_input(input)
    values = [fancy_hash(step) for step in steps]
    return sum(values)


def parse_input(value: str) -> list[str]:
    return value.split(",")


def fancy_hash(value: str) -> int:
    hash_value = 0
    for char in value:
        hash_value += ord(char)
        hash_value = (hash_value * 17) % 256
    return hash_value


def load_and_solve_part_2() -> int:
    input = load_file(15)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    steps = parse_input_steps(input)
    result_boxes = execute_steps(steps)
    return calculcate_focal_power(result_boxes)


def parse_input_steps(value: str) -> list[Step]:
    raw_steps = parse_input(value)
    parsed_steps: list[Step] = []
    for raw in raw_steps:
        if "=" in raw:
            parsed_steps.append(Step(label=raw[:-2], type_="=", focal_point=int(raw[-1])))
        else:
            parsed_steps.append(Step(label=raw[:-1], type_="-", focal_point=None))
    return parsed_steps


def execute_steps(steps: list[Step]) -> BoxConfiguration:
    boxes = defaultdict(list)
    for step in steps:
        hash = fancy_hash(step.label)
        contents = boxes[hash]
        loc = find_lens(step.label, contents)
        if step.type_ == "=":
            if loc != -1:
                contents[loc] = step
            else:
                contents.append(step)
        else:
            if loc != -1:
                del contents[loc]
    return dict(boxes)


def find_lens(label: str, contents: list[Step]) -> int:
    for i, c in enumerate(contents):
        if c.label == label:
            return i
    return -1


def calculcate_focal_power(boxes: BoxConfiguration) -> int:
    value = 0
    for box_number, contents in boxes.items():
        for i, step in enumerate(contents):
            if step.focal_point is None:
                raise ValueError()
            value += (box_number + 1) * (i + 1) * (step.focal_point)
    return value


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
