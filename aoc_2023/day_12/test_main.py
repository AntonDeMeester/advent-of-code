from .main import solve_part_1, solve_part_2

spring_map = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_example_one():
    result = solve_part_1(spring_map)
    assert result == 21


def test_example_two():
    result = solve_part_2(spring_map)
    assert result == 525152
