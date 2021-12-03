from collections import defaultdict
from typing import List

try:
    with open("advent_of_code/14_masks_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("14_masks_input.txt", "r") as input_file:
        input = input_file.read()


def apply_mask(mask: str, value: int) -> int:
    bin_value = str(bin(value))[2:]
    if len(bin_value) < len(mask):
        bin_value = ("0" * (len(mask) - len(bin_value))) + bin_value
    masked_value = "".join(
        value_i if masked_i == "X" else masked_i
        for masked_i, value_i in zip(mask, bin_value)
    )

    return int(masked_value, 2)


def part_one():
    lines = input.split("\n")
    mask = ""
    memory = defaultdict(int)

    for line in lines:
        parsed = line.split(" = ")
        if parsed[0] == "mask":
            mask = parsed[1]
            continue
        mem_loc = parsed[0][4:-1]
        memory[mem_loc] = apply_mask(mask, int(parsed[1]))

    print(sum(memory.values()))


def add_string_to_list(new_char: str, value_list: List[str]) -> List[str]:
    return [v + new_char for v in value_list]


def apply_mem_mask(mask: str, memory: int) -> List[str]:
    bin_value = str(bin(memory))[2:]
    if len(bin_value) < len(mask):
        bin_value = ("0" * (len(mask) - len(bin_value))) + bin_value
    floating_values: List[str] = [""]
    for i in range(len(mask)):
        if mask[i] == "0":
            floating_values = add_string_to_list(bin_value[i], floating_values)
            continue
        if mask[i] == "1":
            floating_values = add_string_to_list(mask[i], floating_values)
            continue
        if mask[i] == "X":
            floating_values = add_string_to_list(
                "1", floating_values
            ) + add_string_to_list("0", floating_values)

    return floating_values


def part_two():
    lines = input.split("\n")
    mask = ""
    memory = defaultdict(int)

    for line in lines:
        parsed = line.split(" = ")
        if parsed[0] == "mask":
            mask = parsed[1]
            continue
        floating_mem_locks = apply_mem_mask(mask, int(parsed[0][4:-1]))
        for mem in floating_mem_locks:
            memory[mem] = int(parsed[1])

    print(sum(memory.values()))


part_one()
part_two()