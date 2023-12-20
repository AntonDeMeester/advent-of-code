from .main import solve_part_1, solve_part_2

layout = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

layout_unfortunate = """111111111111
999999999991
999999999991
999999999991
999999999991"""


def test_example_one_single():
    result = solve_part_1(layout)
    assert result == 102


def test_example_two():
    result = solve_part_2(layout)
    assert result == 94


def test_example_two_unfortunate():
    result = solve_part_2(layout_unfortunate)
    assert result == 71
