from collections import defaultdict
from typing import Counter, Dict, List

try:
    with open("advent_of_code/17_hyperspace_input.txt", "r") as input_file:
        input = input_file.read()
except FileNotFoundError:
    with open("17_hyperspace_input.txt", "r") as input_file:
        input = input_file.read()

""" 3D
ThreeDimSpace = Dict[int, Dict[int, Dict[int, str]]]


def get_initial_space(initial_plane: str) -> ThreeDimSpace:
    # Z plane has y planes. Y planes has X planes. X plan defaults to "."
    cube: ThreeDimSpace = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: "."))
    )
    plane_0 = initial_plane.split("\n")

    for i, y in enumerate(plane_0):
        for j, x in enumerate(y):
            cube[0][i][j] = x

    return cube


def static_space(default_space: ThreeDimSpace) -> ThreeDimSpace:
    static_space: ThreeDimSpace = {}
    z_values = default_space.keys()
    y_values = default_space[0].keys()
    x_values = default_space[0][0].keys()
    for z in range(min(z_values) - 1, max(z_values) + 2):
        static_space[z] = {}
        for y in range(min(y_values) - 1, max(y_values) + 2):
            static_space[z][y] = {}
            for x in range(min(x_values) - 1, max(x_values) + 2):
                static_space[z][y][x] = default_space[z][y][x]

    return static_space


def get_surroundings(space: ThreeDimSpace, x: int, y: int, z: int) -> List[str]:
    all_points: List[str] = []
    # Above and below
    for z_value in (z - 1, z + 1):
        for y_value in (y - 1, y, y + 1):
            for x_value in (x - 1, x, x + 1):
                all_points.append(space[z_value][y_value][x_value])

    # To the sides
    for y_value in (y - 1, y + 1):
        for x_value in (x - 1, x, x + 1):
            all_points.append(space[z][y_value][x_value])

    # Front and back
    for x_value in (x - 1, x + 1):
        all_points.append(space[z][y][x_value])

    return all_points


def get_active_nodes(space: ThreeDimSpace) -> int:
    total_active = 0
    for plane in space.values():
        for line in plane.values():
            for point in line.values():
                total_active += 1 if point == "#" else 0
    return total_active


def part_one():
    space = get_initial_space(input)

    for _ in range(6):
        print(get_active_nodes(space))
        iterator_space = static_space(space)
        new_space: ThreeDimSpace = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: "."))
        )
        for z, plane in iterator_space.items():
            for y, line in plane.items():
                for x, point in line.items():
                    surrounding = get_surroundings(space, x, y, z)
                    counter = Counter(surrounding)
                    if point == "#":
                        new_point = "#" if 2 <= counter["#"] <= 3 else "."
                    else:
                        new_point = "#" if counter["#"] == 3 else "."
                    new_space[z][y][x] = new_point

        space = new_space
    print(get_active_nodes(space))


part_one()
"""

FourDimSpace = Dict[int, Dict[int, Dict[int, Dict[int, str]]]]


def get_initial_space(initial_plane: str) -> FourDimSpace:
    # Z plane has y planes. Y planes has X planes. X plan defaults to "."
    hyper_space: FourDimSpace = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: ".")))
    )
    plane_0 = initial_plane.split("\n")

    for i, y in enumerate(plane_0):
        for j, x in enumerate(y):
            hyper_space[0][0][i][j] = x

    return hyper_space


def static_space(default_space: FourDimSpace) -> FourDimSpace:
    static_space: FourDimSpace = {}
    w_values = default_space.keys()
    z_values = default_space[0].keys()
    y_values = default_space[0][0].keys()
    x_values = default_space[0][0][0].keys()
    for w in range(min(w_values) - 1, max(w_values) + 2):
        static_space[w] = {}
        for z in range(min(z_values) - 1, max(z_values) + 2):
            static_space[w][z] = {}
            for y in range(min(y_values) - 1, max(y_values) + 2):
                static_space[w][z][y] = {}
                for x in range(min(x_values) - 1, max(x_values) + 2):
                    static_space[w][z][y][x] = default_space[w][z][y][x]

    return static_space


def get_surroundings(
    hyper_space: FourDimSpace, x: int, y: int, z: int, w: int
) -> List[str]:
    all_points: List[str] = []
    # Hyper spaced
    for w_value in (w - 1, w + 1):
        for z_value in (z - 1, z, z + 1):
            for y_value in (y - 1, y, y + 1):
                for x_value in (x - 1, x, x + 1):
                    all_points.append(hyper_space[w_value][z_value][y_value][x_value])

    # Above and below
    for z_value in (z - 1, z + 1):
        for y_value in (y - 1, y, y + 1):
            for x_value in (x - 1, x, x + 1):
                all_points.append(hyper_space[w][z_value][y_value][x_value])

    # To the sides
    for y_value in (y - 1, y + 1):
        for x_value in (x - 1, x, x + 1):
            all_points.append(hyper_space[w][z][y_value][x_value])

    # Front and back
    for x_value in (x - 1, x + 1):
        all_points.append(hyper_space[w][z][y][x_value])

    return all_points


def get_active_nodes(hyper_space: FourDimSpace) -> int:
    total_active = 0
    for space in hyper_space.values():
        for plane in space.values():
            for line in plane.values():
                for point in line.values():
                    total_active += 1 if point == "#" else 0
    return total_active


def part_two():
    hyper_space = get_initial_space(input)

    for _ in range(6):
        print(get_active_nodes(hyper_space))
        iterator_space = static_space(hyper_space)
        new_hyper_space: FourDimSpace = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: ".")))
        )
        for w, space in iterator_space.items():
            for z, plane in space.items():
                for y, line in plane.items():
                    for x, point in line.items():
                        surrounding = get_surroundings(hyper_space, x, y, z, w)
                        counter = Counter(surrounding)
                        if point == "#":
                            new_point = "#" if 2 <= counter["#"] <= 3 else "."
                        else:
                            new_point = "#" if counter["#"] == 3 else "."
                        new_hyper_space[w][z][y][x] = new_point

        hyper_space = new_hyper_space
    print(get_active_nodes(hyper_space))


part_two()