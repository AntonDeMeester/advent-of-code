from aoc_2023.utils.parsing import load_file, split_by_newline
from aoc_2023.utils.run import run_and_benchmark
from dataclasses import dataclass
import re
from typing import Generator

from aoc_2023.utils.space import Direction, Coordinate, move_from_coordinate
from aoc_2023.utils.matrix import Matrix

INPUT_REGEX = r"([UDRL]) (\d+) \(#(\w{6})\)"


@dataclass
class Instruction:
    direction: Direction
    amount: int
    color: str


@dataclass
class Plot:
    coordinate: Coordinate
    line: tuple[Direction | None, Direction | None] = (None, None)
    color: str | None = None
    dug_out: bool = False


class Grid(Matrix[Plot]):
    def __init__(self, data: list[list[Plot]], min_x: int, min_y: int):
        super().__init__(data)
        self.min_x = min_x
        self.min_y = min_y

    def get(self, x: int, y: int) -> Plot:
        return self.data[y - self.min_y][x - self.min_x]

    def get_row(self, index: int) -> list[Plot]:
        return self.data[index - self.min_y]

    def get_column(self, index: int) -> list[Plot]:
        return [x[index - self.min_x] for x in self.data]

    def print_grid(self):
        with open("test.txt", "w") as f:
            f.write("\n".join("".join("#" if v.dug_out else "." for v in row) for row in self.get_rows()))

    def __iter__(self) -> Generator[tuple[int, int, Plot], None, None]:
        for j, row in enumerate(self.data):
            for i, value in enumerate(row):
                yield (i + self.min_x, j + self.min_y, value)


def load_and_solve_part_1() -> int:
    input = load_file(18)
    return solve_part_1(input)


def solve_part_1(input: str):
    instructions = parse_input(input)
    grid = create_grid(instructions)
    return sum(v.dug_out for _, _, v in grid)


def solve_part_1_shoelace(input: str) -> int:
    instructions = parse_input(input)
    contained = calculate_contained_area(instructions)
    circumference = calculate_circumference(instructions)
    return calculate_area(contained, circumference)


def parse_input(input: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in split_by_newline(input):
        regexed = re.match(INPUT_REGEX, line)
        instructions.append(Instruction(direction=Direction(regexed[1]), amount=int(regexed[2]), color=regexed[3]))
    return instructions


def create_grid(instructions: list[Instruction]) -> Grid:
    outlines = get_outlines(instructions)
    grid = fill_grid(outlines)
    return grid


def get_outlines(instructions: list[Instruction]) -> list[Plot]:
    plots: list[Plot] = []
    position = Coordinate(0, 0)
    previous_plot: Plot | None = None
    for ins in instructions:
        for _ in range(ins.amount):
            position = move_from_coordinate(position, ins.direction)
            if previous_plot is not None:
                previous_plot.line = (previous_plot.line[0], ins.direction)
            plot = Plot(position, line=(ins.direction, None), color=ins.color)
            plots.append(plot)
            previous_plot = plot
    # Mark end with the start direction
    plots[-1].line = (plots[-1].line[0], plots[0].line[1])
    return plots


def fill_grid(outlines: list[Plot]) -> Grid:
    min_x, max_x, min_y, max_y = get_corners(outlines)
    grid = Grid([[Plot(Coordinate(x, y)) for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)], min_x, min_y)
    grid = mark_grid_outline(outlines, grid)
    grid = fill_inside_grid(grid)
    return grid


def get_corners(outlines: list[Plot]) -> tuple[int, int, int, int]:
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for plot in outlines:
        min_x = min(min_x, plot.coordinate.x)
        max_x = max(max_x, plot.coordinate.x)
        min_y = min(min_y, plot.coordinate.y)
        max_y = max(max_y, plot.coordinate.y)
    return min_x, max_x, min_y, max_y


def mark_grid_outline(outlines: list[Plot], grid: Grid) -> Grid:
    for plot in outlines:
        value = grid.get_from_coordinate(plot.coordinate)
        if value is None:
            raise ValueError()
        value.color = plot.color
        value.dug_out = True
        value.line = plot.line
    return grid


def fill_inside_grid(grid: Grid) -> Grid:
    for row in grid.get_rows():
        inside = False
        for value in row:
            # See day 10 `get_count_enclosed_pipes`
            # We count when we flip from outside to inside. We only consider north connections
            # if pipe.value in ("|", "L", "J"):
            if value.line[1] == Direction.UP or value.line[0] == Direction.DOWN:
                inside = not inside
            if value.line == (None, None):
                value.dug_out = inside
    return grid


def load_and_solve_part_2() -> int:
    input = load_file(18)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    instructions = parse_input_colours(input)
    contained = calculate_contained_area(instructions)
    circumference = calculate_circumference(instructions)
    return calculate_area(contained, circumference)


def parse_input_colours(input: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in split_by_newline(input):
        regexed = re.match(INPUT_REGEX, line)
        color = regexed[3]
        amount = int(color[:5], 16)
        direction = convert_direction_from_hex(color[-1])
        instructions.append(Instruction(direction=direction, amount=amount, color=color))
    return instructions


def convert_direction_from_hex(hex_direction: str) -> Direction:
    if hex_direction == "0":
        return Direction.RIGHT
    if hex_direction == "1":
        return Direction.DOWN
    if hex_direction == "2":
        return Direction.LEFT
    if hex_direction == "3":
        return Direction.UP
    raise ValueError("Could not parse direction")


def calculate_contained_area(instructions: list[Instruction]) -> int:
    corners = get_area_corners(instructions)
    area = execute_shoelace_theorem(corners)
    return area


def execute_shoelace_theorem(coords: list[Coordinate]) -> int:
    """Uses Shoelace formula to calculate the inside"""
    total = 0
    for i in range(len(coords)):
        one, two = coords[i - 1], coords[i]
        total += one.x * two.y - two.x * one.y
    return abs(total // 2)


def get_area_corners(instructions: list[Instruction]) -> list[Coordinate]:
    corners: list[Coordinate] = []
    position = Coordinate(0, 0)
    for ins in instructions:
        position = move_from_coordinate(position, ins.direction, ins.amount)
        corners.append(position)
    return corners


def calculate_circumference(instructions: list[Instruction]) -> int:
    return sum(i.amount for i in instructions)


def calculate_area(contained: int, circumference: int) -> int:
    """Uses Pick's theorem to calculate the area"""
    return contained + circumference // 2 + 1


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
