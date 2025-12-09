import re
from typing import Iterator, Optional, Set


class FreshRange:
    def __init__(self, *, start: int, end: int) -> None:
        if end < start:
            raise ValueError("End must be larger than start")
        self._start: int = start
        self._end: int = end

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def range_size(self) -> int:
        if self.start == self.end:
            return 1
        return self.end - self.start + 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FreshRange):
            raise TypeError()
        return self.start == other.start and self.end == other.end

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def __hash__(self):
        return hash((self.start, self.end))

    def is_in_range(self, ingredient: int) -> bool:
        return self.start <= ingredient <= self.end

    def superset(self, other: "FreshRange") -> Optional["FreshRange"]:
        if self.start == other.start:
            return FreshRange(start=self.start, end=max([self.end, other.end]))
        if self.end == other.end:
            return FreshRange(start=min([self.start, other.start]), end=self.end)
        if self.end < other.end and self.end >= other.start:  # x0 -> y0 -> x1 -> y1
            return FreshRange(start=self.start, end=other.end)
        if other.end < self.end and other.end >= self.start:  # y0 -> x0 -> y1 -> x1
            return FreshRange(start=other.start, end=self.end)
        return None


class Report:
    def __init__(self, *, fresh_ranges: set[FreshRange], ingredient_ids: list[int]) -> None:
        self._fresh_ranges = fresh_ranges
        self._ingredient_ids = ingredient_ids

    @property
    def _fresh_ranges_sorted(self) -> list[FreshRange]:
        return list(sorted(self._fresh_ranges, key=lambda r: r.end))

    def is_fresh(self, ingredient_id: int) -> bool:
        return any(fresh_range.is_in_range(ingredient_id) for fresh_range in self._fresh_ranges)

    @property
    def fresh_ingredients(self) -> Set[int]:
        return set(filter(lambda ingredient: self.is_fresh(ingredient), self._ingredient_ids))


class Document:
    def __init__(self, lines: Iterator[str]) -> None:
        self._lines = list(lines)
        i = self._lines.index("")
        self._range_lines = self._lines[:i]
        self._id_lines = self._lines[(i + 1) :]

    @property
    def _range_lines_generator(self) -> Iterator[str]:
        for line in self._lines:
            if line.strip() == "":
                return
            yield line

    @property
    def fresh_ingredient_ranges(self) -> Iterator[FreshRange]:
        for line in self._range_lines:
            x = re.findall(r"(\d+)-(\d+)", line)[0]
            yield FreshRange(start=int(x[0]), end=int(x[1]))

    @property
    def ingredient_ids(self) -> list[int]:
        return [int(id_) for id_ in self._id_lines]

    @property
    def report(self) -> Report:
        return Report(fresh_ranges=set(self.fresh_ingredient_ranges), ingredient_ids=self.ingredient_ids)
