from typing import Iterator

from printing_department.main import Grid, str2grid


def get_total_count(grid: Grid) -> int:
    if cnt := grid.accessible_by_forklift_count:
        return cnt + get_total_count(grid.move_rolls())
    return 0


def main(lines: Iterator[str]) -> None:
    grid = str2grid(lines, "@")
    print(grid.accessible_by_forklift_count)
    print(get_total_count(grid))
