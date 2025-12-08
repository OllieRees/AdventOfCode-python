from typing import Iterator, Tuple

from cafeteria.main import FreshRange, Inventory


def main(lines: Iterator[str]) -> None:
    x = list(lines)
    split_pos = x.index("")
    inv = Inventory(
        fresh_ranges=(FreshRange(report_line=line) for line in x[:split_pos]),
        ingredient_ids=[int(line.strip()) for line in x[split_pos + 1 :]],
    )
    print(len(inv.fresh_ingredients))
