from typing import Iterator, List, Tuple


class Battery:
    def __init__(self, voltage: int) -> None:
        if not (0 < voltage < 10):
            raise ValueError(f"Voltage must be between 1-9 (inclusive).Voltage={voltage}")
        self._voltage = voltage

    @property
    def voltage(self) -> int:
        return self._voltage

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage == value.voltage

    def __neq__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage != value.voltage

    def __ge__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage >= value.voltage

    def __gt__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage > value.voltage

    def __le__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage <= value.voltage

    def __lt__(self, value: object) -> bool:
        if not isinstance(value, Battery):
            raise TypeError()
        return self.voltage < value.voltage


class Bank:
    def __init__(self, batteries: List[Battery]) -> None:
        self._batteries = batteries

    @property
    def batteries(self) -> List[Battery]:
        return self._batteries

    @property
    def size(self) -> int:
        return len(self.batteries)

    def sorted_battery_positions(self) -> Iterator[Tuple[int, Battery]]:
        return iter(sorted(enumerate(self.batteries), key=lambda x: x[1], reverse=True))
