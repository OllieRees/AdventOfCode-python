from enum import StrEnum
from functools import reduce


class Operation(StrEnum):
    MULTIPLY = "*"
    ADD = "+"

    def operate(self, x: int, y: int) -> int:
        match self:
            case Operation.MULTIPLY:
                return x * y
            case Operation.ADD:
                return x + y
            case _:
                raise ValueError(f"Invalid operation: {self.value}")


class HomeworkGrid:
    def __init__(self, operands: list[list[int]], operations: list[Operation]) -> None:
        self._operands = operands
        self._operations = operations

    def _get_column(self, column_index: int) -> list[int]:
        return [row[column_index] for row in self._operands]

    def calculate(self) -> list[int]:
        return [
            reduce(lambda acc, x: operation.operate(x=acc, y=x), self._get_column(i))
            for i, operation in enumerate(self._operations)
        ]
