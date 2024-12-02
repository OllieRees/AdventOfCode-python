from enum import StrEnum
from pathlib import Path
from typing import Callable, Dict, Iterator, Tuple

import historianhysteria.main as historianHysteria

PUZZLES: Dict[Tuple[int, int], Callable[[Iterator[str]], None]] = {
    (2024, 1): historianHysteria.main
}


class InputMode(StrEnum):
    PRACTICE = "practice"
    REAL = "real"


class Puzzle:
    def __init__(self, *, day: int, year: int) -> None:
        self.day = day
        self.year = year

    @property
    def _executor(self) -> Callable[[Iterator[str]], None]:
        try:
            return PUZZLES[(self.year, self.day)]
        except KeyError as invalid_puzzle:
            raise NotImplementedError from invalid_puzzle

    def run(self, mode: InputMode) -> None:
        print(f"{mode} Puzzle for Year {self.year}, Day {self.day}")
        puzzle_input = PuzzleInput(puzzle=self, mode=mode)
        self._executor(puzzle_input.lines)


class PuzzleInput:
    def __init__(self, *, puzzle: Puzzle, mode: InputMode) -> None:
        self.puzzle = puzzle
        self.mode = mode

    @property
    def _filepath(self) -> Path:
        return Path(f"inputs/{self.puzzle.year}/{self.puzzle.day}/{self.mode}.txt")

    @property
    def lines(self) -> Iterator[str]:
        with open(self._filepath) as f:
            return iter(f.read().splitlines())
        raise FileNotFoundError
