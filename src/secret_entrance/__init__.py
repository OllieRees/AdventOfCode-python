from typing import Iterator

from secret_entrance import main as SecretEntrance


def main(lines: Iterator[str]) -> None:
    dial = SecretEntrance.Dial(current_position=50)
    steps = SecretEntrance.StepsConverter().from_lines(lines)
    positions: list[int] = [dial.rotate_new_position(step) for step in steps]
    print(len([1 for pos in positions if pos == 0]))
