from .main import solve_part_1, solve_part_2

drawing = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_example_one():
    result = solve_part_1(drawing)
    assert result == 405


def test_example_two():
    result = solve_part_2(drawing)
    assert result == 400
