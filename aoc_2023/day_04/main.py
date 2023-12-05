from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
import math


@dataclass
class Card:
    number: int
    winning: list[int]
    selected: list[int]


PATTERN = r"Card (\d+):(\s*(\d+))+ | (\s*(\d+))+"


def load_and_solve_part_1() -> int:
    input = load_file(4)
    return solve_part_1(input)


def solve_part_1(input: str):
    cards = parse_input(input)
    points = [calculate_points(card) for card in cards]
    return sum(points)


def parse_input(input: str) -> list[Card]:
    result: list[Card] = []
    lines = split_by_newline(input)
    for line in lines:
        card, numbers = line.split(": ")
        winning, selected = numbers.split(" | ")
        result.append(
            Card(
                number=int(card[5:]),
                winning=[int(value) for value in winning.split(" ") if value],
                selected=[int(value) for value in selected.split(" ") if value],
            )
        )
    return result


def calculate_points(card: Card) -> int:
    correct = calculate_winning_amount(card)
    if correct == 0:
        return 0
    return int(math.pow(2, correct - 1))


def calculate_winning_amount(card: Card) -> int:
    correct = 0
    for sel in card.selected:
        if sel in card.winning:
            correct += 1
    return correct


def load_and_solve_part_2() -> int:
    input = load_file(4)
    return solve_part_2(input)


def solve_part_2(input: list[str]) -> int:
    cards = parse_input(input)
    final_cards = calculate_final_cards(cards)
    return sum(final_cards)


def calculate_final_cards(cards: list[Card]) -> int:
    card_amounts = [1 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        current_amount = card_amounts[i]
        points = calculate_winning_amount(card)
        for j in range(i + 1, i + points + 1):
            if j >= len(cards):
                continue
            card_amounts[j] += current_amount
    return card_amounts


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
