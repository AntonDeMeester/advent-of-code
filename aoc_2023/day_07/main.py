from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
from enum import Enum
from collections import Counter


class Card(str, Enum):
    A = "A"
    K = "K"
    Q = "Q"
    J = "J"
    T = "T"
    Nine = "9"
    Eight = "8"
    Seven = "7"
    Six = "6"
    Five = "5"
    Four = "4"
    Three = "3"
    Two = "2"

    def __gt__(self, other: "Card") -> bool:
        return CARD_STRENGTH[self] > CARD_STRENGTH[other]


CARD_STRENGTH = {
    Card.A: 14,
    Card.K: 13,
    Card.Q: 12,
    Card.J: 11,
    Card.T: 10,
    Card.Nine: 9,
    Card.Eight: 8,
    Card.Seven: 7,
    Card.Six: 6,
    Card.Five: 5,
    Card.Four: 4,
    Card.Three: 3,
    Card.Two: 2,
}


class HandType(str, Enum):
    FIVE_OF_A_KIND = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    THREE_OF_A_KIND = 6
    TWO_PAIR = 5
    ONE_PAIR = 4
    HIGH_CARD = 3


@dataclass
class Hand:
    cards: list[Card]

    def __post_init__(self):
        self.type_ = define_hand_type(self.cards)

    def __eq__(self, other: "Card") -> bool:
        return self.cards == other.cards

    def __gt__(self, other: "Card") -> bool:
        if self.type_.value > other.type_.value:
            return True
        if self.type_.value < other.type_.value:
            return False
        # Same types
        for own, oth in zip(self.cards, other.cards):
            if own != oth:
                return own > oth
        return False


def define_hand_type(cards: list[Card]) -> HandType:
    counter = Counter(cards)
    common_cards = counter.most_common(2)
    most_count = common_cards[0][1]
    if most_count == 5:
        return HandType.FIVE_OF_A_KIND
    if most_count == 4:
        return HandType.FOUR_OF_A_KIND
    second_most = common_cards[1][1]
    if most_count == 3:
        if second_most == 2:
            return HandType.FULL_HOUSE
        else:
            return HandType.THREE_OF_A_KIND
    if most_count == 2:
        if second_most == 2:
            return HandType.TWO_PAIR
        else:
            return HandType.ONE_PAIR
    return HandType.HIGH_CARD


@dataclass
class Bid:
    hand: Hand
    amount: int


def load_and_solve_part_1() -> int:
    input = load_file(7)
    return solve_part_1(input)


def solve_part_1(input: str):
    bids = parse_input(input)
    winnings = calculate_winnings(bids)
    return sum(winnings)


def parse_input(input: str) -> list[Bid]:
    lines = split_by_newline(input)
    return [parse_line(line) for line in lines]


def parse_line(line: str) -> Bid:
    cards, amount = line.split()
    return Bid(hand=Hand([Card(c) for c in cards]), amount=int(amount))


def calculate_winnings(bids: list[Bid]) -> list[int]:
    """Returns the winnings, sorted by losers to winners"""
    sorted_bids = sorted(bids, key=lambda x: x.hand)
    return [bid.amount * (i + 1) for i, bid in enumerate(sorted_bids)]


class CardWithJoker(str, Enum):
    # Cannot extend enum so copy paste
    A = "A"
    K = "K"
    Q = "Q"
    J = "J"
    T = "T"
    Nine = "9"
    Eight = "8"
    Seven = "7"
    Six = "6"
    Five = "5"
    Four = "4"
    Three = "3"
    Two = "2"

    def __gt__(self, other: "Card") -> bool:
        return CARD_STRENGTH_WITH_JOKER[self] > CARD_STRENGTH_WITH_JOKER[other]


CARD_STRENGTH_WITH_JOKER = {**CARD_STRENGTH, CardWithJoker.J: 1}


class HandWithJoker(Hand):
    def __post_init__(self):
        self.type_ = define_hand_type_with_joker(self.cards)


def load_and_solve_part_2() -> int:
    input = load_file(7)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    bids = parse_input_with_joker(input)
    winnings = calculate_winnings(bids)
    return sum(winnings)


def parse_input_with_joker(input: str) -> list[Bid]:
    lines = split_by_newline(input)
    return [parse_line_with_joker(line) for line in lines]


def parse_line_with_joker(line: str) -> Bid:
    cards, amount = line.split()
    return Bid(hand=HandWithJoker([CardWithJoker(c) for c in cards]), amount=int(amount))


def define_hand_type_with_joker(cards: list[CardWithJoker]) -> HandType:
    jokers = sum(1 for c in cards if c == CardWithJoker.J)
    if jokers == 5:
        return HandType.FIVE_OF_A_KIND
    counter = Counter(c for c in cards if c != CardWithJoker.J)
    common_cards = counter.most_common(2)
    most_count = common_cards[0][1] + jokers
    if most_count == 5:
        return HandType.FIVE_OF_A_KIND
    if most_count == 4:
        return HandType.FOUR_OF_A_KIND
    second_most = common_cards[1][1]
    if most_count == 3:
        if second_most == 2:
            return HandType.FULL_HOUSE
        else:
            return HandType.THREE_OF_A_KIND
    if most_count == 2:
        if second_most == 2:
            return HandType.TWO_PAIR
        else:
            return HandType.ONE_PAIR
    return HandType.HIGH_CARD


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
