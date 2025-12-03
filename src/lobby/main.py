from typing import List, Optional


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

    @property
    def bank_binary_tree(self) -> "BankBinaryTree":
        return BankBinaryTree(bank=self)


class BankBinaryTree:
    def __init__(self, *, bank: Bank) -> None:
        self._bank = bank

    @property
    def root(self) -> Battery:
        return self._bank.batteries[0]

    @property
    def left(self) -> Optional["BankBinaryTree"]:
        if batteries := [b for b in self._bank.batteries[1:] if b.voltage <= self.root.voltage]:
            return BankBinaryTree(bank=Bank(batteries=batteries))
        return None

    @property
    def right(self) -> Optional["BankBinaryTree"]:
        if batteries := [b for b in self._bank.batteries[1:] if b.voltage > self.root.voltage]:
            return BankBinaryTree(bank=Bank(batteries=batteries))
        return None
