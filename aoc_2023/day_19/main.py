from aoc_2023.utils.parsing import load_file, split_by_newline, split_by_double_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass, field
import re
from typing import TypeAlias, Literal

from aoc_2023.utils.space import intersect_two_ranges, Range
from abc import ABC

Field: TypeAlias = str
InstructionName: TypeAlias = str


@dataclass
class Condition(ABC):
    field: Field
    value: int
    instruction: InstructionName
    inverted: bool = False

    def evaluate(self, value: int) -> bool:
        raise NotImplementedError()

    def combine_range(self, range: Range | None) -> Range | None:
        raise NotImplementedError()

    def copy(self) -> "Condition":
        return self.__class__(field=self.field, value=self.value, instruction=self.instruction, inverted=self.inverted)


class LesserThanCondition(Condition):
    def evaluate(self, value: int) -> bool:
        return value < self.value

    def combine_range(self, range: Range | None) -> Range | None:
        if range is None:
            return None
        if self.inverted:
            own_range = Range(self.value, END_RANGE)
        else:
            own_range = Range(START_RANGE, self.value)
        return intersect_two_ranges(own_range, range)


class GreaterThanCondition(Condition):
    def evaluate(self, value: int) -> bool:
        return value > self.value

    def combine_range(self, range: Range | None) -> Range | None:
        if range is None:
            return None
        if self.inverted:
            own_range = Range(START_RANGE, self.value + 1)
        else:
            own_range = Range(self.value + 1, END_RANGE)
        return intersect_two_ranges(own_range, range)


@dataclass
class Instruction:
    name: InstructionName
    conditions: list[Condition]
    backup: InstructionName
    previous: list[Condition] = field(default_factory=list)

    def evaluate(self, part: "Part") -> InstructionName:
        for cond in self.conditions:
            value = getattr(part, cond.field)
            if cond.evaluate(value):
                return cond.instruction
        return self.backup

    def copy(self) -> "Instruction":
        return self.__class__(name=self.name, conditions=self.conditions, backup=self.backup, previous=self.previous.copy())


Workflow = dict[InstructionName, Instruction]
ACCEPTED = "A"
REJECTED = "R"
END_STATES = (ACCEPTED, REJECTED)
START = "in"

START_RANGE = 1
END_RANGE = 4001


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


PART_PATTERN = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
INSTRUCTION_PATTERN = r"(\w+)([<>])(\d+):(\w+)"
WORFKLOW_PATTERN = r"(\w+){(.+),(\w+)}"


def load_and_solve_part_1() -> int:
    input = load_file(19)
    return solve_part_1(input)


def solve_part_1(input: str):
    workflow, parts = parse_input(input)
    accepted_parts = resolve_parts(workflow, parts)
    return calculate_result(accepted_parts)


def parse_input(input: str) -> tuple[Workflow, list[Part]]:
    raw_workflow, raw_parts = split_by_double_newline(input)
    workflow = parse_workflow(raw_workflow)
    parts = parse_parts(raw_parts)
    return workflow, parts


def parse_workflow(raw_workflow: str) -> Workflow:
    instructions = [parse_instruction(line) for line in split_by_newline(raw_workflow)]
    return {ins.name: ins for ins in instructions}


def parse_instruction(line: str) -> Instruction:
    match = re.match(WORFKLOW_PATTERN, line)
    return Instruction(name=match[1], conditions=parse_conditions(match[2]), backup=match[3])


def parse_conditions(line: str) -> list[Condition]:
    if not line:
        return []
    conditions: list[Condition] = []
    for raw in line.split(","):
        match = re.match(INSTRUCTION_PATTERN, raw)
        if match[2] == ">":
            conditions.append(GreaterThanCondition(field=match[1], value=int(match[3]), instruction=match[4]))
        else:
            conditions.append(LesserThanCondition(field=match[1], value=int(match[3]), instruction=match[4]))
    return conditions


def parse_parts(raw_parts: str) -> list[Part]:
    return [parse_single_part(line) for line in split_by_newline(raw_parts)]


def parse_single_part(line: str) -> Part:
    match = re.match(PART_PATTERN, line)
    return Part(int(match[1]), int(match[2]), int(match[3]), int(match[4]))


def resolve_parts(workflow: Workflow, parts: list[Part]) -> list[Part]:
    accepted: list[Part] = []
    for part in parts:
        resolved = resolve_part(workflow, part)
        if resolved == ACCEPTED:
            accepted.append(part)
    return accepted


def resolve_part(workflow: Workflow, part: Part) -> Literal["A", "R"]:
    current = START
    while True:
        instruction = workflow[current]
        current = instruction.evaluate(part)
        if current in END_STATES:
            return current


def calculate_result(parts: list[Part]) -> int:
    return sum(p.x + p.m + p.a + p.s for p in parts)


def load_and_solve_part_2() -> int:
    input = load_file(19)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    workflow, _ = parse_input(input)
    accepted = combine_conditions(workflow)
    possibilities = [calculate_possibilities(acc) for acc in accepted]
    return sum(possibilities)


def combine_conditions(workflow: Workflow) -> list[list[Condition]]:
    accepted: list[list[Condition]] = []
    instructions = [workflow[START]]
    while instructions:
        ins = instructions.pop()
        current_conditions: list[Condition] = ins.previous.copy()
        for new_cond in ins.conditions:
            next_name = new_cond.instruction
            if next_name == ACCEPTED:
                accepted.append(current_conditions + [new_cond])
            elif next_name == REJECTED:
                pass
            else:
                # Add to the tree
                next_ins = workflow[next_name].copy()
                next_ins.previous = current_conditions + [new_cond]
                instructions.append(next_ins)

            # Invert for the next steps
            inverted = new_cond.copy()
            inverted.inverted = True
            current_conditions.append(inverted)

        # Add default/backup case
        next_name = ins.backup
        if next_name == ACCEPTED:
            accepted.append(current_conditions)
        elif next_name == REJECTED:
            pass
        else:
            # Add to the tree
            next_ins = workflow[next_name].copy()
            next_ins.previous = current_conditions
            instructions.append(next_ins)

    return accepted


def calculate_possibilities(conditions: list[Condition]) -> int:
    ranges = {
        "x": Range(START_RANGE, END_RANGE),
        "m": Range(START_RANGE, END_RANGE),
        "a": Range(START_RANGE, END_RANGE),
        "s": Range(START_RANGE, END_RANGE),
    }
    for cond in conditions:
        current = ranges[cond.field]
        new = cond.combine_range(current)
        ranges[cond.field] = new
    total = 1
    for range in ranges.values():
        if range is None:
            return 0
        total *= range.end - range.start
    return total


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
