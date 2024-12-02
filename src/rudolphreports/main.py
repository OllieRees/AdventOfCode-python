from functools import cached_property
from typing import Iterator, List

from paprika import catch


class UnsafeReport(Exception):
    pass


class LevelTrend:
    def __init__(self, *, levels: List[int]) -> None:
        self.levels = levels 

    @property
    def all_incrementing(self) -> bool:
        return all(y > x for x, y in zip(self.levels, self.levels[1:]))
    
    @property 
    def all_decrementing(self) -> bool:
        return all(y < x for x, y in zip(self.levels, self.levels[1:]))
    
    @property
    def is_consistent(self) -> bool:
        return self.all_incrementing or self.all_decrementing


class LevelChanges:
    def __init__(self, *, levels: List[int]) -> None:
        self.level_changes = [y - x for x, y in zip(levels, levels[1:])]

    def within_range(self, min: int, max: int) -> bool:
        return all(min <= abs(level) <= max for level in self.level_changes)


class Report:
    def __init__(self, levels: List[int]):
        self.levels = levels

    def __str__(self) -> str:
        return f"Report<levels={self.levels}>"
    
    @cached_property
    def level_changes(self) -> LevelChanges:
        return LevelChanges(levels=self.levels)
    
    @cached_property
    def level_trend(self) -> LevelTrend:
        return LevelTrend(levels=self.levels)
         
    @property
    def is_safe(self) -> bool:
        return self.level_trend.is_consistent and self.level_changes.within_range(1, 3)

    def _remove_level(self, *, index: int) -> "Report":
        return Report(levels=self.levels[:index] + self.levels[(index + 1):])
    
    @property
    def _dampeners(self) -> Iterator["Report"]:
        return (self._remove_level(index=i) for i, _ in enumerate(self.levels))
    
    def apply_dampener(self) -> "Report":
        if self.is_safe:
            return self
        try:
            return next(r for r in self._dampeners if r.is_safe)
        except StopIteration as err:
            raise UnsafeReport from err
    
    @property
    @catch(exception=UnsafeReport, handler=lambda _: False)
    def is_safe_with_dampener(self) -> bool:         
        return self.apply_dampener().is_safe


def main(lines: Iterator[str]) -> None:
    reports = [Report(levels=[int(report) for report in report_line.split()]) for report_line in lines]
    print(f"Number of Reports that are safe: {len([report for report in reports if report.is_safe])}")
    print(f"Number of Dampened Reports that are safe: {len([report for report in reports if report.is_safe_with_dampener])}")
