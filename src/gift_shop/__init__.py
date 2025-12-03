from typing import Iterator

from gift_shop.main import ProductID, ProductIDRange


def generate_product_id_ranges(line: str) -> Iterator[ProductIDRange]:
    for range in line.split(","):
        start, end = range.strip().split("-", 1)
        yield ProductIDRange(start=ProductID(int(start)), end=ProductID(int(end)))


def main(lines: Iterator[str]) -> None:
    counter = sum(
        int(product_id)
        for line in lines
        for range in generate_product_id_ranges(line)
        for product_id in range.repeating_numbers_from_range
    )
    print(f"Total sum of invalid IDs: {counter}")
