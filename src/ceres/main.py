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
    
    def _count_horizontal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for horizontal in self.horizontals for _ in pattern.finditer(horizontal))
    
    def _count_vertical(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for vertical in self.verticals for _ in pattern.finditer(vertical))
    
    def _count_forward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.forward_diagonals for _ in pattern.finditer(diagonal))
    
    def _count_backward_diagonal(self, *, pattern: re.Pattern[str]) -> int:
        return sum(1 for diagonal in self.backward_diagonals for _ in pattern.finditer(diagonal))
    
    def count_word(self, *, pattern: re.Pattern[str]) -> int:
        return self._count_horizontal(pattern=pattern) + self._count_vertical(pattern=pattern) + self._count_forward_diagonal(pattern=pattern) + self._count_backward_diagonal(pattern=pattern)
    

def main(lines: Iterator[str]) -> None:
    search_grid = WordSearchGrid(grid=np.array([list(line) for line in lines]))
    pattern: re.Pattern[str] = re.compile(r"(?=(XMAS|SAMX))")
    print(f"Number of occurrences of XMAS in the search grid: {search_grid.count_word(pattern=pattern)}")