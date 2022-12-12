from .main import solve_part_1, solve_part_2

sample_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 2


def test_part_2():
    result = solve_part_2(sample_data)
    assert result == 4


# def test_part_2_with_input():
#     input = load_file(2)
#     return solve_part_2(input)
