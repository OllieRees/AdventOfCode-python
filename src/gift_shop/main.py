from functools import cached_property
from typing import Iterator


class ProductID:
    def __init__(self, id: int) -> None:
        self._id = str(id)

    @cached_property
    def id_(self) -> int:
        return int(self)

    def __int__(self) -> int:
        return int(self._id)

    @cached_property
    def _digit_count(self) -> int:
        return len(self._id)

    @cached_property
    def is_repeating(self) -> bool:
        half: int = self._digit_count // 2
        return self._digit_count % 2 == 0 and self._id[:half] == self._id[half:]


class ProductIDRange:
    def __init__(self, *, start: ProductID, end: ProductID):
        self.start = start
        self.end = end

    @property
    def product_ids_in_range(self) -> Iterator[ProductID]:
        for x in range(self.start.id_, self.end.id_ + 1):
            yield ProductID(x)

    @property
    def repeating_numbers_from_range(self) -> Iterator[ProductID]:
        return filter(lambda x: x.is_repeating, self.product_ids_in_range)
