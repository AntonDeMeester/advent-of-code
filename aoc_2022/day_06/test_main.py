import pytest

from .main import solve_part_1, solve_part_2

data_tests_one = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
)

data_tests_two = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
)


@pytest.mark.parametrize("input,result", data_tests_one)
def test_part_1(input: str, result: int):
    result = solve_part_1(input)
    assert result == result


@pytest.mark.parametrize("input,result", data_tests_two)
def test_part_2(input: str, result: int):
    result = solve_part_2(input)
    assert result == result
