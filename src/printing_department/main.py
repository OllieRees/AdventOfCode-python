from typing import Iterator, Optional, Tuple

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


class ToiletRoll:
    def __str__(self) -> str:
        return "@"


class GridPosition:
    def __init__(self, *, roll: Optional[ToiletRoll], x: int, y: int) -> None:
        self._roll = roll
        self._x = x
        self._y = y

    @property
    def roll(self) -> Optional[ToiletRoll]:
        return self._roll

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def is_empty(self) -> bool:
        return self._roll is None

    def __str__(self) -> str:
        return "." if self.is_empty else str(self._roll)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GridPosition):
            raise TypeError()
        return self.is_empty == value.is_empty and self.x == value.x and self.y == value.y


class Grid:
    def __init__(self, *, positions: list[list[GridPosition]]) -> None:
        self._elements = positions

    @property
    def _nrow(self) -> int:
        return len(self._elements)

    @property
    def _ncol(self) -> int:
        return len(self._elements[0])

    @property
    def _np_arr(self) -> np._typing.NDArray:
        return np.array(self._elements)

    @property
    def middle(self) -> Optional[GridPosition]:
        if self._nrow % 2 == 0 or self._ncol % 2 == 0:
            return None
        return self._elements[self._nrow // 2][self._ncol // 2]

    @property
    def roll_count(self) -> int:
        return sum(1 for row in self._elements for e in row if not e.is_empty)

    def window_iterator(self, *, win_row_cnt: int, win_col_cnt: int) -> Iterator["Grid"]:
        return iter(Grid(positions=poss) for row in sliding_window_view(self._np_arr, (win_row_cnt, win_col_cnt)) for poss in row)

    def __str__(self) -> str:
        return "\n".join(["".join([str(e) for e in row]) for row in self._elements])


def str2grid(grid_str: Iterator[str], roll_str: str) -> Grid:
    positions = [
        [GridPosition(roll=ToiletRoll() if token == roll_str else None, x=x, y=y) for y, token in enumerate(row)]
        for x, row in enumerate(grid_str)
    ]
    return Grid(positions=positions)
