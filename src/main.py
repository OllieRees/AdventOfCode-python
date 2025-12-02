from reader.main import InputMode, Puzzle

if __name__ == "__main__":
    year = 2024
    day = int(input("Please enter the day: "))
    puzzle = Puzzle(year=year, day=day)
    print("-------------------------------------------")
    puzzle.run(InputMode.PRACTICE)
    print("-------------------------------------------")
    puzzle.run(InputMode.REAL)
    print("-------------------------------------------")
    try:
        puzzle.run(InputMode.BIGBOY)
    except FileNotFoundError:
        print(f"No big boy for year {year}, day {day}")
    print("-------------------------------------------")
