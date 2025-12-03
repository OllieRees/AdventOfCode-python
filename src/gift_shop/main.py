import re
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
    def repeats_once(self) -> bool:
        return re.search(r"^(\d+)(\1)$", self._id) is not None

    @cached_property
    def is_repeating(self) -> bool:
        return re.search(r"^(\d+)\1+$", self._id) is not None


class ProductIDRange:
    def __init__(self, *, start: ProductID, end: ProductID):
        self.start = start
        self.end = end

    @property
    def product_ids_in_range(self) -> Iterator[ProductID]:
        for x in range(self.start.id_, self.end.id_ + 1):
            yield ProductID(x)
