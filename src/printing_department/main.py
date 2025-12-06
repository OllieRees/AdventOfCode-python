from typing import Iterator, Optional, Tuple


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


class Grid:
    def __init__(self, *, positions: list[list[GridPosition]]) -> None:
        self._elements = positions

    @property
    def _nrow(self) -> int:
        return len(self._elements)

    @property
    def _ncol(self) -> int:
        return len(self._elements[0])

    def window_iterator(self, *, m: int, n: int) -> Iterator["Grid"]:
        return iter([])


def str2grid(grid_str: Iterator[str], roll_str: str) -> Grid:
    positions = [
        [GridPosition(roll=ToiletRoll() if token == roll_str else None, x=x, y=y) for y, token in enumerate(row)]
        for x, row in enumerate(grid_str)
    ]
    return Grid(positions=positions)
