from .main import solve_part_1, solve_part_2

schematic = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test_example_one():
    result = solve_part_1(schematic)
    assert result == 4361


def test_example_two():
    result = solve_part_2(schematic)
    assert result == 467835
