from .main import solve_part_1, solve_part_2

example_data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def test_example_one():
    result = solve_part_1(example_data)
    assert result == 142

example_data_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def test_example_two():
    result = solve_part_2(example_data_2)
    assert result == 281
