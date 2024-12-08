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
    

def main(lines: Iterator[str]) -> None:
    search_grid = WordSearchGrid(grid=np.array([list(line) for line in lines]))