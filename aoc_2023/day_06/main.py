from aoc_2023.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
from math import prod, ceil

@dataclass
class BoatRace:
    time: int
    previous_record: int

def load_and_solve_part_1() -> int:
    input = load_file(6)
    return solve_part_1(input)


def solve_part_1(input: str):
    races = parse_input(input)
    ways_to_win = [define_number_of_ways_to_win(race) for race in races]
    return int(prod(ways_to_win))

def parse_input(input: str) -> list[BoatRace]:
    lines = split_by_newline(input)
    times = lines[0][len("Time: "):].split()
    records = lines[1][len("Distance: "):].split()
    return [BoatRace(time=int(t), previous_record=int(r)) for t, r in zip(times, records)]

def define_number_of_ways_to_win(race: BoatRace) -> int:
    mid_way = race.time / 2
    for i in range(1, ceil(mid_way) + 1):
        if i * (race.time - i) > race.previous_record:
            return (mid_way - i) * 2 + 1
    return 0


def load_and_solve_part_2() -> int:
    input = load_file(6)
    return solve_part_2(input)

def solve_part_2(input: str) -> int:
    race = parse_input_part_2(input)
    return int(define_number_of_ways_to_win(race))

def parse_input_part_2(input: str) -> BoatRace:
    lines = split_by_newline(input)
    time = int(lines[0][len("Time: "):].replace(" ", ""))
    record = int(lines[1][len("Distance: "):].replace(" ", ""))
    return BoatRace(time=time, previous_record=record)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
