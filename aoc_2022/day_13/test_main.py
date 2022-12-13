from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 13


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 5760


def test_part_2_1():
    result = solve_part_2(sample_data)
    assert result == 140


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 26670
