try:
    with open("advent_of_code/07_luggage_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("07_luggage_input.txt", "r") as input_file:
        input = input_file.read()


def parse_input():
    parsed = input.replace("bags", "bag").replace(".\n", "\n").replace(" bag", "")
    split = [item.split(" contain ") for item in parsed.split("\n")]
    split = {key: value.split(", ") for key, value in split}
    parsed_dict = {}
    for key, value in split.items():
        parsed_bags = [bag_item.split(" ", 1) for bag_item in value]
        parsed_dict[key] = {bag[1]: bag[0] for bag in parsed_bags}
    return parsed_dict


def get_possible_list(bag_type: str, total_dict: dict) -> set:
    return {key for key, value in total_dict.items() if bag_type in value}


def part_one():
    bag_dict = parse_input()
    solution = set()
    bags_to_check = {"shiny gold"}

    while bags_to_check:
        bags_would_contain = set()
        for item in bags_to_check:
            bags_would_contain |= get_possible_list(item, bag_dict)

        bags_to_check = bags_would_contain - solution
        solution |= bags_would_contain

    print(len(solution))


def get_amount_in_bag(bag_name, bag_dict) -> int:
    contained_bags = bag_dict[bag_name]
    total = 1
    for key, value in contained_bags.items():
        if value == "no":
            return 1
        total += int(value) * get_amount_in_bag(key, bag_dict)
    return total


def part_two():
    bag_dict = parse_input()
    print(get_amount_in_bag("shiny gold", bag_dict) - 1)


part_one()
part_two()