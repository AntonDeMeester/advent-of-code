from .main import solve_part_1, solve_part_2

square = """.....
.S-7.
.|.|.
.L-J.
....."""

complex = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


def test_example_one_simple():
    result = solve_part_1(square)
    assert result == 4


def test_example_one_complex():
    result = solve_part_1(complex)
    assert result == 8


enclosed_one = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

enclosed_two = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

enclosed_three = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

enclosed_four = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


def test_example_two_one():
    result = solve_part_2(enclosed_one, "F")
    assert result == 4


def test_example_two_two():
    result = solve_part_2(enclosed_two, "F")
    assert result == 4


def test_example_two_three():
    result = solve_part_2(enclosed_three, "F")
    assert result == 8


def test_example_two_four():
    result = solve_part_2(enclosed_four, "7")
    assert result == 10
