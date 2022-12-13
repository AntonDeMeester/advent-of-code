import json
from enum import Enum
from itertools import zip_longest
from typing import cast

from aoc_2022.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2022.utils.run import run_and_benchmark

Signal = int | list["Signal"]
Pair = tuple[Signal, Signal]


class Outcome(Enum):
    left = "left"
    right = "right"
    same = "same"


def parse_pair(pair: str) -> Pair:
    first, second = split_by_newline(pair)
    return cast(Pair, (json.loads(first), json.loads(second)))


def parse_input_to_pairs(input: str) -> list[Pair]:
    pairs = split_by_double_newline(input)
    return [parse_pair(item) for item in pairs]


def compare_pair(pair: Pair) -> Outcome:
    return compare_signal(pair[0], pair[1])


def compare_signal_int(left: int, right: int) -> Outcome:
    if left < right:
        return Outcome.left
    if right < left:
        return Outcome.right
    return Outcome.same


def compare_signal_list(left: list[Signal], right: list[Signal]) -> Outcome:
    for left_item, right_item in zip_longest(left, right, fillvalue=None):
        if left_item is None:
            return Outcome.left
        if right_item is None:
            return Outcome.right
        comparison = compare_signal(left_item, right_item)
        if comparison != Outcome.same:
            return comparison
    return Outcome.same


def compare_signal(left: Signal, right: Signal) -> Outcome:
    left_is_int = isinstance(left, int)
    right_is_int = isinstance(right, int)
    if left_is_int and right_is_int:
        return compare_signal_int(cast(int, left), cast(int, right))

    mod_left = [left] if left_is_int else left
    mod_right = [right] if right_is_int else right
    return compare_signal_list(cast(list[Signal], mod_left), cast(list[Signal], mod_right))


class SignalContainer:
    def __init__(self, data: Signal):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SignalContainer):
            return NotImplemented
        comparison = compare_signal(self.data, other.data)
        return comparison == Outcome.right

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SignalContainer):
            return NotImplemented
        comparison = compare_signal(self.data, other.data)
        return comparison == Outcome.left

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SignalContainer):
            return NotImplemented
        comparison = compare_signal(self.data, other.data)
        return comparison == Outcome.same


def parse_all_inputs(input: str) -> list[SignalContainer]:
    all_signals: list[SignalContainer] = [SignalContainer([[2]]), SignalContainer([[6]])]
    for line in split_by_newline(input):
        if not line:
            continue
        all_signals.append(SignalContainer(cast(Signal, json.loads(line))))
    return all_signals


def score_part_2(signals: list[SignalContainer]) -> int:
    product = 1
    for i, item in enumerate(signals):
        if item.data == [[2]]:
            product *= i + 1
        if item.data == [[6]]:
            product *= i + 1
    return product


def load_and_solve_part_1() -> int:
    input = load_file(13)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    pairs = parse_input_to_pairs(input)
    comparison = [compare_pair(pair) for pair in pairs]
    return sum(i + 1 for i, value in enumerate(comparison) if value == Outcome.left)


def load_and_solve_part_2() -> int:
    input = load_file(13)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    all_signals = parse_all_inputs(input)
    sorted_signals = sorted(all_signals)
    return score_part_2(sorted_signals)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
