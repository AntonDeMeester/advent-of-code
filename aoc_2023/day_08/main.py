from dataclasses import dataclass

from aoc_2023.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from typing import Literal
import re
from itertools import cycle
from math import lcm

LOCATION_REGEX = r"(...) = \((...), (...)\)"


@dataclass
class Node:
    name: str
    left: str
    right: str


NodeMap = dict[str, Node]


@dataclass
class TotalMap:
    instructrions: list[Literal["R", "L"]]
    node_map: NodeMap


@dataclass
class Cycle:
    offset: int
    cycle: int


START = "AAA"
END = "ZZZ"


def load_and_solve_part_1() -> int:
    input = load_file(8)
    return solve_part_1(input)


def solve_part_1(input: str):
    total_map = parse_input(input)
    return iterate_until_end(total_map)


def parse_input(input: str) -> TotalMap:
    instructions, raw_nodes = split_by_double_newline(input)
    nodes: list[Node] = []
    for node in split_by_newline(raw_nodes):
        match = re.match(LOCATION_REGEX, node)
        nodes.append(Node(name=match[1], left=match[2], right=match[3]))
    return TotalMap(instructrions=list(instructions), node_map={node.name: node for node in nodes})


def iterate_until_end(total_map: TotalMap) -> int:
    count = 0
    current_name = START
    for direction in cycle(total_map.instructrions):
        current_name = iterate_step(current_name, direction, total_map)
        count += 1
        if current_name == END:
            return count


def load_and_solve_part_2() -> int:
    input = load_file(8)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    total_map = parse_input(input)
    return find_lcm_solution(total_map)
    # return iterate_simultaneously(total_map)


def iterate_simultaneously(total_map: TotalMap) -> int:
    node_names = get_start_node_names(total_map)
    count = 0
    for direction in cycle(total_map.instructrions):
        node_names = [iterate_step(name, direction, total_map) for name in node_names]
        count += 1
        if has_ended(node_names):
            return count


def get_start_node_names(total_map: TotalMap) -> list[str]:
    return [node for node in total_map.node_map.keys() if node.endswith("A")]


def iterate_step(name: str, direction: Literal["L", "R"], total_map: TotalMap) -> str:
    node = total_map.node_map[name]
    if direction == "L":
        return node.left
    else:
        return node.right


def has_ended(node_names: list[str]) -> bool:
    return all(name.endswith("Z") for name in node_names)


"""It look forever so I checked on Reddit and apparently this is the wrong way"""


def find_lcm_solution(total_map: TotalMap) -> int:
    node_names = get_start_node_names(total_map)
    cycle_sizes = [find_cycle_size(name, total_map) for name in node_names]
    return find_first_common_point(cycle_sizes)


def find_cycle_size(start: str, total_map: TotalMap) -> Cycle:
    current = start
    offset = 0
    count = 0
    for direction in cycle(total_map.instructrions):
        current = iterate_step(current, direction, total_map)
        count += 1
        if current.endswith("Z"):
            if offset == 0:
                offset = count
            else:
                return Cycle(offset=offset, cycle=count - offset)


def find_first_common_point(cycles: list[Cycle]) -> int:
    """From observation, offset == cycle, so we can just to Least Common Multiple"""
    return lcm(*[cycle.cycle for cycle in cycles])


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
