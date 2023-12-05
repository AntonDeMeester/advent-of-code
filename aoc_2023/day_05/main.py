from aoc_2023.utils.parsing import load_file, split_by_newline, split_by_double_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
import math


@dataclass
class AlmanacMapItem:
    destination_start: int
    source_start: int
    range: int

    def get_destination(self, source: int) -> int | None:
        if self.source_start <= source < self.source_start + self.range:
            return self.destination_start + (source - self.source_start)
        return None


@dataclass
class Almanac:
    seeds: list[int]
    seed_to_soil: list[AlmanacMapItem]
    soil_to_fertilizer: list[AlmanacMapItem]
    fertilizer_to_water: list[AlmanacMapItem]
    water_to_light: list[AlmanacMapItem]
    light_to_temperature: list[AlmanacMapItem]
    temperature_to_humidity: list[AlmanacMapItem]
    humidity_to_location: list[AlmanacMapItem]

def load_and_solve_part_1() -> int:
    input = load_file(5)
    return solve_part_1(input)


def solve_part_1(input: str):
    almanac = parse_input(input)
    locations = [find_location(almanac, seed) for seed in almanac.seeds]
    return min(locations)


def parse_input(input: str) -> Almanac:
    categories = split_by_double_newline(input)
    seeds = [int(value) for value in categories[0][len("seeds: ") :].split()]
    parsed_categories: list[list[AlmanacMapItem]] = []
    for cat in categories[1:]:
        parsed_category: list[AlmanacMapItem] = []
        lines = split_by_newline(cat)
        for line in lines[1:]:
            values = line.split()
            parsed_category.append(
                AlmanacMapItem(destination_start=int(values[0]), source_start=int(values[1]), range=int(values[2]))
            )
        parsed_categories.append(parsed_category)
    return Almanac(
        seeds=seeds,
        seed_to_soil=parsed_categories[0],
        soil_to_fertilizer=parsed_categories[1],
        fertilizer_to_water=parsed_categories[2],
        water_to_light=parsed_categories[3],
        light_to_temperature=parsed_categories[4],
        temperature_to_humidity=parsed_categories[5],
        humidity_to_location=parsed_categories[6],
    )


def find_location(almanac: Almanac, source: int) -> int:
    soil = find_mapping(almanac.seed_to_soil, source)
    fertilizer = find_mapping(almanac.soil_to_fertilizer, soil)
    water = find_mapping(almanac.fertilizer_to_water, fertilizer)
    light = find_mapping(almanac.water_to_light, water)
    temperature = find_mapping(almanac.light_to_temperature, light)
    humidity = find_mapping(almanac.temperature_to_humidity, temperature)
    location = find_mapping(almanac.humidity_to_location, humidity)
    return location


def find_mapping(almanac_map: list[AlmanacMapItem], source: int) -> int:
    for mapping in almanac_map:
        destination = mapping.get_destination(source)
        if destination is not None:
            return destination
    return source


def load_and_solve_part_2() -> int:
    input = load_file(5)
    return solve_part_2(input)


def solve_part_2(input: list[str]) -> int:
    almanac = parse_input(input)
    almanac.seeds = update_to_seed_range(almanac.seeds)
    locations = [find_location(almanac, seed) for seed in almanac.seeds]
    return min(locations)


def update_to_seed_range(seeds: list[int]) -> list[int]:
    result = []
    for i in range(0, len(seeds), 2):
        start, length = seeds[i], seeds[i + 1]
        for j in range(start, start + length):
            result.append(j)
    return result


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
