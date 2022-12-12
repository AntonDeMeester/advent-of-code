from .main import solve_part_1, solve_part_2

example_data = """A Y
B X
C Z"""


def test_part_1():
    assert solve_part_1(example_data) == 15


def test_part_2():
    assert solve_part_2(example_data) == 12
