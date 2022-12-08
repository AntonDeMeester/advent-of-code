from typing import Generator, Generic, TypeVar

T = TypeVar("T")


class Matrix(Generic[T]):
    """Matrix with horizontal x (left to right) and vertical y (top to bottom)"""

    def __init__(self, data: list[list[T]]):
        self.data = data
        self._i = 0
        self._j = 0

    def get(self, x: int, y: int) -> T:
        return self.data[y][x]

    def horizontal_length(self) -> int:
        return len(self.data[0])

    def vertical_length(self) -> int:
        return len(self.data)

    def get_row(self, index: int) -> list[T]:
        return self.data[index]

    def get_column(self, index: int) -> list[T]:
        return [x[index] for x in self.data]

    def __iter__(self) -> Generator[tuple[int, int, T], None, None]:
        for j, row in enumerate(self.data):
            for i, value in enumerate(row):
                yield (i, j, value)
