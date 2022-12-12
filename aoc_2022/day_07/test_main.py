from aoc_2022.utils.parsing import load_file

from .main import solve_part_1, solve_part_2

sample_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def test_part_1():
    result = solve_part_1(sample_data)
    assert result == 95437


def test_part_1_with_real_data():
    input = load_file(7)
    result = solve_part_1(input)
    assert result == 1723892


def test_part_2():
    result = solve_part_2(sample_data)
    assert result == 24933642


def test_part_2_with_real_data():
    input = load_file(7)
    result = solve_part_2(input)
    assert result == 8474158
