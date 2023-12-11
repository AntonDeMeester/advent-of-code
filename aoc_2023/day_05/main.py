import sys
from dataclasses import dataclass

from aoc_2023.utils.parsing import load_file, split_by_double_newline, split_by_newline
from aoc_2023.utils.run import run_and_benchmark


@dataclass
class AlmanacMapItem:
    destination_start: int
    source_start: int
    range: int

    def __post_init__(self):
        self.destination_end = self.destination_start + self.range
        self.source_end = self.source_start + self.range

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


SOURCE_START_LAMBDA = lambda x: x.source_start


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
        seed_to_soil=sorted(parsed_categories[0], key=SOURCE_START_LAMBDA),
        soil_to_fertilizer=sorted(parsed_categories[1], key=SOURCE_START_LAMBDA),
        fertilizer_to_water=sorted(parsed_categories[2], key=SOURCE_START_LAMBDA),
        water_to_light=sorted(parsed_categories[3], key=SOURCE_START_LAMBDA),
        light_to_temperature=sorted(parsed_categories[4], key=SOURCE_START_LAMBDA),
        temperature_to_humidity=sorted(parsed_categories[5], key=SOURCE_START_LAMBDA),
        humidity_to_location=sorted(parsed_categories[6], key=SOURCE_START_LAMBDA),
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


def solve_part_2(input: str) -> int:
    return solve_part_2_efficiently(input)
    # almanac = parse_input(input)

    # with Pool(10) as p:
    #     results = p.starmap(
    #         solve_part_2_seed, [(almanac.seeds[i], almanac.seeds[i + 1], almanac) for i in range(0, len(almanac.seeds), 2)]
    #     )
    # return min(results)


def solve_part_2_seed(start: int, length: int, almanac: Almanac) -> int:
    minimum_location = sys.maxsize
    for j in range(start, start + length):
        location = find_location(almanac, j)
        minimum_location = min(location, minimum_location)

    return minimum_location


def update_to_seed_range(seeds: list[int]) -> list[int]:
    result = []
    for i in range(0, len(seeds), 2):
        start, length = seeds[i], seeds[i + 1]
        for j in range(start, start + length):
            result.append(j)
    return result


def solve_part_2_efficiently(input: str) -> int:
    almanac = parse_input(input)
    seed_to_location = map_possible_seeds_to_location(almanac)
    return min(item.destination_start for item in seed_to_location)


def map_possible_seeds_to_location(almanac: Almanac) -> list[AlmanacMapItem]:
    seed_almanac_items = []
    for i in range(0, len(almanac.seeds), 2):
        start, range_ = almanac.seeds[i], almanac.seeds[i + 1]
        seed_almanac_items.append(AlmanacMapItem(destination_start=start, source_start=start, range=range_))

    seed_to_soil = flatten_source_to_destination(seed_almanac_items, almanac.seed_to_soil)
    seed_to_fertilizer = flatten_source_to_destination(seed_to_soil, almanac.soil_to_fertilizer)
    seed_to_water = flatten_source_to_destination(seed_to_fertilizer, almanac.fertilizer_to_water)
    seed_to_light = flatten_source_to_destination(seed_to_water, almanac.water_to_light)
    seed_to_temperature = flatten_source_to_destination(seed_to_light, almanac.light_to_temperature)
    seed_to_humidity = flatten_source_to_destination(seed_to_temperature, almanac.temperature_to_humidity)
    seed_to_location = flatten_source_to_destination(seed_to_humidity, almanac.humidity_to_location)
    return seed_to_location


def flatten_source_to_destination(from_: list[AlmanacMapItem], to_: list[AlmanacMapItem]) -> list[AlmanacMapItem]:
    new_items: list[AlmanacMapItem] = []
    for item in from_:
        new_items.extend(map_source_item_to_destination(item, to_))
    return new_items


def map_source_item_to_destination(first: AlmanacMapItem, to_: list[AlmanacMapItem]) -> list[AlmanacMapItem]:
    result: list[AlmanacMapItem] = []
    current = first.destination_start
    diff_first = 0
    to_index = 0
    while True:
        try:
            second = to_[to_index]
        except IndexError:
            second = None
        """
        There are 5 options

        First is completely before
        first  -####------
        second ------####- 
        ===> We map from to itself, as we know the to is sorted, and to cannot overlap else a first could map to two seconds
        ===> DONE

        First is slightly before
        first  -####------
        second ---####----
        ===> We map the overlapping parts of first to itself and set current to to where it overlaps and add the amounts to diff_first

        First is partially overlapping / start overlaps (same)
        first  ---####----
        second -########--
        ===> We map the overlapping parts of first to second. Make sure to keep also include the diff of second
        ===> DONE

        First is longer than overlapping
        first  ---######--
        second -######----
        ===> We map the overlapping parts of first to second. Make sure to keep also include the diff of second. We set current to to where it stops overlapping and add the amounts to diff_first

        First is beyond second
        first  -----#####-
        second -###-------
        ===> We just go to the next second in the list. If none are left, we map first to itself
        """
        if second is None or first.destination_end < second.source_start:
            result.append(AlmanacMapItem(source_start=current, destination_start=current, range=first.range - diff_first))
            return result
        if current < second.source_start:
            new_range = second.source_start - current
            result.append(AlmanacMapItem(source_start=current, destination_start=current, range=new_range))
            current += new_range
            diff_first += new_range
            continue
        if first.destination_end < second.source_end:
            new_range = first.destination_end - current
            diff_second = current - second.source_start
            result.append(
                AlmanacMapItem(source_start=current, destination_start=second.destination_start + diff_second, range=new_range)
            )
            return result
        if first.destination_start < second.source_end:
            new_range = second.source_end - current
            diff_second = current - second.source_start
            result.append(
                AlmanacMapItem(source_start=current, destination_start=second.destination_start + diff_second, range=new_range)
            )
            current += new_range
            diff_first += new_range
            to_index += 1
            continue
        else:
            to_index += 1
            continue


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
