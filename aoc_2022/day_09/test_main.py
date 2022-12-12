from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


sample_data_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 13


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 5779


def test_part_2_1():
    result = solve_part_2(sample_data)
    assert result == 1


def test_part_2_2():
    result = solve_part_2(sample_data_2)
    assert result == 36


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 2331
