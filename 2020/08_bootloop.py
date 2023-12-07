from typing import Optional

try:
    with open("advent_of_code/08_bootloop_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("08_bootloop_input.txt", "r") as input_file:
        input = input_file.read()


def part_one():
    instructions = [line.split(" ") for line in input.split("\n")]

    acc = 0
    line_history = set()
    line_number = 0

    while line_number not in line_history:
        line = instructions[line_number]
        line_history.add(line_number)

        if line[0] == "acc":
            acc += int(line[1])
            line_number += 1
        elif line[0] == "jmp":
            line_number += int(line[1])
        elif line[0] == "nop":
            line_number += 1

    print(acc)


def get_next(current_line_number, current_instruction, instructions):
    acc = 0
    if current_instruction[0] == "acc":
        acc += int(current_instruction[1])
        next_line_number = current_line_number + 1
    elif current_instruction[0] == "jmp":
        next_line_number = current_line_number + int(current_instruction[1])
    elif current_instruction[0] == "nop":
        next_line_number = current_line_number + 1
    try:
        next_instruction = instructions[next_line_number]
    except IndexError:
        next_instruction = None
    return next_line_number, next_instruction, acc


def terminates(current_line_number, current_instruction, instructions, history: set):
    line_number = current_line_number
    line = current_instruction
    history = history.copy()

    while line_number not in history:
        history.add(line_number)
        if line[0] == "acc":
            line_number += 1
        elif line[0] == "jmp":
            line_number += int(line[1])
        elif line[0] == "nop":
            line_number += 1

        try:
            line = instructions[line_number]
        except IndexError:
            return True

    return False


def get_result(instructions, history, line_number, acc) -> Optional[int]:
    try:
        while line_number not in history:
            line = instructions[line_number]
            history.add(line_number)

            if line[0] == "acc":
                acc += int(line[1])
                line_number += 1
            elif line[0] == "jmp":
                line_number += int(line[1])
            elif line[0] == "nop":
                line_number += 1
        return None
    except IndexError:
        return acc


def switcharoo(instruction):
    if instruction[0] == "nop":
        instruction[0] = "jmp"
    elif instruction[0] == "jmp":
        instruction[0] = "nop"
    return instruction


def part_two():
    instructions = [line.split(" ") for line in input.split("\n")]

    acc = 0
    line_history = set()
    line_number = 0
    current_instruction = instructions[0]

    while line_number not in line_history:
        if current_instruction[0] in ["nop", "jmp"]:
            current_instruction = switcharoo(current_instruction)

            if terminates(line_number, current_instruction, instructions, line_history):
                acc = get_result(instructions, line_history, line_number, acc)
                break

            current_instruction = switcharoo(current_instruction)

        line_history.add(line_number)
        line_number, current_instruction, increase = get_next(line_number, current_instruction, instructions)
        acc += increase
        if current_instruction is None:
            break
    else:
        print("failure")

    print(acc)


part_one()
part_two()
