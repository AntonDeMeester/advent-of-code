from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 24


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 843


def test_part_2_1():
    result = solve_part_2(sample_data)
    assert result == 93


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 27625
