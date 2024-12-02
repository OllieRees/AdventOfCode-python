from functools import cached_property
from typing import Iterator, List


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


def main(lines: Iterator[str]) -> None:
    reports = [Report(levels=[int(report) for report in report_line.split()]) for report_line in lines]
    print(f"Number of Reports that are safe: {len([report for report in reports if report.is_safe])}")
