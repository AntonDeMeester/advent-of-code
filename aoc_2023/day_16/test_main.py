from .main import solve_part_1, solve_part_2

layout = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def test_example_one_single():
    result = solve_part_1(layout)
    assert result == 46


def test_example_two():
    result = solve_part_2(layout)
    assert result == 51
