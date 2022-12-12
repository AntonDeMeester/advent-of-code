from enum import Enum

from aoc_2022.utils.parsing import load_file, split_by, split_by_newline
from aoc_2022.utils.run import run_and_benchmark


class LeftChoice(Enum):
    A = "A"
    B = "B"
    C = "C"


class RightChoice(Enum):
    X = "X"
    Y = "Y"
    Z = "Z"


class RockPaperScissors(Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


class Outcome(Enum):
    left = "left"
    draw = "draw"
    right = "right"


score_by_outcome: dict[Outcome, int] = {Outcome.right: 6, Outcome.draw: 3, Outcome.left: 0}

score_by_choice: dict[RightChoice, int] = {RightChoice.X: 1, RightChoice.Y: 2, RightChoice.Z: 3}

choice_to_rps_map: dict[LeftChoice | RightChoice, RockPaperScissors] = {
    LeftChoice.A: RockPaperScissors.rock,
    LeftChoice.B: RockPaperScissors.paper,
    LeftChoice.C: RockPaperScissors.scissors,
    RightChoice.X: RockPaperScissors.rock,
    RightChoice.Y: RockPaperScissors.paper,
    RightChoice.Z: RockPaperScissors.scissors,
}

rps_to_right_choice_map: dict[RockPaperScissors, RightChoice] = {
    RockPaperScissors.rock: RightChoice.X,
    RockPaperScissors.paper: RightChoice.Y,
    RockPaperScissors.scissors: RightChoice.Z,
}

right_choice_to_outcome_map: dict[RightChoice, Outcome] = {
    RightChoice.X: Outcome.left,
    RightChoice.Y: Outcome.draw,
    RightChoice.Z: Outcome.right,
}

Battle = tuple[LeftChoice, RightChoice]


def decide_winner(left: LeftChoice, right: RightChoice) -> Outcome:
    rps_left = choice_to_rps_map[left]
    rps_right = choice_to_rps_map[right]
    if rps_left == rps_right:
        return Outcome.draw
    if rps_left == RockPaperScissors.rock:
        if rps_right == RockPaperScissors.paper:
            return Outcome.right
        else:
            return Outcome.left
    if rps_left == RockPaperScissors.paper:
        if rps_right == RockPaperScissors.scissors:
            return Outcome.right
        else:
            return Outcome.left
    if rps_left == RockPaperScissors.scissors:
        if rps_right == RockPaperScissors.rock:
            return Outcome.right
        else:
            return Outcome.left
    raise ValueError("Did not have a proper Rock Paper Scissors")


def decide_rps(left: LeftChoice, right: RightChoice) -> RockPaperScissors:
    rps_left = choice_to_rps_map[left]
    outcome = right_choice_to_outcome_map[right]
    if outcome == Outcome.draw:
        return rps_left
    if rps_left == RockPaperScissors.rock:
        if outcome == Outcome.left:
            return RockPaperScissors.scissors
        else:
            return RockPaperScissors.paper
    if rps_left == RockPaperScissors.paper:
        if outcome == Outcome.left:
            return RockPaperScissors.rock
        else:
            return RockPaperScissors.scissors
    if rps_left == RockPaperScissors.scissors:
        if outcome == Outcome.left:
            return RockPaperScissors.paper
        else:
            return RockPaperScissors.rock
    raise ValueError("Did not have a proper Rock Paper Scissors")


def solve_battle(left: LeftChoice, right: RightChoice) -> int:
    winner = decide_winner(left, right)
    choice_score = score_by_choice[right]
    outcome_score = score_by_outcome[winner]
    return choice_score + outcome_score


def solve_strategy(left: LeftChoice, right: RightChoice) -> int:
    right_rps = decide_rps(left, right)
    choice_score = score_by_choice[rps_to_right_choice_map[right_rps]]
    outcome_score = score_by_outcome[right_choice_to_outcome_map[right]]
    return choice_score + outcome_score


def load_and_solve_part_1() -> int:
    input = load_file(2)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    battles = parse_rock_paper_scissors(input)
    return sum([solve_battle(left, right) for [left, right] in battles])


def parse_rock_paper_scissors(input: str) -> list[Battle]:
    raw_battles = split_by_newline(input)
    return [parse_battle(battle) for battle in raw_battles]


def parse_battle(line: str) -> Battle:
    [left, right] = split_by(line, " ")
    return (LeftChoice(left), RightChoice(right))


def load_and_solve_part_2() -> int:
    input = load_file(2)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    battles = parse_rock_paper_scissors(input)
    return sum([solve_strategy(left, right) for [left, right] in battles])


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
