from typing import Optional, Tuple

try:
    with open("advent_of_code/18_math_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("18_math_input.txt", "r") as input_file:
        input = input_file.read()


def get_closing_bracket_index(line: str) -> int:
    if line[0] != "(":
        return -1
    open_index = line.find("(", 1)
    close_index = line.find(")", 0)
    while open_index != -1 and open_index < close_index:
        open_index = line.find("(", open_index + 1)
        close_index = line.find(")", close_index + 1)
    return close_index


def split_first_atom(line: str) -> Tuple[str, Optional[str], Optional[str]]:
    close_index = 0
    if line[0] == "(":
        close_index = get_closing_bracket_index(line)
    mul_close = close_index
    mul_open = line.find("(", mul_close)
    mul_loc = line.find("*", mul_close)
    while mul_loc != -1 and mul_open != -1 and mul_loc > mul_open:
        mul_close = get_closing_bracket_index(line[mul_open:]) + mul_open
        mul_open = line.find("(", mul_close)
        mul_loc = line.find("*", mul_close)

    if mul_loc != -1:
        return line[: mul_loc - 1], "*", line[mul_loc + 2 :]
    if " + " in line:
        return line[: close_index + 1], "+", line[close_index + 4 :]
    return line[: close_index + 1], None, None


def is_complex(atom: str) -> bool:
    return len(atom.split(" ")) > 1


def evaluate_atom(atom: str) -> int:
    if atom[0] == "(" and get_closing_bracket_index(atom) == len(atom) - 1:
        return evaluate_atom(atom[1 : get_closing_bracket_index(atom)])
    if is_complex(atom):
        return calculate_line(atom)
    return int(atom)


def calculate_line(line: str) -> int:
    atom, operand, rest = split_first_atom(line)
    atom_value = evaluate_atom(atom)
    if operand is None or rest is None:
        return atom_value
    rest_value = evaluate_atom(rest)
    if operand == "*":
        return atom_value * rest_value
    else:
        return atom_value + rest_value


def part_one():
    lines = input.split("\n")
    for line in lines:
        print(calculate_line(line))
    print(sum(calculate_line(line) for line in lines))


part_one()

"""
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
