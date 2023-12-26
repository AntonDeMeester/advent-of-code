from .main import solve_part_1, solve_part_2, solve_part_1_shoelace

instructions = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def test_example_one():
    result = solve_part_1(instructions)
    assert result == 62


def test_example_one_pick():
    result = solve_part_1_shoelace(instructions)
    assert result == 62


def test_example_two():
    result = solve_part_2(instructions)
    assert result == 952408144115
