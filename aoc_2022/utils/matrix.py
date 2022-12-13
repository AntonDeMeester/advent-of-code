from typing import Generator, Generic, TypeVar

from .space import Coordinate

T = TypeVar("T")


class Matrix(Generic[T]):
    """Matrix with horizontal x (left to right) and vertical y (top to bottom)"""

    def __init__(self, data: list[list[T]]):
        self.data = data
        self._i = 0
        self._j = 0

    def get(self, x: int, y: int) -> T:
        return self.data[y][x]

    def get_from_coordinate(self, coord: Coordinate) -> T:
        return self.get(coord.x, coord.y)

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


class BoundedMatrix(Matrix[T]):
    def get(self, x: int, y: int) -> T | None:  # type: ignore
        if self.test_boundaries(x, y) is False:
            return None
        return self.data[y][x]

    def get_from_coordinate(self, coord: Coordinate) -> T | None:  # type: ignore
        return self.get(coord.x, coord.y)

    def test_boundaries(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.horizontal_length():
            return False
        if y < 0 or y >= self.vertical_length():
            return False
        return True
