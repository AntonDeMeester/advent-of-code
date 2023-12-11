from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from aoc_2023.utils.matrix import BoundedMatrix
from aoc_2023.utils.space import Coordinate, get_manhattan_distance
from typing import Literal

GalaxyMap = BoundedMatrix[Literal[".", "#"]]
EXPANSION_SPEED = 1_000_000 - 1


def load_and_solve_part_1() -> int:
    input = load_file(11)
    return solve_part_1(input)


def solve_part_1(input: str):
    galaxy_map = parse_input(input)
    future_galaxy = expand_universe(galaxy_map)
    closest_distances = calculate_closest_galaxies(future_galaxy)
    return sum(closest_distances)


def parse_input(input: str) -> GalaxyMap:
    lines = split_by_newline(input)
    return GalaxyMap([list(line) for line in lines])


def expand_universe(galaxy: GalaxyMap) -> GalaxyMap:
    new_galaxy = galaxy.copy()
    extra_i = 0
    for i in range(galaxy.vertical_length()):
        row = galaxy.get_row(i)
        if all(v == "." for v in row):
            new_galaxy.data = (
                new_galaxy.data[: i + extra_i]
                + [["." for _ in range(galaxy.horizontal_length())]]
                + new_galaxy.data[i + extra_i :]
            )
            extra_i += 1

    extra_i = 0
    for i in range(galaxy.horizontal_length()):
        col = galaxy.get_column(i)
        if all(v == "." for v in col):
            new_galaxy.data = [line[: i + extra_i] + ["."] + line[i + extra_i :] for line in new_galaxy.data]
            extra_i += 1
    return new_galaxy


def calculate_closest_galaxies(galaxy: GalaxyMap) -> list[int]:
    galaxies = [Coordinate(x, y) for x, y, value in galaxy if value == "#"]
    distances: list[int] = []
    for i, gal in enumerate(galaxies):
        for oth in galaxies[i:]:
            distances.append(get_manhattan_distance(gal, oth))
    return distances


def load_and_solve_part_2() -> int:
    input = load_file(11)
    return solve_part_2(input, EXPANSION_SPEED)


def solve_part_2(input: str, expansion_speed: int) -> int:
    galaxy_map = parse_input(input)
    closest_distances = calculate_closest_galaxies_with_speed(galaxy_map, expansion_speed)
    return sum(closest_distances)


def calculate_closest_galaxies_with_speed(galaxy: GalaxyMap, speed: int) -> list[int]:
    galaxies = [Coordinate(x, y) for x, y, value in galaxy if value == "#"]
    empty_rows = [i for i in range(galaxy.vertical_length()) if all(v == "." for v in galaxy.get_row(i))]
    empty_cols = [i for i in range(galaxy.horizontal_length()) if all(v == "." for v in galaxy.get_column(i))]
    distances: list[int] = []
    for i, gal in enumerate(galaxies):
        for oth in galaxies[i:]:
            dist = get_manhattan_distance(gal, oth)
            for row_index in empty_rows:
                if (gal.y < row_index < oth.y) or (gal.y > row_index > oth.y):
                    dist += speed
            for col_index in empty_cols:
                if (gal.x < col_index < oth.x) or (gal.x > col_index > oth.x):
                    dist += speed
            distances.append(dist)
    return distances


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
