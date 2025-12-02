from typing import Iterator

from gift_shop.main import ProductID, ProductIDRange


def main(lines: Iterator[str]) -> None:
    rv = []
    line = next(lines)
    for range in line.split(","):
        start, end = range.strip().split("-", 1)
        rv.append(ProductIDRange(start=ProductID(start), end=ProductID(end)))
