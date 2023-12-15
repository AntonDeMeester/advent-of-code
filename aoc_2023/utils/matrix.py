from typing import Generator, Generic, TypeVar, Sequence
from copy import deepcopy

from .space import Coordinate

T = TypeVar("T")


class Matrix(Generic[T]):
    """Matrix with horizontal x (left to right) and vertical y (top to bottom)"""

    def __init__(self, data: Sequence[Sequence[T]]):
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

    def get_adjecent_values(self, coord: Coordinate) -> list[T]:
        results: list[T] = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                results.append(self.get(coord.x + i, coord.y + j))
        return results

    def get_adjecent_cardinal_values(self, coord: Coordinate) -> list[T]:
        results = [
            self.get(coord.x + 1, coord.y + 0),
            self.get(coord.x + 0, coord.y + 1),
            self.get(coord.x - 1, coord.y + 0),
            self.get(coord.x + 0, coord.y - 1),
        ]
        return results

    def copy(self) -> "Matrix[T]":
        return self.__class__(deepcopy(self.data))

    def transpose(self) -> "Matrix[T]":
        return self.__class__(self.get_columns())

    def get_rows(self) -> Sequence[Sequence[T]]:
        return self.data

    def get_columns(self) -> list[list[T]]:
        return [self.get_column(i) for i in range(self.horizontal_length())]


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
