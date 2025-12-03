from reader.main import InputMode, Puzzle

if __name__ == "__main__":
    year = 2025
    day = int(input("Please enter the day: "))
    puzzle = Puzzle(year=year, day=day)
    print("-------------------------------------------")
    puzzle.run(InputMode.PRACTICE)
    print("-------------------------------------------")
    puzzle.run(InputMode.REAL)
    try:
        puzzle.run(InputMode.BIGBOY)
    except FileNotFoundError:
        print(f"BigBoy puzzle doesn't exist for {year}-{day}")
