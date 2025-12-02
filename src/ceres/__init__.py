from typing import Iterator

from ceres import main as ceres


def main(lines: Iterator[str]) -> None:
    word = ceres.Word("XMAS")
    grid = ceres.Grid(lines)
    wordsearch = ceres.WordSearchGrid(grid=grid, word=word)
    print(len(list(wordsearch.word_positions())))
