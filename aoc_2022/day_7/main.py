from typing import Optional

from aoc_2022.utils.parsing import load_file, split_by, split_by_newline
from aoc_2022.utils.run import run_and_benchmark


class File:
    def __init__(self, parent: "Directory", size: int, name: str):
        self.parent = parent
        self.size = size
        self.name = name

    def get_size(self) -> int:
        return self.size

    def sum_directory_size_if_smaller_than(self, limit: int) -> int:
        return 0

    def find_smallest_directory_larger_than(self, limit: int) -> Optional["Directory"]:
        return None


class Directory:
    def __init__(self, name: str, parent: Optional["Directory"]):
        self.name = name
        self.parent = parent
        self.children: dict[str, "File" | "Directory"] = {}

    def get_size(self):
        return sum(child.get_size() for child in self.children.values())

    def sum_directory_size_if_smaller_than(self, limit: int) -> int:
        child_sum = sum(child.sum_directory_size_if_smaller_than(limit) for child in self.children.values())
        own_size = self.get_size()
        if own_size <= limit:
            return child_sum + own_size
        return child_sum

    def is_directory_smaller_than(self, limit: int) -> bool:
        return self.get_size() <= limit

    def find_smallest_directory_larger_than(self, limit: int) -> Optional["Directory"]:
        largest: Directory | None = None
        for child in self.children.values():
            child_largest = child.find_smallest_directory_larger_than(limit)
            if child_largest is None:
                continue
            if largest is None:
                largest = child_largest
                continue
            if limit < child_largest.get_size() < largest.get_size():
                largest = child_largest
        if largest is not None:
            return largest
        if self.get_size() > limit:
            return self
        return None

    def find_directory_to_free_space(self, disk_space: int, necessary_space: int) -> Optional["Directory"]:
        space_to_delete = necessary_space - (disk_space - self.get_size())
        return self.find_smallest_directory_larger_than(space_to_delete)


def create_file_structure(input: str) -> Directory:
    commands = split_by(input, "$ ")
    root = Directory("/", None)
    current = root
    for comm in commands[2:]:
        current = execute_command(comm, current)
    return root


def execute_command(command: str, directory: "Directory") -> "Directory":
    command, *result = split_by_newline(command)
    match command.split():
        case ["cd", ".."]:
            if directory.parent is None:
                raise ValueError("Can't go up from the root directory")
            return directory.parent
        case ["cd", child_name]:
            child = directory.children[child_name]
            if isinstance(child, File):
                raise ValueError("Cannot cd into a file")
            return child
        case ["ls"]:
            return add_children(directory, result)
    raise ValueError("Unknown command")


def add_children(directory: "Directory", children: list[str]) -> "Directory":
    for child in children:
        if not child:
            continue
        one, two = child.split(" ")
        if one == "dir":
            directory.children[two] = Directory(two, directory)
        else:
            directory.children[two] = File(directory, int(one), two)
    return directory


def load_and_solve_part_1() -> int:
    input = load_file(7)
    return solve_part_1(input)


def solve_part_1(input: str) -> int:
    root = create_file_structure(input)
    return root.sum_directory_size_if_smaller_than(100000)


def load_and_solve_part_2() -> int:
    input = load_file(7)
    return solve_part_2(input)


def solve_part_2(input: str) -> int:
    root = create_file_structure(input)
    dir_to_remove = root.find_directory_to_free_space(70000000, 30000000)
    if dir_to_remove is None:
        raise ValueError("Could not find a directory to free enough space")
    return dir_to_remove.get_size()


if __name__ == "__main__":
    run_and_benchmark(load_and_solve_part_1)
    run_and_benchmark(load_and_solve_part_2)
