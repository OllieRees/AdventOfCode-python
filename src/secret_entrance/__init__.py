from typing import Iterator

from src import secret_entrance as SecretEntrance


def main(lines: Iterator[str]) -> None:
    print([step for step in SecretEntrance.StepsConverter().from_lines(lines)])
