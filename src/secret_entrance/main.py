from dataclasses import dataclass
from enum import StrEnum
from typing import Iterator


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
            yield Step(direction=line[0].upper(), magnitude=int(line[1:]))


def main(lines: Iterator[str]) -> None:
    print([step for step in StepsConverter().from_lines(lines)])
