from .main import solve_part_1, solve_part_2

example_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_example_one():
    result = solve_part_1(example_data)
    assert result == 24000


def test_example_two():
    result = solve_part_2(example_data)
    assert result == 45000
