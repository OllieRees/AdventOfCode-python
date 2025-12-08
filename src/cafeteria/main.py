import re
from functools import reduce
from typing import Iterator, Optional, Set


class Ingredient:
    def __init__(self, *, id_: int, is_fresh: bool) -> None:
        self._id = id_
        self.is_fresh = is_fresh


class FreshRange:
    def __init__(self, *, report_line: str) -> None:
        self._report_line = report_line
        grps = re.findall(r"(\d+)-(\d+)", self._report_line)[0]
        self._start = int(grps[0])
        self._end = int(grps[1])

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def id_set(self) -> Set[int]:
        return set(range(self.start, self.end + 1))

    def is_in_range(self, ingredient: int) -> bool:
        return self.start <= ingredient <= self.end

    def superset(self, other: "FreshRange") -> Optional["FreshRange"]:
        if len(self.id_set.intersection(other.id_set)) >= 1:
            start = self.start if self.start <= other.start else other.start
            end = self.end if self.end >= other.end else other.end
            return FreshRange(report_line=f"{start}-{end}")
        return None


class Inventory:
    def __init__(self, *, fresh_ranges: Iterator[FreshRange], ingredient_ids: list[int]) -> None:
        self._fresh_ranges = fresh_ranges
        self._ingredient_ids = ingredient_ids

    @property
    def _fresh_ingredient_ids(self) -> Set[int]:
        return reduce(lambda x, y: x.union(y), (r.id_set for r in self._fresh_ranges))

    @property
    def fresh_ingredients(self) -> Set[int]:
        return self._fresh_ingredient_ids.intersection(self._ingredient_ids)
