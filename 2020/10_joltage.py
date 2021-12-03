from collections import Counter

try:
    with open("advent_of_code/10_joltage_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("10_joltage_input.txt", "r") as input_file:
        input = input_file.read()


def part_one():
    joltages = sorted([int(line) for line in input.split("\n")])

    previous = joltages[0]
    current = joltages[1]
    index = 1
    # Ground to first adapter
    joltage_diffs = [previous]

    try:
        while True:
            joltage_diffs.append(current - previous)

            index += 1
            previous, current = current, joltages[index]
    except IndexError:
        pass
    # Highest adapter to device
    joltage_diffs.append(3)

    counter = Counter(joltage_diffs)
    print(counter)
    print(counter[3] * counter[1])


def part_two():
    joltages = sorted([int(line) for line in input.split("\n")])

    step_map = {0: 1}
    for jolt in joltages:
        options = 0
        for i in [1, 2, 3]:
            options += step_map.get(jolt - i, 0)
        step_map[jolt] = options

    print(options)


part_one()
part_two()
