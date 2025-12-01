from dataclasses import dataclass
from enum import StrEnum
from typing import Iterator


class Dial:
    def __init__(self, current_position: int = 0) -> None:
        self._current_position = current_position

    @property
    def current_position(self) -> int:
        return self._current_position

    @current_position.setter
    def current_position(self, value: int) -> None:
        if not (0 <= value <= 99):
            raise ValueError("Position must be between 0 and 99 inclusive.")
        self._current_position = value

    def rotate(self, step: "Step") -> None:
        match step.direction:
            case Direction.LEFT:
                self.current_position = (self.current_position - step.magnitude) % 100
            case Direction.RIGHT:
                self.current_position = (self.current_position + step.magnitude) % 100
            case _:
                raise ValueError("Invalid direction.")

    def rotate_new_position(self, step: "Step") -> int:
        self.rotate(step)
        return self.current_position


class Direction(StrEnum):
    LEFT = "L"
    RIGHT = "R"


@dataclass(frozen=True, kw_only=True)
class Step:
    direction: Direction
    magnitude: int


class StepsConverter:
    def from_lines(self, lines: Iterator[str]) -> Iterator[Step]:
        for line in lines:
            yield Step(direction=Direction(line[0].upper()), magnitude=int(line[1:]))
