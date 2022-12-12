from .main import solve_part_1, solve_part_2

sample_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == "CMZ"


def test_part_2():
    result = solve_part_2(sample_data)
    assert result == "MCD"
