from functools import reduce
from typing import Literal, Protocol

from aoc_2022.utils.parsing import load_file, split_by, split_by_double_newline, split_by_newline
from aoc_2022.utils.run import run_and_benchmark

Item = int


class Operation(Protocol):
    def perform_operation(self, item: Item) -> Item:
        ...


class PlusOperation:
    def __init__(self, right: str):
        self.right: Literal["old"] | Item = "old" if right == "old" else Item(right)

    def perform_operation(self, item: Item) -> Item:
        if self.right == "old":
            return item + item
        else:
            return item + self.right


class MultipleOperation:
    def __init__(self, right: str):
        self.right: Literal["old"] | Item = "old" if right == "old" else Item(right)

    def perform_operation(self, item: Item) -> Item:
        if self.right == "old":
            return item * item
        else:
            return item * self.right


class Test:
    def __init__(self, modulo: int):
        self.modulo = modulo

    def perform_test(self, value: Item) -> bool:
        return (value % self.modulo) == 0


class Monkey:
    def __init__(self, starting_items: list[Item], test: Test, operation: Operation, true_target: int, false_target: int):
        self.items = starting_items
        self.test = test
        self.operation = operation
        self.true_target = true_target
        self.false_target = false_target
        self.inspect_count = 0
        self.common_worry: int | None = None

    def add_item(self, item: Item):
        self.items.append(item)

    def resolve_round(self, monkey_list: list["Monkey"]):
        old_items = self.items
        self.items = []
        for item in old_items:
            self.resolve_item(item, monkey_list)

    def resolve_item(self, item: Item, monkey_list: list["Monkey"]):
        self.inspect_count += 1
        new_worry = self.operation.perform_operation(item) // 3
        if self.test.perform_test(new_worry):
            monkey_list[self.true_target].add_item(new_worry)
        else:
            monkey_list[self.false_target].add_item(new_worry)

    def set_common_worry(self, value: int):
        self.common_worry = value

    def resolve_round_high_worry(self, monkey_list: list["Monkey"]):
        old_items = self.items
        self.items = []
        for item in old_items:
            self.resolve_item_high_worry(item, monkey_list)

    def resolve_item_high_worry(self, item: Item, monkey_list: list["Monkey"]):
        self.inspect_count += 1
        new_worry = self.operation.perform_operation(item)
        if self.common_worry is None:
            raise ValueError("Common worry is not set")
        new_worry %= self.common_worry
        if self.test.perform_test(new_worry):
            monkey_list[self.true_target].add_item(new_worry)
        else:
            monkey_list[self.false_target].add_item(new_worry)


def parse_starting_items(line: str) -> list[Item]:
    return [Item(item) for item in line.replace("Starting items: ", "").split(", ")]


def parse_operation(line: str) -> Operation:
    core = split_by(line, " ")[-2:]
    if core[0] == "*":
        return MultipleOperation(core[1])
    if core[0] == "+":
        return PlusOperation(core[1])
    raise ValueError(f"Cannot parse operation {line}")


def parse_test(line: str) -> Test:
    return Test(int(split_by(line, " ")[-1]))


def parse_target(line: str) -> int:
    return int(split_by(line, " ")[-1])


def parse_monkey(input: str) -> Monkey:
    lines = split_by_newline(input)
    items = parse_starting_items(lines[1])
    operation = parse_operation(lines[2])
    test = parse_test(lines[3])
    true_op = parse_target(lines[4])
    false_op = parse_target(lines[5])
    return Monkey(items, test, operation, true_op, false_op)


def resolve_rounds(monkey_list: list[Monkey], rounds: int) -> list[Monkey]:
    for _ in range(rounds):
        for monkey in monkey_list:
            monkey.resolve_round(monkey_list)
    return monkey_list


def resolve_rounds_high_worry(monkey_list: list[Monkey], rounds: int) -> list[Monkey]:
    common_worry = reduce(lambda worry, monkey: worry * monkey.test.modulo, monkey_list, 1)
    for monkey in monkey_list:
        monkey.set_common_worry(common_worry)
    for _ in range(rounds):
        for monkey in monkey_list:
            monkey.resolve_round_high_worry(monkey_list)
    return monkey_list


def score_worry(monkey_list: list[Monkey]) -> int:
    sorted_monkeys = sorted(monkey_list, key=lambda x: x.inspect_count, reverse=True)
    return sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count


def load_and_solve_part_1() -> int:
    input = load_file(11)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    monkey_list = [parse_monkey(raw) for raw in split_by_double_newline(input)]
    monkey_list = resolve_rounds(monkey_list, 20)
    return score_worry(monkey_list)


def load_and_solve_part_2() -> int:
    input = load_file(11)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    monkey_list = [parse_monkey(raw) for raw in split_by_double_newline(input)]
    monkey_list = resolve_rounds_high_worry(monkey_list, 10000)
    return score_worry(monkey_list)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
