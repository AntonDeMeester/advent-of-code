from typing import Iterable

from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark
from aoc_2022.utils.space import Coordinate, Direction, move_from_coordinate

Command = tuple[Direction, int]


class History:
    def __init__(self, *knot_history_list: list[Coordinate]):
        self.knot_history_list = knot_history_list
        self.knot_length = len(knot_history_list)

    def current_state(self) -> "State":
        return State([hist[-1] for hist in self.knot_history_list])

    def unique_head_locations(self) -> set[Coordinate]:
        return set(self.knot_history_list[0])

    def unique_tail_locations(self) -> set[Coordinate]:
        return set(self.knot_history_list[-1])

    def unique_locations_for(self, index: int) -> set[Coordinate]:
        return set(self.knot_history_list[index])

    def add_to_history(self, state: "State") -> "History":
        return History(*[[*self.knot_history_list[i], state[i]] for i in range(len(state))])


class State(list[Coordinate]):
    def __init__(self, *args: Iterable[Coordinate] | Coordinate):  # type: ignore
        if isinstance(args[0], Iterable) and len(args) == 1:
            super().__init__(args[0])
        else:
            super().__init__(args)  # type: ignore

    @property
    def head(self):
        return self[0]

    @property
    def tail(self):
        return self[1]


def move_tail_to_head(head: Coordinate, old_tail: Coordinate) -> Coordinate:
    diff_x = head.x - old_tail.x
    diff_y = head.y - old_tail.y
    # At least one is more than 1 off and the other one is at least 1 off
    move_diag = (abs(diff_x) >= 1 and abs(diff_y) >= 1) and (abs(diff_x) > 1 or abs(diff_y) > 1)

    if diff_x > 1:
        extra_x = 1
    elif diff_x < -1:
        extra_x = -1
    elif move_diag:
        extra_x = diff_x
    else:
        extra_x = 0

    if diff_y > 1:
        extra_y = 1
    elif diff_y < -1:
        extra_y = -1
    elif move_diag:
        extra_y = diff_y
    else:
        extra_y = 0

    return Coordinate(old_tail.x + extra_x, old_tail.y + extra_y)


def execute_step(history: History, direction: Direction) -> History:
    state = history.current_state()
    new_state_coordinates: list[Coordinate] = []
    new_head = move_from_coordinate(state.head, direction)
    new_state_coordinates.append(new_head)
    for i in range(1, history.knot_length):
        new_head = move_tail_to_head(new_head, state[i])
        new_state_coordinates.append(new_head)

    return history.add_to_history(State(new_state_coordinates))


def execute_command(history: History, command: Command) -> History:
    for _ in range(command[1]):
        history = execute_step(history, command[0])
    return history


def parse_command(line: str) -> Command:
    direction, count = line.split(" ")
    return (Direction(direction), int(count))


def parse_input(input: str) -> list[Command]:
    lines = split_by_newline(input)
    return [parse_command(line) for line in lines]


def load_and_solve_part_1() -> int:
    input = load_file(9)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    commands = parse_input(input)
    history = History([Coordinate(0, 0)], [Coordinate(0, 0)])
    for c in commands:
        history = execute_command(history, c)
    return len(history.unique_tail_locations())


def load_and_solve_part_2() -> int:
    input = load_file(9)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    commands = parse_input(input)
    history = History(*[[Coordinate(0, 0)] for _ in range(10)])
    for c in commands:
        history = execute_command(history, c)
    return len(history.unique_tail_locations())


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
