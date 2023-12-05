from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass


@dataclass(order=True)
class GameState:
    red: int
    blue: int
    green: int


def load_and_solve_part_1() -> int:
    input = load_file(2)
    target = GameState(12, 14, 13)
    return solve_part_1(input, target)


def solve_part_1(input: list[str], target: GameState) -> int:
    game_dict = parse_input(input)
    good_game_numbers = find_possible_games(game_dict, target)
    return sum(good_game_numbers)


def parse_input(lines: list[str]) -> dict[int, list[GameState]]:
    games = split_by_newline(lines)
    parsed_states: dict[int, list[GameState]] = {}
    for line in games:
        game: list[GameState] = []
        game_number, state_line = line.split(": ")
        states = state_line.split("; ")
        for state_str in states:
            parsed_state = GameState(0, 0, 0)
            items = state_str.split(", ")
            for item in items:
                number, colour = item.split(" ")
                setattr(parsed_state, colour, int(number))
            game.append(parsed_state)
        parsed_states[int(game_number[5:])] = game
    return parsed_states


def find_possible_games(game_dict: dict[int, list[GameState]], target: GameState) -> list[int]:
    possible: list[int] = []
    for game_number, game_list in game_dict.items():
        for game in game_list:
            if game.red > target.red or game.blue > target.blue or game.green > target.green:
                break
        else:
            possible.append(game_number)
    return possible


def load_and_solve_part_2() -> int:
    input = load_file(2)
    return solve_part_2(input)


def solve_part_2(input: list[str]) -> int:
    game_dict = parse_input(input)
    results = calculate_all_game_power(game_dict)
    return sum(results)


def calculate_all_game_power(game_dict: dict[int, list[GameState]]) -> list[int]:
    return [calculate_game_power(game_list) for game_list in game_dict.values()]


def calculate_game_power(game_list: list[GameState]) -> int:
    min_state = GameState(0, 0, 0)
    for game in game_list:
        if game.red > min_state.red:
            min_state.red = game.red
        if game.green > min_state.green:
            min_state.green = game.green
        if game.blue > min_state.blue:
            min_state.blue = game.blue
    return min_state.red * min_state.green * min_state.blue


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
