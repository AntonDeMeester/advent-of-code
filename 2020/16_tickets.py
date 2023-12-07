from collections import defaultdict
from typing import Dict, List, Tuple

try:
    with open("advent_of_code/16_tickets_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("16_tickets_input.txt", "r") as input_file:
        input = input_file.read()


def parse_options(options: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    result = defaultdict(list)
    for o in options:
        key_split = o.split(": ")
        ranges = key_split[1].split(" or ")
        for r in ranges:
            values = r.split("-")
            result[key_split[0]].append((int(values[0]), int(values[1])))
    return result


def find_match(value: int, options: List[Tuple[int, int]]) -> bool:
    return any(o[0] <= value <= o[1] for o in options)


def part_one():
    blocks = input.split("\n\n")
    options_raw = blocks[0].split("\n")
    options = parse_options(options_raw)
    yours_raw = blocks[1].split("\n")[1:]
    yours = yours_raw[0].split(",")
    nearby_raw = blocks[2].split("\n")[1:]
    nearby = [[int(v) for v in l.split(",")] for l in nearby_raw]

    options_flat = [r for o in options.values() for r in o]
    result = 0
    for l in nearby:
        for v in l:
            if not find_match(v, options_flat):
                result += v
    print(result)


def part_two():
    blocks = input.split("\n\n")
    options_raw = blocks[0].split("\n")
    options = parse_options(options_raw)
    yours_raw = blocks[1].split("\n")[1:]
    yours = yours_raw[0].split(",")
    nearby_raw = blocks[2].split("\n")[1:]
    nearby = [[int(v) for v in l.split(",")] for l in nearby_raw]

    options_flat = [r for o in options.values() for r in o]
    correct_tickets = [l for l in nearby if all(find_match(o, options_flat) for o in l)]

    column_options: List[List[str]] = []
    for i in range(len(correct_tickets[0])):
        column = [ticket[i] for ticket in correct_tickets]
        possible_keys = []
        for key, values in options.items():
            if all(find_match(v, values) for v in column):
                possible_keys.append(key)
        column_options.append(possible_keys)

    while max(len(option) for option in column_options) > 1:
        to_prune_list = []
        for option in column_options:
            if len(option) == 1:
                to_prune_list.append(option[0])
        pruned_options = []
        for to_prune in to_prune_list:
            pruned_options = []
            changed = False
            for options in column_options:
                if options == [to_prune]:
                    pruned_options.append(options)
                    continue
                changed = changed or any(to_prune == value for value in options)
                pruned_options.append([value for value in options if value != to_prune])
            if changed:
                break

        column_options = pruned_options
    column_options = [options[0] for options in column_options]
    result = 1
    for i, column in enumerate(column_options):
        if column.startswith("departure"):
            result *= int(yours[i])
    print(result)


# part_one()
part_two()
