try:
    with open("advent_of_code/09_encoding_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("09_encoding_input.txt", "r") as input_file:
        input = input_file.read()


def part_one():
    lines = [int(i) for i in input.split("\n")]
    index = 0
    offset = 25

    while True:
        next_number = lines[index + offset]
        for i, first in enumerate(lines[index : index + offset]):
            for second in lines[index + i : index + offset]:
                if first + second == next_number:
                    break
            else:
                continue
            break
        else:
            print(f"The wrong number was {next_number}")
            return next_number
        index += 1


def part_two():
    wrong_number = part_one()

    lines = [int(i) for i in input.split("\n")]
    for i in range(len(lines)):
        offset = 1
        total = sum(lines[i : i + offset + 1])
        while total <= wrong_number:
            if total == wrong_number:
                break
            offset += 1
            total = sum(lines[i : i + offset + 1])
        else:
            continue
        print(f"{wrong_number} is the sum from index {i} to and including {i+offset}.")
        edges = max(lines[i : i + offset + 1]) + min(lines[i : i + offset + 1])
        print(f"Sum of min and max is {edges}")


part_one()
part_two()