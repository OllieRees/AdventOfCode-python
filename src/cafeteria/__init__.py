from typing import Iterator, Tuple

from cafeteria.main import Document, FreshRange, Report


def main(lines: Iterator[str]) -> None:
    report = Document(lines=lines).report
    print(report.fresh_ingredients)
