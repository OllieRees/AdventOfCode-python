from typing import List, Iterator
from collections import Counter


class HistoriansLists:
    def __init__(self, *, left: List[int], right: List[int]) -> None:
        self.left = left
        self.right = right

    @property
    def total_distance(self) -> int:
        return sum(abs(x - y) for x, y in zip(sorted(self.left), sorted(self.right)))

    @property
    def similarity_score(self) -> int:
        counter = Counter(self.right)
        return sum(location * counter[location] for location in self.left)

    @classmethod
    def from_input(cls, lines: Iterator[str]) -> "HistoriansLists":
        xs = [tuple(map(int, line.split())) for line in lines]
        return HistoriansLists(left=[x[0] for x in xs], right=[x[1] for x in xs])


def main(lines: Iterator[str]) -> None:
    p = HistoriansLists.from_input(lines)
    print(f"Total Distance: {p.total_distance}")
    print(f"Similarity Score: {p.similarity_score}")
