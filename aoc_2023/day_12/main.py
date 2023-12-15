from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
from enum import Enum
from functools import cache

FOLD_AMOUNT = 5


class SpringState(str, Enum):
    GOOD = "."
    BROKEN = "#"
    UNKNOWN = "?"


@dataclass
class SpringStateLine:
    state: tuple[SpringState]
    broken: tuple[int]

    def __post_init__(self):
        self.hash = hash_state(self.state, self.broken)

    def copy(self):
        return SpringStateLine(state=tuple(self.state), broken=tuple(self.broken))

    def __eq__(self, other: "SpringStateLine") -> bool:
        return self.broken == other.broker and self.state == other.state

    def __hash__(self) -> str:
        return self.hash


def load_and_solve_part_1() -> int:
    input = load_file(12)
    return solve_part_1(input)


def solve_part_1(input: str):
    springs = parse_input(input)
    options = [calculate_options(spring) for spring in springs]
    return sum(options)


def parse_input(input: str) -> list[SpringStateLine]:
    result: list[SpringStateLine] = []
    for line in split_by_newline(input):
        raw_state, raw_broken = line.split(" ")
        state = tuple(SpringState(v) for v in raw_state)
        broken = tuple(int(v) for v in raw_broken.split(","))
        result.append(SpringStateLine(state=state, broken=broken))
    return result


def hash_state(state: list[SpringState], broken: list[int]) -> str:
    return hash(("".join(state), ",".join(str(v) for v in broken)))


def calculate_options(spring: SpringStateLine) -> int:
    possible = is_possible(spring.state, spring.broken)
    if not possible:
        return 0
    if not any(v == SpringState.UNKNOWN for v in spring.state):
        return 1 if possible else 0

    count = 0
    for i, char in enumerate(spring.state):
        if char != SpringState.UNKNOWN:
            continue
        good = spring.copy()
        good.state = (*good.state[:i], SpringState.GOOD, *good.state[i + 1 :])
        count += calculate_options(good)

        broken = spring.copy()
        broken.state = (*broken.state[:i], SpringState.BROKEN, *broken.state[i + 1 :])
        count += calculate_options(broken)
        break
    return count


@cache
def is_possible(state: tuple[SpringState], broken_list: tuple[int]) -> bool:
    cnt = 0
    broken_index = 0
    broken = None
    for char in state:
        if char == SpringState.UNKNOWN:
            return True
        elif char == SpringState.BROKEN:
            cnt += 1
            continue
        if cnt == 0:
            continue
        try:
            broken = broken_list[broken_index]
            broken_index += 1
        except IndexError:
            return False
        if cnt != broken:
            return False
        cnt = 0
    if char == SpringState.BROKEN:
        try:
            broken = broken_list[broken_index]
            broken_index += 1
        except IndexError:
            return False
        if cnt != broken:
            return False
    if broken_index < len(broken_list):
        return False
    return True


def load_and_solve_part_2() -> int:
    input = load_file(12)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    springs = parse_input(input)
    folded_springs = [fold_spring(spring) for spring in springs]
    options = [calculate_options(spring) for spring in folded_springs]
    return sum(options)


def fold_spring(spring: SpringStateLine) -> SpringStateLine:
    return SpringStateLine(
        state=(
            *spring.state,
            SpringState.UNKNOWN,
            *spring.state,
            SpringState.UNKNOWN,
            *spring.state,
            SpringState.UNKNOWN,
            *spring.state,
            SpringState.UNKNOWN,
            *spring.state,
        ),
        broken=spring.broken * 5,
    )


# def prefix_spring(spring: SpringStateLine) -> SpringStateLine:
#     return SpringStateLine(state=[SpringState.UNKNOWN] + spring.state, broken=spring.broken)

# def postfix_spring(spring: SpringStateLine) -> SpringStateLine:
#     return SpringStateLine(state=spring.state + [SpringState.UNKNOWN], broken=spring.broken)

# def combine_options(initial: int, pre: int, post: int) -> int:
#     pre_combined = initial * math.pow(pre, 4)
#     post_combined = math.pow(post, 4) * initial
#     return pre_combined + post_combined


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
