from collections import defaultdict

try:
    with open("advent_of_code/15_memory_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("15_memory_input.txt", "r") as input_file:
        input = input_file.read()


def part_one():
    starting = [int(i) for i in input.split(",")]

    spoken = defaultdict(list)
    last = 0
    for i, value in enumerate(starting):
        spoken[value].append(i + 1)
        last = value

    for i in range(len(starting) + 1, 2020 + 1):
        used_list = spoken[last]
        last = 0 if len(used_list) <= 1 else i - used_list[-2] - 1
        spoken[last].append(i)
    print(last)


def part_two():
    starting = [int(i) for i in input.split(",")]

    spoken = defaultdict(list)
    last = 0
    for i, value in enumerate(starting):
        spoken[value].append(i + 1)
        last = value

    for i in range(len(starting) + 1, 30000000 + 1):
        used_list = spoken[last]
        last = 0 if len(used_list) <= 1 else i - used_list[-2] - 1
        spoken[last].append(i)
    print(last)


part_one()
part_two()