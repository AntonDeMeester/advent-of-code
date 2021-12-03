import math
from typing import Tuple

try:
    with open("advent_of_code/12_risk_of_rain_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("12_risk_of_rain_input.txt", "r") as input_file:
        input = input_file.read()


def move(instruction: str, angle: float) -> Tuple[Tuple[float, float], int]:
    direction = instruction[0]
    amount = int(instruction[1:])
    vector: Tuple[float, float] = (0, 0)
    if direction == "N":
        vector = (0, 1)
    elif direction == "E":
        vector = (1, 0)
    elif direction == "S":
        vector = (0, -1)
    elif direction == "W":
        vector = (-1, 0)
    elif direction == "L":
        angle += amount
    elif direction == "R":
        angle -= amount
    elif direction == "F":
        rad = math.radians(angle)
        vector = (math.cos(rad), math.sin(rad))
    return ((vector[0] * amount, vector[1] * amount), angle)


def part_one():
    instructions = input.split("\n")
    angle = 0
    location: Tuple[float, float] = (0, 0)
    for ins in instructions:
        (dx, dy), angle = move(ins, angle)
        location = (location[0] + dx, location[1] + dy)
    print(location)


def move_waypoint(
    instruction: str, waypoint: Tuple[float, float]
) -> Tuple[float, float]:
    direction = instruction[0]
    amount = int(instruction[1:])
    if direction == "N":
        return (waypoint[0], waypoint[1] + amount)
    if direction == "E":
        return (waypoint[0] + amount, waypoint[1])
    if direction == "S":
        return (waypoint[0], waypoint[1] + -amount)
    if direction == "W":
        return (waypoint[0] + -amount, waypoint[1])
    angle = math.radians(amount) * (1 if direction == "L" else -1)
    c, s = math.cos(angle), math.sin(angle)
    return (waypoint[0] * c - waypoint[1] * s, waypoint[0] * s + waypoint[1] * c)


def part_two():
    instructions = input.split("\n")
    waypoint = (10, 1)
    location: Tuple[float, float] = (0, 0)
    for ins in instructions:
        if ins[0] == "F":
            amount = int(ins[1:])
            location = (
                location[0] + waypoint[0] * amount,
                location[1] + waypoint[1] * amount,
            )
            continue
        waypoint = move_waypoint(ins, waypoint)
    print(location)
    print(sum(abs(a) for a in location))


part_one()
part_two()