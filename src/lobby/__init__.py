from typing import Iterator


def largest_n_digits(bank: list[int], n: int) -> int:
    if n == 1:
        return max(bank)
    pos, battery = max(enumerate(bank[: -(n - 1)]), key=lambda x: x[1])
    return int(battery * 10 ** (n - 1)) + largest_n_digits(bank[(pos + 1) :], n - 1)


def main(lines: Iterator[str]) -> None:
    banks: list[list[int]] = [[int(c) for c in line] for line in lines]
    print(sum(largest_n_digits(bank, 2) for bank in banks))
    print(sum(largest_n_digits(bank, 12) for bank in banks))
