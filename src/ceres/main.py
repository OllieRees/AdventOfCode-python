import re
from dataclasses import dataclass
from typing import Iterator, List


class Word:
    def __init__(self, value: str) -> None:
        self.word = value


@dataclass(frozen=True, kw_only=True)
class GridBox:
    val: str
    x: int
    y: int

    def __post_init__(self):
        if len(self.val) != 1:
            raise TypeError("GridBox only supports characters")

    def __str__(self) -> str:
        return f"{self.val}: ({self.x}, {self.y})"


class GridLine:
    def __init__(self, value: List[GridBox]) -> None:
        self._value = value

    def __str__(self) -> str:
        return "".join(v.val for v in self._value)

    def search_word(self, word: Word) -> Iterator[List[GridBox]]:
        for m in re.finditer(word.word, str(self)):
            yield self._value[m.start() : m.end()]
        for m in re.finditer(word.word[::-1], str(self)):
            yield self._value[m.start() : m.end()]


class Grid:
    def __init__(self, lines: Iterator[str]) -> None:
        self._lines: list[str] = list(lines)

    def __create_box_from_coords(self, x: int, y: int) -> GridBox:
        return GridBox(val=self._lines[x][y], x=x, y=y)

    @property
    def column_count(self) -> int:
        return len(self._lines[0])

    @property
    def row_count(self) -> int:
        return len(self._lines)

    @property
    def horizontal_lines(self) -> List[GridLine]:
        return [GridLine([GridBox(val=c, x=i, y=j) for j, c in enumerate(line)]) for i, line in enumerate(self._lines)]

    @property
    def vertical_lines(self) -> List[GridLine]:
        rv = []
        for j in range(self.column_count):
            rv.append(GridLine([GridBox(val=self._lines[i][j], x=i, y=j) for i in range(self.row_count)]))
        return rv

    @property
    def forward_diagonals(self) -> List[GridLine]:
        rv = [GridLine([self.__create_box_from_coords(x=i, y=i) for i in range(self.column_count)])]
        for offset in range(1, self.row_count):
            rv.append(GridLine([self.__create_box_from_coords(x=i + offset, y=i) for i in range(self.column_count - offset)]))
            rv.append(GridLine([self.__create_box_from_coords(x=i, y=i + offset) for i in range(self.row_count - offset)]))
        return rv

    @property
    def backward_diagonals(self) -> List[GridLine]:
        rv = [GridLine([self.__create_box_from_coords(x=i, y=-(i + 1)) for i in range(self.column_count)])]
        for offset in range(1, self.row_count):
            rv.append(
                GridLine([self.__create_box_from_coords(x=offset + i, y=-(i + 1)) for i in range(self.column_count - offset)])
            )
            rv.append(GridLine([self.__create_box_from_coords(x=i, y=-(i + 1 + offset)) for i in range(self.row_count - offset)]))
        return rv


class WordSearchGrid:
    def __init__(self, *, grid: Grid, word: Word) -> None:
        self.grid = grid
        self.word = word

    def word_positions(self) -> Iterator[List[GridBox]]:
        for line in self.grid.horizontal_lines:
            for occurrence in line.search_word(self.word):
                yield occurrence
        for line in self.grid.vertical_lines:
            for occurrence in line.search_word(self.word):
                yield occurrence
        for line in self.grid.forward_diagonals:
            for occurrence in line.search_word(self.word):
                yield occurrence
        for line in self.grid.backward_diagonals:
            for occurrence in line.search_word(self.word):
                yield occurrence
