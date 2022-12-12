from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """30373
25512
65332
33549
35390"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 21


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 1827


def test_part_2():
    result = solve_part_2(sample_data)
    assert result == 8


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 335580
