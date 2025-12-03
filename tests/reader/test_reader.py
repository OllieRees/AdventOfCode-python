from pathlib import Path
from unittest import TestCase

import pytest

from reader.main import InputMode, Puzzle, PuzzleInput


class MockPuzzleInput(PuzzleInput):
    def __init__(self, *, puzzle: Puzzle, mode: InputMode, filepath: str | None = None) -> None:
        super().__init__(puzzle=puzzle, mode=mode)
        self.filepath = filepath

    @property
    def _filepath(self) -> str:
        return self.filepath or super()._filepath


class TestPuzzle(TestCase):
    def test_bad_year_day(self) -> None:
        with pytest.raises(ValueError, match="No puzzle found for year and day. Year=2000 Day=1"):
            Puzzle(year=2000, day=1)

    def test_executor_exists(self) -> None:
        assert Puzzle(year=2024, day=1)._executor

    def test_executor_does_not_exist(self) -> None:
        with pytest.raises(ValueError, match="No puzzle found for year and day. Year=2000 Day=1"):
            assert Puzzle(year=2000, day=1)._executor


class TestPuzzleInput(TestCase):
    def setUp(self):
        self.puzzle = Puzzle(year=2024, day=1)
        self.practice_input = PuzzleInput(puzzle=self.puzzle, mode=InputMode.PRACTICE)
        self.real_input = PuzzleInput(puzzle=self.puzzle, mode=InputMode.REAL)

    def test_filepath_practice_mode(self) -> None:
        assert MockPuzzleInput(puzzle=self.puzzle, mode=InputMode.PRACTICE)._filepath == Path("inputs/2024/1/practice.txt")

    def test_filepath_real_mode(self) -> None:
        assert MockPuzzleInput(puzzle=self.puzzle, mode=InputMode.REAL)._filepath == Path("inputs/2024/1/real.txt")

    def test_lines(self) -> None:
        mock_input = MockPuzzleInput(puzzle=self.puzzle, mode=InputMode.PRACTICE, filepath="tests/reader/mocks/lines.txt")
        assert list(mock_input.lines) == ["testing", "reader", "lines"]

    def test_lines_on_file_not_found(self) -> None:
        mock_input = MockPuzzleInput(puzzle=self.puzzle, mode=InputMode.PRACTICE, filepath="mocks/no_file.txt")
        with pytest.raises(FileNotFoundError):
            mock_input.lines
