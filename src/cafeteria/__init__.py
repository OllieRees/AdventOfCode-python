from typing import Iterator

from cafeteria.main import Document


def main(lines: Iterator[str]) -> None:
    report = Document(lines=lines).report
    print(f"Number of fresh ingredients: {len(report.fresh_ingredients)}")
    print(f"Range Size: {sum(fresh_range.range_size for fresh_range in report.fresh_ranges)}")
