import re
from functools import cached_property
from typing import Iterator, List, Tuple

import numpy as np


class WordSearchGrid:
    def __init__(self, *, grid: np.typing.NDArray[List[List[str]]]):
        self.grid = grid

    @cached_property
    def _transpose(self) -> "WordSearchGrid":
        return WordSearchGrid(grid=self.grid.T)

    @property
    def horizontals(self) -> List[str]:
        return ["".join(row) for row in self.grid]

    @property
    def verticals(self) -> List[str]:
        return self._transpose.horizontals

    @property
    def forward_diagonals(self) -> List[str]:
        return ["".join(self.grid.diagonal(offset=offset)) for offset in range(-len(self.grid) + 1, len(self.grid[0]))]

    @property
    def backward_diagonals(self) -> List[str]:
        return ["".join(np.fliplr(self.grid).diagonal(offset=offset)) for offset in range(-len(self.grid) + 1, len(self.grid[0]))]

    def partition_grid(self, *, partition_size: Tuple[int, int]) -> List["WordSearchGrid"]:
        return [WordSearchGrid(grid=p) for ps in np.lib.stride_tricks.sliding_window_view(self.grid, partition_size) for p in ps]

    def __eq__(self, other) -> bool:
        if not isinstance(other, WordSearchGrid):
            return False
        return bool((self.grid == other.grid).all())


class WordSearchCounter:
    def __init__(self, *, grid: WordSearchGrid) -> None:
        self.grid = grid

    def count_horizontal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for horizontal in self.grid.horizontals for _ in pattern.finditer(horizontal))

    def count_vertical(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for vertical in self.grid.verticals for _ in pattern.finditer(vertical))

    def count_forward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.grid.forward_diagonals for _ in pattern.finditer(diagonal))

    def count_backward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.grid.backward_diagonals for _ in pattern.finditer(diagonal))

    def count_pattern_occurrences(self, *, pattern: re.Pattern[str]) -> int:
        return (
            self.count_horizontal(pattern=pattern)
            + self.count_vertical(pattern=pattern)
            + self.count_forward_diagonal(pattern=pattern)
            + self.count_backward_diagonal(pattern=pattern)
        )

    def count_grid_occurrences(self, *, grid: WordSearchGrid) -> int:
        return sum(1 for partition in self.grid.partition_grid(partition_size=grid.grid.shape) if partition == grid)


def main(lines: Iterator[str]) -> None:
    grid = WordSearchGrid(grid=np.array([list(line) for line in lines]))
    counter = WordSearchCounter(grid=grid)
    count = counter.count_pattern_occurrences(pattern=re.compile(r"(?=(XMAS|SAMX))"))
    print(f"Number of occurrences of XMAS in the search grid: {count}")
