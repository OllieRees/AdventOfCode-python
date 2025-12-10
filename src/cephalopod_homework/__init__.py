from typing import Iterator

from cephalopod_homework.main import HomeworkGrid, Operation


def main(lines: Iterator[str]) -> None:
    lines_list = list(lines)
    operands: list[list[int]] = [[int(x.strip()) for x in row.strip().split()] for row in lines_list[:-1]]
    operations: list[Operation] = list(map(lambda x: Operation(x.strip()), lines_list[-1].split()))
    grid = HomeworkGrid(operands=operands, operations=operations)
    print(f"Sum of calculations: {sum(grid.calculate())}")
