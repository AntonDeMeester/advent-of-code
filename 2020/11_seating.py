from copy import deepcopy
from typing import Counter, List, Optional, Tuple

try:
    with open("advent_of_code/11_seating_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("11_seating_input.txt", "r") as input_file:
        input = input_file.read()


def get_surrounding_seats(all_seats: List[List[str]], i: int, j: int) -> List[str]:
    result: List[str] = []
    number_of_rows = len(all_seats)
    number_of_columns = len(all_seats[0])
    if i > 0:
        result.extend(all_seats[i - 1][max(j - 1, 0) : j + 2])
    if j > 0:
        result.append(all_seats[i][j - 1])
    if j < number_of_columns - 1:
        result.append(all_seats[i][j + 1])
    if i < number_of_rows - 1:
        result.extend(all_seats[i + 1][max(j - 1, 0) : j + 2])
    return result


def get_visible_seat(all_seats: List[List[str]], location: Tuple[int, int], direction: Tuple[int, int]) -> str:
    seat = "."
    position = location
    while seat == ".":
        position = (position[0] + direction[0], position[1] + direction[1])
        if any(index < 0 for index in position):
            return "."
        try:
            seat = all_seats[position[0]][position[1]]
        except IndexError:
            return "."
    return seat


def get_visible_seats(all_seats: List[List[str]], i: int, j: int) -> List[str]:
    result: List[str] = []
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    for direc in directions:
        result.append(get_visible_seat(all_seats, (i, j), direc))
    return result


def part_one():
    seats = input.split("\n")

    last_seating = None
    new_seating = deepcopy(seats)

    while last_seating != new_seating:
        last_seating = new_seating
        new_seating = []
        for i, row in enumerate(last_seating):
            current_row = []
            for j, seat in enumerate(row):
                if seat == ".":
                    current_row.append(".")
                    continue
                surround = get_surrounding_seats(last_seating, i, j)
                counter = Counter(surround)
                if seat == "L":
                    if counter["#"] == 0:
                        current_row.append("#")
                    else:
                        current_row.append("L")
                    continue
                if counter["#"] >= 4:
                    current_row.append("L")
                else:
                    current_row.append("#")
            new_seating.append(current_row)
    total_counter = sum(Counter(row)["#"] for row in new_seating)
    print(f"Total number of occupied seats is {total_counter}")


def part_two():
    seats = input.split("\n")

    last_seating = None
    new_seating = deepcopy(seats)

    while last_seating != new_seating:
        last_seating = new_seating
        new_seating = []
        for i, row in enumerate(last_seating):
            current_row = []
            for j, seat in enumerate(row):
                if seat == ".":
                    current_row.append(".")
                    continue
                surround = get_visible_seats(last_seating, i, j)
                counter = Counter(surround)
                if seat == "L":
                    if counter["#"] == 0:
                        current_row.append("#")
                    else:
                        current_row.append("L")
                    continue
                if counter["#"] >= 5:
                    current_row.append("L")
                else:
                    current_row.append("#")
            new_seating.append(current_row)
    total_counter = sum(Counter(row)["#"] for row in new_seating)
    print(f"Total number of occupied seats is {total_counter}")


part_one()
part_two()
