from typing import Iterator

from secret_entrance import main as SecretEntrance


def main(lines: Iterator[str]) -> None:
    print([step for step in SecretEntrance.StepsConverter().from_lines(lines)])
