from reader.main import InputMode, Puzzle

if __name__ == '__main__':
    puzzle = Puzzle(year=2024, day=1)
    print("-------------------------------------------")
    puzzle.run(InputMode.PRACTICE)
    print("-------------------------------------------")
    puzzle.run(InputMode.REAL)
