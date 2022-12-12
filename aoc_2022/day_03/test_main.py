from .main import solve_part_1, solve_part_2

sample_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 157


def test_part_2():
    result = solve_part_2(sample_data)
    assert result == 70
