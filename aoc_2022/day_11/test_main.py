from .main import load_and_solve_part_1, load_and_solve_part_2, solve_part_1, solve_part_2

sample_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 10605


def test_part_1_with_real_data():
    result = load_and_solve_part_1()
    assert result == 61503


def test_part_2_1():
    result = solve_part_2(sample_data)
    assert result == 2713310158


def test_part_2_with_real_data():
    result = load_and_solve_part_2()
    assert result == 14081365540
