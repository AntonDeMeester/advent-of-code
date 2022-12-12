from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark
from enum import Enum


def execute_command(command: str, current_value: int) -> list[int]:
    if command == "noop":
        return [current_value]
    if command.startswith("addx"):
        value = int(command.split()[1])
        return [current_value, current_value + value]
    raise ValueError(f"Unknown command {command}")


def parse_input(input: str) -> list[str]:
    return split_by_newline(input)


def calculate_data_during_cycles(commands: list[str]) -> list[int]:
    x = 1
    data_during_cycle = [x]
    for c in commands:
        new_values = execute_command(c, x)
        data_during_cycle.extend(new_values)
        x = new_values[-1]
    return data_during_cycle


def load_and_solve_part_1() -> int:
    input = load_file(10)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    commands = parse_input(input)
    data_during_cycle = calculate_data_during_cycles(commands)
    return sum(data_during_cycle[i - 1] * i for i in range(20, len(data_during_cycle), 40))


def load_and_solve_part_2() -> int:
    input = load_file(10)
    return solve_part_2(input)


def draw_image(data: list[int]) -> list[str]:
    result = []
    for row_index in range(0, len(data) - 1, 40):
        row_result = ""
        for i in range(40):
            total_index = row_index + i
            value = data[total_index]
            if i - 1 <= value <= i + 1:
                row_result += "#"
            else:
                row_result += "."
        result.append(row_result)
    return result


def solve_part_2(input: str) -> int:
    commands = parse_input(input)
    data_during_cycle = calculate_data_during_cycles(commands)
    image = draw_image(data_during_cycle)
    print(image)
    return "\n".join(image)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
