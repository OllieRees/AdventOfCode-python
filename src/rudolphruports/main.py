from typing import Iterator, List


class Report:
    def __init__(self, levels: List[int]):
        self.levels = levels

    def __str__(self) -> str:
        return f"Report<levels={self.levels}>"    
    
    @property
    def _levels_difference(self) -> List[int]:
        return [y - x for x, y in zip(self.levels[:-1], self.levels[1:])]

    @property
    def is_safe(self) -> bool:
        return all(1 <= abs(level_diff) <= 3 for level_diff in self._levels_difference) and (
            all((level_diff < 0 for level_diff in self._levels_difference)) or all((level_diff > 0 for level_diff in self._levels_difference))
        )
    
def main(lines: Iterator[str]) -> None:
    reports = [Report(levels=[int(report) for report in report_line.split()]) for report_line in lines]
    print(f"Number of Reports that are safe: {len([report for report in reports if report.is_safe])}")

        