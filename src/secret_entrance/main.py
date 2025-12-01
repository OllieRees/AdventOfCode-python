from dataclasses import dataclass
from enum import StrEnum
from typing import Iterator


class Dial:
    def __init__(self, current_position: int = 0) -> None:
        self._current_position = current_position
        self._pass_origin_count = 0
        self._stops_at_origin = 0

    @property
    def passed_origin(self) -> int:
        return self._pass_origin_count

    @property
    def stops_at_origin(self) -> int:
        return self._stops_at_origin

    @property
    def current_position(self) -> int:
        return self._current_position

    @current_position.setter
    def current_position(self, value: int) -> None:
        if not (0 <= value <= 99):
            raise ValueError("Position must be between 0 and 99 inclusive.")
        if value == 0:
            self._stops_at_origin += 1
        self._current_position = value

    def rotate(self, step: "Step") -> None:
        match step.direction:
            case Direction.LEFT:
                if self.current_position == 0:
                    self._pass_origin_count -= 1
                self._pass_origin_count += abs((self.current_position - step.magnitude) // 100)
                self.current_position = (self.current_position - step.magnitude) % 100
                if self.current_position == 0:
                    self._pass_origin_count += 1
            case Direction.RIGHT:
                self._pass_origin_count += abs((self.current_position + step.magnitude) // 100)
                self.current_position = (self.current_position + step.magnitude) % 100


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
