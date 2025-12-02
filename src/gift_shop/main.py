from functools import cached_property


class ProductID:
    def __init__(self, id: str) -> None:
        self._id = id

    @cached_property
    def id_(self) -> str:
        return self._id

    @cached_property
    def digit_count(self) -> int:
        return len(self._id)

    @cached_property
    def is_repeating(self) -> bool:
        half: int = self.digit_count // 2
        return len(set(self._id)) == 1 or (self.digit_count % 2 == 0 and self._id[:half] == self._id[half:])


class ProductIDRange:
    def __init__(self, *, start: ProductID, end: ProductID):
        self.start = start
        self.end = end

    @property
    def largest_repeating_number_from_terminals(self) -> int:
        return 0
