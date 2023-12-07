from .main import solve_part_1, solve_part_2

boat_timings = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_example_one():
    result = solve_part_1(boat_timings)
    assert result == 6440


def test_example_two():
    result = solve_part_2(boat_timings)
    assert result == 5905
