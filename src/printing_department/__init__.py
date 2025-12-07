from typing import Iterator

from printing_department.main import str2grid


def main(lines: Iterator[str]) -> None:
    grid = str2grid(lines, "@")
    cnt = grid.accessible_by_forklift_count
    print(cnt)
