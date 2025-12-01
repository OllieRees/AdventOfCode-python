from dataclasses import dataclass
from enum import StrEnum
from typing import Iterator


class Direction(StrEnum):
    LEFT = "L"
    RIGHT = "R"

    def move(self, position: int, magnitude: int) -> int:
        match self:
            case Direction.LEFT:
                return (position - magnitude) % 100
            case Direction.RIGHT:
                return (position + magnitude) % 100

    def passes_origin_once(self, position: int, magnitude: int) -> bool:
        if position == 0:
            return False
        magnitude = magnitude % 100
        match self:
            case Direction.LEFT:
                return position - magnitude <= 0
            case Direction.RIGHT:
                return position + magnitude >= 100


class Dial:
    def __init__(self, current_position: int = 0) -> None:
        self._current_position = current_position
        self._pass_origin_count = 0
        self._stop_at_origin_count = 0

    @property
    def passed_origin(self) -> int:
        return self._pass_origin_count

    @property
    def stops_at_origin(self) -> int:
        return self._stop_at_origin_count

    @property
    def current_position(self) -> int:
        return self._current_position

    @current_position.setter
    def current_position(self, value: int) -> None:
        if not (0 <= value <= 99):
            raise ValueError("Position must be between 0 and 99 inclusive.")
        if value == 0:
            self._stop_at_origin_count += 1
        self._current_position = value

    def rotate(self, rotation: "Rotation") -> None:
        self._pass_origin_count += rotation.magnitude // 100 + int(rotation.passes_origin_once(self._current_position))
        self.current_position = rotation.rotate(self._current_position)


@dataclass(frozen=True, kw_only=True)
class Rotation:
    direction: Direction
    magnitude: int

    def __post_init__(self):
        if self.magnitude < 0:
            raise ValueError("magnitude must be positive")

    def rotate(self, position: int) -> int:
        return self.direction.move(position, self.magnitude)

    def passes_origin_once(self, position: int) -> bool:
        return self.direction.passes_origin_once(position, self.magnitude)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rotation):
            raise TypeError("Cannot compare Rotation with different type.")
        return (self.direction, self.magnitude) == (other.direction, other.magnitude)


class StepsConverter:
    def from_lines(self, lines: Iterator[str]) -> Iterator[Rotation]:
        for line in lines:
            yield Rotation(direction=Direction(line[0].upper()), magnitude=int(line[1:]))
