import re
from dataclasses import dataclass
from functools import cached_property
from typing import Iterator, List

import numpy as np


@dataclass(frozen=True, kw_only=True)
class WordSearchGrid:
    grid: np.typing.NDArray[List[List[str]]]

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
    

class WordSearchCounter:
    def __init__(self, *, grid: WordSearchGrid) -> None:
        self.grid= grid

    def count_horizontal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for horizontal in self.grid.horizontals for _ in pattern.finditer(horizontal))
    
    def count_vertical(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for vertical in self.grid.verticals for _ in pattern.finditer(vertical))
    
    def count_forward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.grid.forward_diagonals for _ in pattern.finditer(diagonal))
    
    def count_backward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.grid.backward_diagonals for _ in pattern.finditer(diagonal))
    
    def count_word_occurrences(self, *, pattern: re.Pattern[str]) -> int:
        return self.count_horizontal(pattern=pattern) + self.count_vertical(pattern=pattern) + self.count_forward_diagonal(pattern=pattern) + self.count_backward_diagonal(pattern=pattern)
   
    def count_grid_occurrences(self, *, grid: WordSearchGrid) -> int:
        return 0


def main(lines: Iterator[str]) -> None:
    counter = WordSearchCounter(grid=WordSearchGrid(grid=np.array([list(line) for line in lines])))
    print(f"Number of occurrences of XMAS in the search grid: {counter.count_word_occurrences(pattern=re.compile(r"(?=(XMAS|SAMX))"))}")

    mas_cross = np.array([[""], [""], [""]])
    print(f"Number of occurrences of X-MAS in the search grid: {counter.count_grid_occurrences(grid=WordSearchGrid(grid=mas_cross))}")