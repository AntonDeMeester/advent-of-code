from aoc_2022.utils.matrix import Matrix
from aoc_2022.utils.parsing import load_file, split_by_newline
from aoc_2022.utils.run import run_and_benchmark

Tree = int
Row = list[int]
Forest = Matrix[Tree]


def check_if_visible_line(line: list[int], index: int) -> bool:
    height = line[index]
    return all(height > other for other in line[:index]) or all(height > other for other in line[index + 1 :])


def parse_input(input: str) -> Forest:
    return Matrix([[Tree(i) for i in row] for row in split_by_newline(input)])


def count_visible_trees_outside(forest: Forest) -> int:
    edges = 2 * forest.horizontal_length() + 2 * forest.vertical_length() - 4
    visible_center = 0
    for i, j, _ in forest:
        if i == 0 or i == forest.horizontal_length() - 1:
            continue
        if j == 0 or j == forest.vertical_length() - 1:
            continue
        row = forest.get_row(j)
        column = forest.get_column(i)
        if check_if_visible_line(row, i) or check_if_visible_line(column, j):
            visible_center += 1
    return edges + visible_center


def load_and_solve_part_1() -> int:
    input = load_file(8)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    forest = parse_input(input)
    return count_visible_trees_outside(forest)


def count_visible_trees_line(line: list[int], loc: int, forward: bool) -> int:
    height = line[loc]
    count = 1
    iterator = range(loc + 1, len(line)) if forward else range(loc - 1, -1, -1)
    for i in iterator:
        if line[i] < height:
            count += 1
        else:
            break
    else:
        count -= 1
    return count


def count_visible_trees_inside(forest: Forest, x: int, y: int) -> tuple[int, int, int, int]:
    row = forest.get_row(y)
    column = forest.get_column(x)

    left = count_visible_trees_line(row, x, False)
    right = count_visible_trees_line(row, x, True)
    top = count_visible_trees_line(column, y, False)
    bottom = count_visible_trees_line(column, y, True)

    return (left, top, right, bottom)


def calculate_scenic_score(forest: Forest, i: int, j: int) -> int:
    tree_amounts = count_visible_trees_inside(forest, i, j)
    return tree_amounts[0] * tree_amounts[1] * tree_amounts[2] * tree_amounts[3]


def calculate_maximum_scenic_score(forest: Forest) -> int:
    scenic_scores = [
        [calculate_scenic_score(forest, x, y) for x in range(forest.horizontal_length())]
        for y in range(forest.vertical_length())
    ]
    return max(max(score for score in row) for row in scenic_scores)


def load_and_solve_part_2() -> int:
    input = load_file(8)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    forest = parse_input(input)
    return calculate_maximum_scenic_score(forest)


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
