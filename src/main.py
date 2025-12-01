from reader.main import InputMode, Puzzle

if __name__ == "__main__":
    day = int(input("Please enter the day: "))
    puzzle = Puzzle(year=2024, day=day)
    print("-------------------------------------------")
    puzzle.run(InputMode.PRACTICE)
    print("-------------------------------------------")
    puzzle.run(InputMode.REAL)
