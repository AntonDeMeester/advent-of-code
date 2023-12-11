from .main import solve_part_1, solve_part_2

galaxy = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def test_example_one():
    result = solve_part_1(galaxy)
    assert result == 374


def test_example_two_1():
    result = solve_part_2(galaxy, 1)
    assert result == 374


def test_example_two_10():
    result = solve_part_2(galaxy, 9)
    assert result == 1030


def test_example_two_100():
    result = solve_part_2(galaxy, 99)
    assert result == 8410
