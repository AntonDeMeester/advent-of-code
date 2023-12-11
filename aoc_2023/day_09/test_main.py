from .main import solve_part_1, solve_part_2

almanac = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_example_one():
    result = solve_part_1(almanac)
    assert result == 114


def test_example_two():
    result = solve_part_2(almanac)
    assert result == 2
