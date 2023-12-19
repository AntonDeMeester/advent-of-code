from .main import solve_part_1, solve_part_2

single_value = "HASH"
list_value = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_example_one_single():
    result = solve_part_1(single_value)
    assert result == 52


def test_example_one_multiple():
    result = solve_part_1(list_value)
    assert result == 1320


def test_example_two():
    result = solve_part_2(list_value)
    assert result == 145
