from .main import solve_part_1, solve_part_2

boat_timings = """Time:      7  15   30
Distance:  9  40  200"""


def test_example_one():
    result = solve_part_1(boat_timings)
    assert result == 288


def test_example_two():
    result = solve_part_2(boat_timings)
    assert result == 71503
