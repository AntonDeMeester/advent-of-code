def load_file(day: int, part: int | None = None) -> str:
    part_file = f"input_{part}" if part is not None else "input"
    with open(f"aoc_2023/day_{day:02d}/{part_file}.txt", "r") as f:
        return f.read()


def split_by(input: str, char: str) -> list[str]:
    return input.split(char)


def split_by_newline(input: str) -> list[str]:
    return split_by(input, "\n")


def split_by_double_newline(input: str) -> list[str]:
    return split_by(input, "\n\n")
