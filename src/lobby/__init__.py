from typing import Iterator

from lobby.main import Bank, Battery


def largest_2_digits(bank: Bank) -> int:
    if len(bank.batteries) == 1:
        return bank.batteries[0].voltage
    if len(bank.batteries) == 2:
        return bank.batteries[0].voltage * 10 + bank.batteries[1].voltage
    first_battery = bank.batteries[0]
    second_battery = bank.batteries[1]
    for battery in bank.batteries[2:]:
        if second_battery > first_battery:
            first_battery = second_battery
            second_battery = battery
        elif battery > second_battery:
            second_battery = battery
    return first_battery.voltage * 10 + second_battery.voltage


def main(lines: Iterator[str]) -> None:
    banks = [Bank(batteries=[Battery(int(c)) for c in line]) for line in lines]
    print(sum(largest_2_digits(bank) for bank in banks))
