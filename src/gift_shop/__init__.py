from typing import Iterator

from gift_shop.main import ProductID, ProductIDRange


def generate_product_id_ranges(line: str) -> Iterator[ProductIDRange]:
    for range in line.split(","):
        start, end = range.strip().split("-", 1)
        yield ProductIDRange(start=ProductID(int(start)), end=ProductID(int(end)))


def main(lines: Iterator[str]) -> None:
    half_count, repeat_count = 0, 0
    for line in lines:
        for range in generate_product_id_ranges(line):
            half_count += sum(int(product_id) for product_id in range.repeat_once_product_ids_from_range)
            repeat_count += sum(int(product_id) for product_id in range.repeating_product_ids_from_range)
    print(f"Total sum of invalid IDs: {half_count}")
    print(f"Total sum of invalid IDs: {repeat_count}")
