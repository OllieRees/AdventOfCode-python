from typing import Iterator

from secret_entrance import main as SecretEntrance


def main(lines: Iterator[str]) -> None:
    steps = SecretEntrance.StepsConverter().from_lines(lines)
    dial = SecretEntrance.Dial(current_position=50)
    for step in steps:
        dial.rotate(step)
    print(dial.stops_at_origin)
    print(dial.count_dial_passed_origin)
