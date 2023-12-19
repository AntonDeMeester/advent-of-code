from .main import solve_part_1, solve_part_2

parabola = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def test_example_one():
    result = solve_part_1(parabola)
    assert result == 136


def test_example_two():
    result = solve_part_2(parabola)
    assert result == 64
