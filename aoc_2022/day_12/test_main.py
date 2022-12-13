from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 31


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 425


def test_part_2_1():
    result = solve_part_2(sample_data)
    assert result == 29


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 418
