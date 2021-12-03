import math
from typing import List, Optional

try:
    with open("advent_of_code/13_waiting_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("13_waiting_input.txt", "r") as input_file:
        input = input_file.read()


def part_one():
    lines = input.split("\n")
    time = int(lines[0])
    buses = lines[1].split(",")

    first_bus = None
    first_bus_time = 1e20
    for bus in buses:
        if bus.strip() == "x":
            continue
        period = int(bus)
        bus_time = (((time - 1) // period) + 1) * (period)
        if bus_time < first_bus_time:
            first_bus_time = bus_time
            first_bus = period
    print(
        f"Bus {first_bus} arrived at {first_bus_time}, {first_bus_time - time} after you arrive at {time}"
    )
    print(f"Solution = {(first_bus_time - time) * first_bus}")


def check_solution(time_stamp: int, bus_list: List[Optional[int]]) -> bool:
    # for i, bus in enumerate(bus_list):
    #     if bus is None:
    #         continue
    #     if ((time_stamp + i) % bus) != 0:
    #         return False
    # return True
    for i, value in bus_list.items():
        if ((time_stamp + i) % value) != 0:
            return False
    return True


def part_two():
    lines = input.split("\n")
    # buses = [int(bus) if bus.strip() != "x" else None for bus in lines[1].split(",")]
    buses = {
        i: int(value)
        for i, value in enumerate(lines[1].split(","))
        if value.strip() != "x"
    }
    solved = False
    # max_time = max(int(bus) for bus in buses if bus is not None)
    # max_time = max(buses.values())
    max_time = 523 * 547 * 41  # the time for which the two highest numbers work out
    # time = buses.index(max_time)
    # time = [k for k, v in buses.items() if v == max_time][0]
    time = 6711640  # time initial moment for which the two highest numbers work out

    while not solved:
        time += max_time
        solved = check_solution(time, buses)
    print(time)


def test():
    for i in range(523 * 547 * 41):
        if ((i + 19) % 523) == 0 and ((i + 50) % 547) == 0 and ((i + 60) % 41) == 0:
            print(i)


part_one()
part_two()